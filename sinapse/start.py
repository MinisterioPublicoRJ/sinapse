import base64
import json
import requests
from string import ascii_letters as abc

from copy import deepcopy
from datetime import datetime
from functools import wraps

from flask import (
    jsonify,
    request,
    render_template,
    session,
    url_for,
    redirect
)

from sinapse.buildup import (
    app,
    _LOG_MONGO,
    _ENDERECO_NEO4J,
    _AUTH,
    _HEADERS,
    _AUTH_MPRJ,
    _USERINFO_MPRJ,
)
from sinapse.detran.tasks import get_photos_asynch
from sinapse.detran.utils import get_node_id
from sinapse.queries import find_next_nodes


def redirecionar(url, code=302):
    retorno = redirect(url, code=code)
    retorno.autocorrect_location_header = False
    return retorno


def respostajson(response, **kwargs):
    usuario = session.get('usuario', "dummy")
    sessionid = request.cookies.get('session')
    _log_response(usuario, sessionid, response)
    dados = response.json()
    if isinstance(dados, dict):
        dados.update(kwargs)

    if resposta_sensivel(dados):
        return jsonify(remove_info_sensiveis(dados))

    return jsonify(dados)


def limpa_nos(nos):
    copia_nos = deepcopy(nos)
    for no in copia_nos:
        if 'sensivel' in no['properties'].keys():
            no['labels'] = ['sigiloso']
            no['properties'] = dict()

    return copia_nos


def limpa_linhas(linhas):
    copia_linhas = deepcopy(linhas)
    novas_linhas = []
    for linha in copia_linhas:
        if isinstance(linha, list):
            novas_linhas.append(limpa_linhas(linha))
        elif isinstance(linha, dict):
            if 'sensivel' in linha.keys():
                novas_linhas.append(dict())
            else:
                novas_linhas.append(linha)

    return novas_linhas


def limpa_relacoes(relacoes):
    copia_relacoes = deepcopy(relacoes)
    for relacao in copia_relacoes:
        if 'sensivel' in relacao['properties'].keys():
            relacao['type'] = 'sigiloso'
            relacao['properties'] = dict()

    return copia_relacoes


def remove_info_sensiveis(resposta):
    resp = deepcopy(resposta)
    for data in resp['results'][0]['data']:
        data['graph']['nodes'] = limpa_nos(data['graph']['nodes'])
        data['row'] = limpa_linhas(data['row'])
        data['graph']['relationships'] = limpa_relacoes(
            data['graph']['relationships'])

    return resp


def conta_nos(opcoes, letras):
    count_letras = ['count(%s)' % letra for letra in letras]
    count_letras = ' + '.join(count_letras)
    query = {'statements': [{
        'statement': (
            ' '.join(opcoes) +
            ' return %s' % count_letras
            ),
        'resultDataContents': ['row', 'graph']
    }]}

    response = requests.post(
        _ENDERECO_NEO4J % '/db/data/transaction/commit',
        data=json.dumps(query),
        auth=_AUTH,
        headers=_HEADERS)

    return response.json()['results'][0]['data'][0]['row'][0]


def conta_expansoes(n_id):
    query = {"statements": [{
        "statement": "MATCH r = (n)-[*..1]-(x) where id(n) = %s"
        " return count(r), count(n), count(x)" % n_id,
    }]}

    response = requests.post(
        _ENDERECO_NEO4J % '/db/data/transaction/commit',
        data=json.dumps(query),
        auth=_AUTH,
        headers=_HEADERS)

    return response.json()['results'][0]['data'][0]['row']


def resposta_sensivel(resposta):
    def parser_dicionario(dicionario, chave):
        if isinstance(dicionario, dict):
            for k, v in dicionario.items():
                if k == chave:
                    yield v
                else:
                    yield from parser_dicionario(v, chave)
        elif isinstance(dicionario, list):
            for item in dicionario:
                yield from parser_dicionario(item, chave)

    try:
        return next(parser_dicionario(resposta, 'sensivel'))
    except StopIteration:
        return False


def _log_response(usuario, sessionid, response):
    _LOG_MONGO.insert(
        {
            'usuario': usuario,
            'datahora': datetime.now(),
            'sessionid': sessionid,
            'resposta': response.json()
        }
    )


def _autenticar(usuario, senha):
    "Autentica o usuário no SCA"
    sessao = requests.session()
    senha = base64.b64encode(senha.encode('utf-8')).decode('utf-8')
    response = sessao.post(
        url=_AUTH_MPRJ,
        data={
            'username': usuario,
            'password': senha
        })
    if response.status_code == 200:
        response = sessao.get(url=_USERINFO_MPRJ)
        permissoes = json.loads(
            response.content.decode('utf-8'))['permissions']

        if 'ROLE_Conexao' in permissoes and permissoes['ROLE_Conexao']:
            return usuario
    return None


def login_necessario(funcao):
    @wraps(funcao)
    def funcao_decorada(*args, **kwargs):
        if "usuario" not in session:
            return "Não autorizado", 403
        return funcao(*args, **kwargs)
    return funcao_decorada


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        resposta = _autenticar(usuario, senha)
        if resposta:
            session['usuario'] = resposta
            return redirecionar(url_for(request.args.get('next', 'raiz')))

        session['flask_msg'] = 'Falha no login'
        return render_template('login.html'), 401


@app.route("/logout", methods=["GET", "POST"])
def logout():
    if request.headers.get('x-purpose'):
        return "NOK", 404

    if 'usuario' in session:
        del session['usuario']
        sucesso = 'Você foi deslogado com sucesso'
        session['flask_msg'] = sucesso

    return redirecionar(url_for('login'), code=302)


@app.route("/")
def raiz():
    if 'usuario' not in session:
        retorno = redirecionar(
            url_for('login', next=request.endpoint),
            code=302)
        retorno.autocorrect_location_header = False
        return retorno
    return render_template('index.html')


@app.route("/api/node")
@login_necessario
def api_node():
    node_id = request.args.get('node_id')

    query = {"statements": [{
        "statement": "MATCH  (n) where id(n) = " + node_id + " return n",
        "resultDataContents": ["row", "graph"]
    }]}

    response = requests.post(
        _ENDERECO_NEO4J % '/db/data/transaction/commit',
        data=json.dumps(query),
        auth=_AUTH,
        headers=_HEADERS)

    return respostajson(response)


def _monta_query_filtro_opcional(label, prop, val, letra):
    if prop == 'pess_dk':
        return "optional match (%s:%s {%s:%s})" % (
            letra,
            label,
            prop,
            val
        )

    return "optional match (%s:%s {%s:toUpper('%s')})" % (
        letra,
        label,
        prop,
        val
    )


@app.route("/api/findNodes")
@login_necessario
def api_findNodes():
    plabel = request.args.get('label').split(',')
    pprop = request.args.get('prop').split(',')
    pval = request.args.get('val').split(',')
    # TODO: alterar para prepared statement

    letras = abc[0:len(plabel)]

    opcoes = []

    for label, prop, val, letra in zip(plabel,
                                       pprop,
                                       pval,
                                       letras):
        opcoes.append(
            _monta_query_filtro_opcional(
                label,
                prop,
                val,
                letra
            )
        )

    query = {'statements': [{
        'statement': (
            ' '.join(opcoes) +
            ' return %s limit 100' % (','.join(letras))
            ),
        'resultDataContents': ['row', 'graph']
    }]}

    response = requests.post(
        _ENDERECO_NEO4J % '/db/data/transaction/commit',
        data=json.dumps(query),
        auth=_AUTH,
        headers=_HEADERS)

    numero_de_nos = conta_nos(opcoes, letras)

    node_id = get_node_id(response.json())
    # Call asynchronously task
    # get_photos_asynch.delay(node_id)

    return respostajson(response, numero_de_nos=numero_de_nos)


@app.route("/api/nextNodes")
@login_necessario
def api_nextNodes():
    node_id = request.args.get('node_id')

    response = find_next_nodes(node_id)

    numero_expansoes = conta_expansoes(node_id)
    # Call asynchronously task
    #get_photos_asynch.delay(node_id)

    return respostajson(response, numero_de_expansoes=numero_expansoes)


@app.route("/api/nodeProperties")
@login_necessario
def api_nodeProperties():
    label = request.args.get('label')

    cypher = "MATCH (n:" + label + ")  RETURN  keys(n) limit 1"
    query = {"query": cypher}
    response = requests.post(
        _ENDERECO_NEO4J % '/db/data/cypher',
        data=json.dumps(query),
        auth=_AUTH,
        headers=_HEADERS)
    return respostajson(response)


@app.route("/api/labels")
@login_necessario
def api_labels():
    response = requests.get(
        _ENDERECO_NEO4J % '/db/data/labels',
        auth=_AUTH,
        headers=_HEADERS)
    return respostajson(response)


@app.route("/api/relationships")
@login_necessario
def api_relationships():
    response = requests.get(
        _ENDERECO_NEO4J % '/db/data/relationship/types',
        auth=_AUTH,
        headers=_HEADERS)
    return respostajson(response)


@app.context_processor
def mensagens_processor():
    def mensagens():
        try:
            return session.pop('flask_msg')
        except KeyError:
            return ''
    return dict(flask_msg=mensagens)

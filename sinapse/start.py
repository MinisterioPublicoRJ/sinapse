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
    _LOG_NEO4J,
    _LOG_ACESSO,
    _LOG_LOGIN,
    _ENDERECO_NEO4J,
    _AUTH,
    _HEADERS,
    _AUTH_MPRJ,
    _USERINFO_MPRJ,
)
from sinapse.tasks import (get_person_photo_asynch,
                           get_vehicle_photo_asynch)
from sinapse.detran.utils import get_node_id
from sinapse.queries import (find_next_nodes,
                             person_info,
                             vehicle_info)
from sinapse.whereabouts.whereabouts import (get_whereabouts_receita,
                                             get_whereabouts_credilink)


@app.before_request
def before_request():
    request.check_compliance = True


def parse_json_to_visjs(json, **kwargs):
    nodes = {}
    relationships = {}

    # Change this to have an error message
    if 'results' not in json:
        return json

    for result in json['results'][0]['data']:
        result_nodes = result['graph']['nodes']
        result_relationships = result['graph']['relationships']
        for node in result_nodes:
            nodes[node['id']] = node
        for relationship in result_relationships:
            relationships[relationship['id']] = relationship

    nodes = list(nodes.values())
    for d in nodes:
        d['type'] = d.pop('labels')

    relationships = list(relationships.values())
    for r in relationships:
        r['label'] = r.pop('type')
        r['from'] = r.pop('startNode')
        r['to'] = r.pop('endNode')
        r['arrows'] = "to"
        r['dashes'] = False

    json_visjs = {'nodes': nodes, 'edges': relationships}
    json_visjs.update(kwargs)

    return json_visjs


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


def get_path(resposta):
    paths = []
    for path in resposta['results'][0]['data']:
        ordered_path = []
        path_meta = path['meta'][0]
        path_graph = path['graph']

        for element in path_meta:
            if element['type'] == 'node':
                for node in path_graph['nodes']:
                    if int(node['id']) == element['id']:
                        ordered_path.append(node)
            if element['type'] == 'relationship':
                for rel in path_graph['relationships']:
                    if int(rel['id']) == element['id']:
                        ordered_path.append(rel)

        paths.append(ordered_path)
    return {'paths': paths}


def parse_paths(paths):
    for path in paths['paths']:
        for i in range(len(path)):
            element = path[i]
            if i % 2 == 0:
                element['type'] = element.pop('labels')
            else:
                element['label'] = element.pop('type')
                element['from'] = element.pop('startNode')
                element['to'] = element.pop('endNode')
                element['arrows'] = "to"
                element['dashes'] = False


def respostajson_visjs(response, return_path=False, **kwargs):
    usuario = session.get('usuario', "dummy")
    sessionid = request.cookies.get('session')
    _log_response(usuario, sessionid, response)
    dados = response.json()
    if isinstance(dados, dict):
        dados.update(kwargs)
    if resposta_sensivel(dados):
        dados = remove_info_sensiveis(dados)
    if return_path:
        paths = get_path(deepcopy(dados))
        parse_paths(paths)
        kwargs.update(paths)

    json_visjs = parse_json_to_visjs(dados, **kwargs)

    return jsonify(json_visjs)


def limpa_nos(nos):
    copia_nos = deepcopy(nos)
    for no in copia_nos:
        if ('sensivel' in no['properties'].keys() and
                no['properties']['sensivel'] == '1'):
            no['labels'] = ['sigiloso']
            no['properties'] = dict()

    return copia_nos


# def limpa_linhas(linhas):
#     copia_linhas = deepcopy(linhas)
#     novas_linhas = []
#     for linha in copia_linhas:
#         if isinstance(linha, list):
#             novas_linhas.append(limpa_linhas(linha))
#         elif isinstance(linha, dict):
#             if 'sensivel' in linha.keys():
#                 novas_linhas.append(dict())
#             else:
#                 novas_linhas.append(linha)

#     return novas_linhas


def limpa_relacoes(relacoes):
    copia_relacoes = deepcopy(relacoes)
    for relacao in copia_relacoes:
        if ('sensivel' in relacao['properties'].keys()
                and relacao['properties']['sensivel'] == '1'):
            relacao['type'] = 'sigiloso'
            relacao['properties'] = dict()

    return copia_relacoes


def remove_info_sensiveis(resposta):
    resp = deepcopy(resposta)
    for data in resp['results'][0]['data']:
        data['graph']['nodes'] = limpa_nos(data['graph']['nodes'])
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


def conta_expansoes(n_id, rel_types=''):
    query = {"statements": [{
        "statement": "MATCH r = (n)-[%s*..1]-(x) where id(n) = %s"
        " return count(r), count(n), count(x)" % (rel_types, n_id),
    }]}

    response = requests.post(
        _ENDERECO_NEO4J % '/db/data/transaction/commit',
        data=json.dumps(query),
        auth=_AUTH,
        headers=_HEADERS)

    return response.json()['results'][0]['data'][0]['row']


def resposta_sensivel(resposta):
    return resposta
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
    _LOG_NEO4J.insert(
        {
            'usuario': usuario,
            'datahora': datetime.now(),
            'sessionid': sessionid,
            'resposta': response.json(),
            'ip': request.remote_addr
        }
    )


def _log_login(usuario, motivo, sucesso):
    _LOG_LOGIN.insert(
        {
            "usuario": usuario,
            "motivo": motivo,
            "sucesso": sucesso,
            "ip": request.remote_addr
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
        _log_login(usuario, 'senhaok', True)
        response = sessao.get(url=_USERINFO_MPRJ)
        permissoes = json.loads(
            response.content.decode('utf-8'))['permissions']

        if 'ROLE_Conexao' in permissoes and permissoes['ROLE_Conexao']:
            _log_login(usuario, 'roleok', True)
            return usuario
        else:
            _log_login(usuario, 'rolenok', False)
    else:
        _log_login(usuario, 'senhanok', False)

    return None


def naocompleia(funcao):
    @wraps(funcao)
    def wrapper(*args, **kwargs):
        request.check_compliance = False
        return funcao(*args, **kwargs)
    return wrapper


def login_necessario(funcao):
    @wraps(funcao)
    def funcao_decorada(*args, **kwargs):
        def _(item, lista): return lista.pop(item) if item in lista else None
        if "usuario" not in session:
            return "Não autorizado", 403
        if request.check_compliance:
            if "ultimoacesso" not in session or\
                    (datetime.now() - session["ultimoacesso"]).seconds > 60*30:
                _("ultimoacesso", session)
                _("tipoacesso", session)
                _("numeroprocedimento", session)

                return "Tempo de Compliance expirado", 401
        session["ultimoacesso"] = datetime.now()
        return funcao(*args, **kwargs)
    return funcao_decorada


@app.route("/compliance", methods=["POST"])
@naocompleia
@login_necessario
def compliance():
    tipoacesso = request.form.get("tipoacesso")
    numeroprocedimento = request.form.get("numeroprocedimento")
    descricao = request.form.get("descricao")

    session["ultimoacesso"] = datetime.now()
    session["numeroprocedimento"] = numeroprocedimento
    session["tipoacesso"] = tipoacesso

    _LOG_ACESSO.insert(
        {
            "usuario": session["usuario"],
            "tipoacesso": tipoacesso,
            "numeroprocedimento": numeroprocedimento,
            "descricao": descricao,
            "ip": request.remote_addr
        }
    )

    return "OK", 200


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
        session.clear()
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
        "resultDataContents": ["graph"]
    }]}

    response = requests.post(
        _ENDERECO_NEO4J % '/db/data/transaction/commit',
        data=json.dumps(query),
        auth=_AUTH,
        headers=_HEADERS)

    return respostajson_visjs(response)


@app.route("/api/findShortestPath")
@login_necessario
def api_findShortestPath():
    label1 = request.args.get('label1')
    label2 = request.args.get('label2')
    id_start = request.args.get('node_uuid1')
    id_end = request.args.get('node_uuid2')
    rel_types = request.args.get('rel_types', '')
    if rel_types:
        rel_types = ':' + rel_types.replace(',', '|:')

    query = {"statements": [{
        "statement": "MATCH p = allShortestPaths((a:%s)-[%s*]-(b:%s))"
        " WHERE a.uuid = '%s' AND b.uuid = '%s' RETURN p"
        % (label1, rel_types, label2, id_start, id_end),
        "resultDataContents": ["row", "graph"]
    }]}

    response = requests.post(
        _ENDERECO_NEO4J % '/db/data/transaction/commit',
        data=json.dumps(query),
        auth=_AUTH,
        headers=_HEADERS)

    return respostajson_visjs(response, return_path=True)


def _monta_query_filtro_opcional(label, prop, val, letra):
    if prop == 'pess_dk':
        return "optional match (%s:%s {%s:%s})" % (
            letra,
            label,
            prop,
            val
        )
    elif prop == 'uuid':
        return "optional match (%s:%s {%s:'%s'})" % (
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

    for label, prop, val, letra in zip(plabel, pprop, pval, letras):
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
        'resultDataContents': ['graph']
    }]}

    response = requests.post(
        _ENDERECO_NEO4J % '/db/data/transaction/commit',
        data=json.dumps(query),
        auth=_AUTH,
        headers=_HEADERS)

    numero_de_nos = conta_nos(opcoes, letras)

    node_id = get_node_id(response.json())

    # Call asynchronously tasks
    person_infos = person_info(node_id)
    vehicle_infos = vehicle_info(node_id)

    get_person_photo_asynch.delay(person_infos)
    get_vehicle_photo_asynch.delay(vehicle_infos)

    return respostajson_visjs(response, numero_de_nos=numero_de_nos)


@app.route("/api/nextNodes")
@login_necessario
def api_nextNodes():
    node_id = request.args.get('node_id')
    rel_types = request.args.get('rel_types', '')
    if rel_types:
        rel_types = ':' + rel_types.replace(',', '|:')

    parameters = {
        'where': 'id(n) = {id}'.format(id=node_id),
        'relation_type': rel_types,
        'path_size': 1,
        'limit': 'limit 100',
        'node_type': ''
    }
    response = find_next_nodes(parameters)

    numero_expansoes = conta_expansoes(node_id, rel_types)

    # Call tasks asynchronously
    person_infos = person_info(node_id)
    vehicle_infos = vehicle_info(node_id)

    get_person_photo_asynch.delay(person_infos)
    get_vehicle_photo_asynch.delay(vehicle_infos)
    return respostajson_visjs(response, numero_de_expansoes=numero_expansoes)


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


@app.route("/api/whereaboutsCredilink")
@login_necessario
def api_whereabouts_credilink():
    uuid = request.args.get('uuid')

    query = {"statements": [{
        "statement": "MATCH (p:Pessoa) WHERE p.uuid = '%s' RETURN p"
        % (uuid),
        "resultDataContents": ["row", "graph"]
    }]}

    response = requests.post(
        _ENDERECO_NEO4J % '/db/data/transaction/commit',
        data=json.dumps(query),
        auth=_AUTH,
        headers=_HEADERS)

    response = remove_info_sensiveis(response.json())

    node_props = response['results'][0]['data'][0]['graph'][
        'nodes'][0]['properties']
    # If information is confidential, properties will be empty
    if node_props:
        num_cpf = node_props['num_cpf']
    else:
        return jsonify({})

    whereabouts_credilink = get_whereabouts_credilink(num_cpf)

    return jsonify(whereabouts_credilink)


@app.route("/api/whereaboutsReceita")
@login_necessario
def api_whereabouts_receita():
    uuid = request.args.get('uuid')

    query = {"statements": [{
        "statement": "MATCH (p:Pessoa) WHERE p.uuid = '%s' RETURN p"
        % (uuid),
        "resultDataContents": ["row", "graph"]
    }]}

    response = requests.post(
        _ENDERECO_NEO4J % '/db/data/transaction/commit',
        data=json.dumps(query),
        auth=_AUTH,
        headers=_HEADERS)

    response = remove_info_sensiveis(response.json())

    node_props = response['results'][0]['data'][0]['graph'][
        'nodes'][0]['properties']
    # If information is confidential, properties will be empty
    if node_props:
        num_cpf = node_props['num_cpf']
    else:
        return jsonify({})

    whereabouts_receita = get_whereabouts_receita(num_cpf)

    return jsonify(whereabouts_receita)


@app.context_processor
def mensagens_processor():
    def mensagens():
        try:
            return session.pop('flask_msg')
        except KeyError:
            return ''
    return dict(flask_msg=mensagens)

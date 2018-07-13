import base64
import json
import requests

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
)


def respostajson(response):
    usuario = session.get('usuario', "dummy")
    sessionid = request.cookies.get('session')
    _log_response(usuario, sessionid, response)
    return jsonify(response.json())


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
        # TODO: implementar a restrição por grupo do SCA
        # response = sessao.get(url=_USERINFO_MPRJ)
        # json.loads(response.content.decode('utf-8'))
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
            return redirect(url_for(request.args.get('next', 'raiz')))

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

    return redirect(url_for('login'), code=302)


@app.route("/")
def raiz():
    if 'usuario' not in session:
        return redirect(url_for('login', next=request.endpoint), code=302)
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


@app.route("/api/findNodes")
@login_necessario
def api_findNodes():
    label = request.args.get('label')
    prop = request.args.get('prop')
    val = request.args.get('val')
    # TODO: alterar para prepared statement
    query = {"statements": [{
        "statement": "MATCH (n: %s { %s:toUpper('%s')}) "
        "return n" % (label, prop, val),
        "resultDataContents": ["row", "graph"]
    }]}
    response = requests.post(
        _ENDERECO_NEO4J % '/db/data/transaction/commit',
        data=json.dumps(query),
        auth=_AUTH,
        headers=_HEADERS)
    return respostajson(response)


@app.route("/api/nextNodes")
@login_necessario
def api_nextNodes():
    node_id = request.args.get('node_id')
    query = {"statements": [{
        "statement": "MATCH r = (n)-[*..1]-(x) where id(n) = %s "
        "return r,n,x" % node_id,
        "resultDataContents": ["row", "graph"]
    }]}
    response = requests.post(
        _ENDERECO_NEO4J % '/db/data/transaction/commit',
        data=json.dumps(query),
        auth=_AUTH,
        headers=_HEADERS)
    return respostajson(response)


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

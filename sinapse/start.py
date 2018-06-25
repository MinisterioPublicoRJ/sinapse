from datetime import datetime
from flask import (
    Flask,
    jsonify,
    request,
    send_from_directory,
    render_template,
    session,
    Session
)
import requests
import json
from sinapse.buildup import (
    app,
    _LOG_MONGO,
    HTTPBasicAuth,
    _ENDERECO_NEO4J,
    _AUTH,
    _HEADERS
)



def respostajson(usuario, sessionid, response):
    _log_response(usuario, sessionid, response)
    return jsonify(response.json())


def _log_response(usuario, sessionid, response):
    _LOG_MONGO.insert(
        {
            'usuario': usuario,
            'datahora': datetime.date(),
            'sessionid': sessionid,
            'resposta': response.json()
        }
    )

@app.route("/")
def raiz():
    return render_template('index.html')


@app.route("/api/node")
def api_node():
    node_id = request.args.get('node_id')

    query  = { "statements" : [ { "statement" : "MATCH  (n) where id(n) = "+ node_id +" return n", "resultDataContents" : [ "row", "graph" ] } ] }
    response = requests.post(_ENDERECO_NEO4J % '/db/data/transaction/commit', data=json.dumps(query), auth=_AUTH, headers=_HEADERS)
    return respostajson()


@app.route("/api/findNodes")
def api_findNodes():
    label = request.args.get('label')
    prop = request.args.get('prop')
    val = request.args.get('val')

    query  = { "statements" : [ { "statement" : "MATCH (n:"+ label +" {"+ prop +":toUpper('"+ val +"')}) return n", "resultDataContents" : [ "row", "graph" ] } ] }
    response = requests.post(_ENDERECO_NEO4J % '/db/data/transaction/commit', data=json.dumps(query), auth=_AUTH, headers=_HEADERS)
    return jsonify(response.json())


@app.route("/api/nextNodes")
def api_nextNodes():
    node_id = request.args.get('node_id')
    query  = { "statements" : [ { "statement" : "MATCH r = (n)-[*..1]-(x) where id(n) = "+ node_id +" return r,n,x", "resultDataContents" : [ "row", "graph" ] } ] }
    response = requests.post(_ENDERECO_NEO4J % '/db/data/transaction/commit', data=json.dumps(query), auth=_AUTH, headers=_HEADERS)
    return jsonify(response.json())    


@app.route("/api/nodeProperties")
def api_nodeProperties():
    label = request.args.get('label')

    cypher = "MATCH (n:"+ label +")  RETURN  keys(n) limit 1"
    query = { "query" : cypher }
    response = requests.post(_ENDERECO_NEO4J % '/db/data/cypher', data=json.dumps(query), auth=_AUTH, headers=_HEADERS)
    return jsonify(response.json())

@app.route("/api/labels")
def api_labels():
    response = requests.get(_ENDERECO_NEO4J % '/db/data/labels', auth=_AUTH, headers=_HEADERS)
    return jsonify(response.json())


@app.route("/api/relationships")
def api_relationships():
    response = requests.get(_ENDERECO_NEO4J % '/db/data/relationship/types', auth=_AUTH, headers=_HEADERS)
    return jsonify(response.json())

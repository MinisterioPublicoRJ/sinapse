from flask import Flask, jsonify, request, send_from_directory, render_template
import requests
from requests.auth import HTTPBasicAuth
import json
from decouple import config


app = Flask(__name__)
_AUTH = HTTPBasicAuth(config('NEO4J_USUARIO'), config('NEO4J_SENHA'))
_ENDERECO_NEO4J = config('NEO4J_DOMINIO') + '%s'
_HEADERS = {'content-type': 'application/json'}

@app.route("/")
def raiz():
    return render_template('index.html')


@app.route("/api/node")
def api_node():
    node_id = request.args.get('node_id')

    query  = { "statements" : [ { "statement" : "MATCH  (n) where id(n) = "+ node_id +" return n", "resultDataContents" : [ "row", "graph" ] } ] }
    response = requests.post(_ENDERECO_NEO4J % '/db/data/transaction/commit', data=json.dumps(query), auth=_AUTH, headers=_HEADERS)
    return jsonify(response.json())    


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

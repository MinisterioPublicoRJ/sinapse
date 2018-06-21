from flask import Flask, jsonify, request, send_from_directory, render_template
import requests
from requests.auth import HTTPBasicAuth
import json
from decouple import config


app = Flask(__name__)
_AUTH = HTTPBasicAuth(config('NEO4J_USUARIO'), config('NEO4J_SENHA'))
_ENDERECO_NEO4J = config('NEO4J_DOMINIO') + '%s'


print(_AUTH)
print(_ENDERECO_NEO4J)


@app.route("/")
def raiz():
    return render_template('index.html')


@app.route("/api/node")
def api_node():
    node_id = request.args.get('node_id')

    #cypher = "MATCH  (n) where id(n) = "+ node_id +" return n"
    #query = { "query" : cypher }
    query  = { "statements" : [ { "statement" : "MATCH  (n) where id(n) = "+ node_id +" return n", "resultDataContents" : [ "row", "graph" ] } ] }
    _headers = {'content-type': 'application/json'}
    #response = requests.post('http://neo4j.cloud.mprj.mp.br/db/data/cypher', data=json.dumps(query), auth=_AUTH, headers=_headers)
    response = requests.post(_ENDERECO_NEO4J % '/db/data/transaction/commit', data=json.dumps(query), auth=_AUTH, headers=_headers)
    return jsonify(response.json())    


@app.route("/api/findNodes")
def api_findNodes():
    label = request.args.get('label')
    prop = request.args.get('prop')
    val = request.args.get('val')

    #cypher = "MATCH (n:"+ label +" {"+ prop +":toUpper('"+ val +"')}) return n"
    #query = { "query" : cypher }
    query  = { "statements" : [ { "statement" : "MATCH (n:"+ label +" {"+ prop +":toUpper('"+ val +"')}) return n", "resultDataContents" : [ "row", "graph" ] } ] }
    _headers = {'content-type': 'application/json'}
    #response = requests.post('http://neo4j.cloud.mprj.mp.br/db/data/cypher', data=json.dumps(query), auth=_AUTH, headers=_headers)
    response = requests.post(_ENDERECO_NEO4J % '/db/data/transaction/commit', data=json.dumps(query), auth=_AUTH, headers=_headers)
    return jsonify(response.json())


@app.route("/api/nextNodes")
def api_nextNodes():
    node_id = request.args.get('node_id')
    query  = { "statements" : [ { "statement" : "MATCH r = (n)-[*..1]-(x) where id(n) = "+ node_id +" return r,n,x", "resultDataContents" : [ "row", "graph" ] } ] }
    _headers = {'content-type': 'application/json'}
    response = requests.post(_ENDERECO_NEO4J % '/db/data/transaction/commit', data=json.dumps(query), auth=_AUTH, headers=_headers)
    return jsonify(response.json())    


@app.route("/api/nodeProperties")
def api_nodeProperties():
    label = request.args.get('label')

    cypher = "MATCH (n:"+ label +")  RETURN  keys(n) limit 1"
    query = { "query" : cypher }
    _headers = {'content-type': 'application/json'}
    response = requests.post(_ENDERECO_NEO4J % '/db/data/cypher', data=json.dumps(query), auth=_AUTH, headers=_headers)
    return jsonify(response.json())



@app.route("/api/nextNodes2")
def api_nextNodes2():
    query  = { "statements" : [ { "statement" : "MATCH r = (n)-[*..1]-(x) where id(n) = 140885160 return r,n,x", "resultDataContents" : [ "row", "graph" ] } ] }
    _headers = {'content-type': 'application/json'}
    response = requests.post(_ENDERECO_NEO4J % '/db/data/transaction/commit', data=json.dumps(query), auth=_AUTH, headers=_headers)
    return jsonify(response.json())        
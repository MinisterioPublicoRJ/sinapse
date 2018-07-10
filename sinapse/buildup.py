from decouple import config
from flask import Flask
from pymongo import MongoClient
from requests.auth import HTTPBasicAuth


app = Flask("sinapse")
app.secret_key = config('SECRET')
app.jinja_env.auto_reload = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['TEMPLATES_AUTO_RELOAD'] = True

_AUTH = HTTPBasicAuth(config('NEO4J_USUARIO'), config('NEO4J_SENHA'))
_ENDERECO_NEO4J = config('NEO4J_DOMINIO') + '%s'
_HEADERS = {'content-type': 'application/json'}

_USUARIO_MONGO = config('MONGO_USUARIO')
_SENHA_MONGO = config('MONGO_SENHA')
_HOST_MONGO = config('MONGO_HOST')
_AUTHDB_MONGO = config('MONGO_AUTHDB')

_MONGO_CLIENT = MongoClient(
    _HOST_MONGO,
    27017,
    username=_USUARIO_MONGO,
    password=_SENHA_MONGO,
    authSource=_AUTHDB_MONGO
)

_LOG_MONGO = _MONGO_CLIENT.mmps.log_sinapse
_AUTH_MPRJ = config('AUTH_MPRJ')
_USERINFO_MPRJ = config('USERINFO_MPRJ')

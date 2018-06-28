from functools import wraps
import json
import unittest
import responses
from unittest import mock
from sinapse.start import (
    app,
    _autenticar,
    _AUTH_MPRJ,
    _ENDERECO_NEO4J
)
from .fixtures import (
    request_node_ok,
    resposta_node_ok,
    request_filterNodes_ok,
    resposta_filterNodes_ok
)


class CasoGlobal(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_raiz(self):
        resposta = self.app.get('/')

        assert resposta.status_code == 200

    def test_api_authorization(self):
        api_node = self.app.get('/api/node')
        api_findNodes = self.app.get('/api/findNodes')
        api_nextNodes = self.app.get('/api/nextNodes')
        api_nodeProperties = self.app.get('/api/nodeProperties')
        api_relationships = self.app.get('/api/relationships')

        assert api_node.status_code == 403
        assert api_findNodes.status_code == 403
        assert api_nextNodes.status_code == 403
        assert api_nodeProperties.status_code == 403
        assert api_relationships.status_code == 403

    @responses.activate
    def test_autenticar_invalido(self):
        responses.add(
            responses.POST,
            _AUTH_MPRJ,
            status=403
        )

        retorno = _autenticar("usuario", "senha")
        assert retorno is None

    @responses.activate
    def test_autenticar(self):
        responses.add(
            responses.POST,
            _AUTH_MPRJ,
            status=200
        )

        retorno = _autenticar("usuario", "senha")
        assert retorno == "usuario"


class LoginUsuario(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    @responses.activate
    @mock.patch("sinapse.start._log_response")
    @mock.patch("sinapse.start._autenticar")
    def test_login(self, _autenticar, _log_response):
        retorno_esperado = {"saida": "dados"}
        _autenticar.side_effect = ["usuario"]

        retorno = self.app.post(
            "/login",
            data={
                "usuario": "usuario",
                "senha": "senha"})

        assert retorno.status_code == 201

        responses.add(
            responses.POST,
            _ENDERECO_NEO4J % '/db/data/transaction/commit',
            json=retorno_esperado
        )

        resposta = self.app.get("/api/node?node_id=10")
        assert resposta.get_json() == retorno_esperado
        assert _log_response.call_count == 1

    @mock.patch('sinapse.start._autenticar', return_value=None)
    def test_falha_login(self, _autenticar):
        retorno = self.app.post(
            "/login",
            data={
                "usuario": "usuario",
                "senha": "senha"
            }
        )

        assert retorno.status_code == 401


def logresponse(funcao):
    @mock.patch("sinapse.start._log_response")
    @responses.activate
    @wraps(funcao)
    def wrapper(*args, **kwargs):
        # remove o _log_response da lista de argumentos
        args = list(args)
        args.pop(-1)
        return funcao(*args, **kwargs)

    return wrapper


class MetodosConsulta(unittest.TestCase):
    @mock.patch("sinapse.start._autenticar")
    def setUp(self, _autenticar):
        self.app = app.test_client()
        _autenticar.side_effect = ["usuario"]

        self.app.post(
            "/login",
            data={
                "usuario": "usuario",
                "senha": "senha"})

    @logresponse
    def test_api_node(self):
        responses.add(
            responses.POST,
            _ENDERECO_NEO4J % '/db/data/transaction/commit',
            json=resposta_node_ok
        )

        resposta = self.app.get("/api/node?node_id=395989945")

        assert resposta.get_json() == resposta_node_ok
        assert json.loads(responses.calls[0].request.body) == request_node_ok

    @logresponse
    def test_api_findNodes(self):
        responses.add(
            responses.POST,
            _ENDERECO_NEO4J % '/db/data/transaction/commit',
            json=resposta_filterNodes_ok
        )

        resposta = self.app.get(
            "/api/findNodes",
            query_string={
                'label': 'pessoa',
                'prop': 'nome',
                'val': 'DANIEL CARVALHO BELCHIOR'
            }
        )

        assert resposta.get_json() == resposta_filterNodes_ok
        assert json.loads(
            responses.calls[0].request.body) == request_filterNodes_ok

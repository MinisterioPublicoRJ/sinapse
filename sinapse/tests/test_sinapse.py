import unittest
import responses
from unittest import mock
# from sinapse.buildup import (
#     _AUTH,
#     _HEADERS
# )
from sinapse.start import (
    app,
    _autenticar,
    _AUTH_MPRJ,
    _ENDERECO_NEO4J
)


class CasoGlobal(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_raiz(self):
        resposta = self.app.get('/')

        assert resposta.status_code == 200

    # def itest_api_node(self):
    #     _post.assert_called_once_with(
    #         'http://neo4j.cloud.mprj.mp.br/db/data/transaction/commit',
    #         data=('{"statements": [{"statement": "MATCH  (n) where id(n) = 1'
    #               ' return n", "resultDataContents": ["row", "graph"]}]}'),
    #         auth=_AUTH,
    #         headers=_HEADERS
    #     )

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


class LogoutUsuario(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    @mock.patch("sinapse.start._autenticar")
    def test_logout(self, _autenticar):
        _autenticar.side_effect = ["usuario"]
        # Loga usuario
        self.app.post(
            "/login",
            data={
                "usuario": "usuario",
                "senha": "senha"})

        retorno = self.app.get(
            "/logout",
        )

        assert retorno.status_code == 201
        assert retorno.data == b'OK'

    def test_logout_usuario_nao_logado(self):
        retorno = self.app.get("/logout")

        assert retorno.status_code == 200
        assert retorno.data == 'Usuário não logado'.encode('utf-8')

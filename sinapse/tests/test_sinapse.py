import json
import responses
import unittest

from functools import wraps
from unittest import mock

from freezegun import freeze_time
from freezegun.api import FakeDatetime
from sinapse.start import (
    app,
    _autenticar,
    _AUTH_MPRJ,
    _ENDERECO_NEO4J,
    _log_response
)

from .fixtures import casos_servicos


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


@mock.patch("sinapse.start._LOG_MONGO")
def test_log_response(_log_mongo):
    response = mock.Mock()
    response.json.side_effect = ["response"]

    with freeze_time("2018-06-28"):
        _log_response("usuario", "1234", response)

    _log_mongo.insert.assert_called_once_with(
        {
            'usuario': 'usuario',
            'datahora': FakeDatetime(2018, 6, 28, 0, 0),
            'sessionid': '1234',
            'resposta': 'response'
        }
    )


class CasoGlobal(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_raiz(self):
        resposta = self.app.get('/')

        assert resposta.status_code == 200

    def test_autorizacao_da_api(self):
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


class MetodosConsulta(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        with mock.patch("sinapse.start._autenticar") as _autenticar:
            _autenticar.side_effect = ["usuario"]
            self.app.post(
                "/login",
                data={
                    "usuario": "usuario",
                    "senha": "senha"})

    @logresponse
    def test_metodos_consulta(self):
        for caso in casos_servicos:
            self._consultar(caso)

    def _consultar(self, caso):
        with self.subTest(caso['nome']):
            responses.add(
                caso['metodo'],
                _ENDERECO_NEO4J % caso['endereco'],
                json=caso['resposta']
            )

            resposta = self.app.get(
                caso['servico'],
                query_string=caso['query_string']
            )

            assert resposta.get_json() == caso['resposta']
            if caso['query_string']:
                assert json.loads(
                    responses.calls[-1].request.body) == caso['requisicao']
            else:
                assert responses.calls[-1].request.body is None

            responses.remove(
                caso['metodo'],
                _ENDERECO_NEO4J % caso['endereco']
            )

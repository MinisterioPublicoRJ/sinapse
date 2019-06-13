import json
import responses
import unittest

from freezegun import freeze_time
from copy import deepcopy
from functools import wraps
from unittest import mock
from datetime import datetime

from flask_testing import TestCase as FlaskTestCase
from freezegun.api import FakeDatetime
from sinapse.start import (
    app,
    _autenticar,
    _AUTH_MPRJ,
    _ENDERECO_NEO4J,
    _log_response,
    limpa_nos,
    remove_info_sensiveis,
    resposta_sensivel,
    limpa_relacoes,
    conta_nos,
    conta_expansoes,
    _monta_query_filtro_opcional,
    _USERINFO_MPRJ,
    parse_json_to_visjs,
    get_path,
    parse_paths
)

from .fixtures import (
    resposta_node_sensivel_ok,
    nos_sensiveis_esp,
    resposta_node_sensivel_esp,
    resposta_node_ok,
    request_node_ok,
    resposta_sensivel_mista,
    resposta_sensivel_mista_esp,
    relacoes_sensiveis,
    relacoes_sensiveis_esp,
    request_filterNodes_ok,
    resposta_filterNodes_ok,
    resposta_nextNodes_ok,
    request_nextNodes_ok,
    request_nextNodes_umfiltro_ok,
    request_nextNodes_doisfiltros_ok,
    resposta_findShortestPath_ok,
    request_findShortestPath_umfiltro_ok,
    request_findShortestPath_doisfiltros_ok,
    request_findShortestPath_ok,
    resposta_nodeproperties_ok,
    request_nodeproperties_ok,
    resposta_label_ok,
    resposta_relationships_ok,
    query_dinamica,
    parser_test_input,
    parser_test_output,
    get_path_input,
    get_path_output,
    parse_path_input,
    parse_path_output
)


def test_parser_visjs():
    saida = parse_json_to_visjs(parser_test_input)
    assert saida == parser_test_output


def test_get_path():
    saida = get_path(get_path_input)
    assert saida == get_path_output

def test_parse_path():
    input_copy = deepcopy(parse_path_input)
    parse_paths(input_copy)
    assert input_copy == parse_path_output


def test_monta_query_filtro_opcional():
    saida = _monta_query_filtro_opcional(
        'label',
        'prop',
        'val',
        'a'
    )

    assert saida == "optional match (a:label {prop:toUpper('val')})"


def test_monta_query_filtro_opcional_pessdk():
    saida = _monta_query_filtro_opcional(
        'label',
        'pess_dk',
        'val',
        'a'
    )

    assert saida == "optional match (a:label {pess_dk:val})"

@mock.patch("sinapse.start._log_login")
@responses.activate
def test_autenticar_invalido(_LOG_LOGIN):
    responses.add(
        responses.POST,
        _AUTH_MPRJ,
        status=403
    )

    retorno = _autenticar("usuario", "senha")
    assert retorno is None

@mock.patch("sinapse.start._log_login")
@responses.activate
def test_autenticar(_LOG_LOGIN):
    responses.add(
        responses.POST,
        _AUTH_MPRJ,
        status=200
    )
    responses.add(
        responses.GET,
        _USERINFO_MPRJ,
        status=200,
        json={'permissions': {'ROLE_Conexao': True}}
    )

    retorno = _autenticar("usuario", "senha")
    assert retorno == "usuario"


def mock_logresponse(funcao):
    @mock.patch("sinapse.start._log_response")
    @responses.activate
    @wraps(funcao)
    def wrapper(*args, **kwargs):
        # remove o _log_response da lista de argumentos
        args = list(args)
        for arg in list(args):
            if arg.__dict__.get('_mock_name', '') == '_log_response':
                args.remove(arg)
        return funcao(*args, **kwargs)

    return wrapper


@mock.patch("sinapse.start._LOG_NEO4J")
@mock.patch("sinapse.start.request")
def test_log_response(request, _log_mongo):
    response = mock.Mock()
    response.json.side_effect = ["response"]
    request.remote_addr = '192.168.0.1'

    with freeze_time("2018-06-28"):
        _log_response("usuario", "1234", response)

    _log_mongo.insert.assert_called_once_with(
        {
            'usuario': 'usuario',
            'datahora': FakeDatetime(2018, 6, 28, 0, 0),
            'sessionid': '1234',
            'resposta': 'response',
            'ip': '192.168.0.1'
        }
    )


class CasoGlobal(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_raiz(self):
        resposta = self.app.get('/')

        assert resposta.status_code == 302

    @mock.patch('sinapse.start.vehicle_info')
    @mock.patch('sinapse.start.person_info')
    @mock.patch('sinapse.start.get_vehicle_photo_asynch')
    @mock.patch('sinapse.start.get_person_photo_asynch')
    def test_autorizacao_da_api(self, _gpa, _gva, _pi, _vi):
        api_node = self.app.get('/api/node')
        api_findNodes = self.app.get('/api/findNodes')
        api_nextNodes = self.app.get('/api/nextNodes')
        api_nodeProperties = self.app.get('/api/nodeProperties')
        api_relationships = self.app.get('/api/relationships')
        api_findShortestPath = self.app.get('/api/findShortestPath')
        api_whereabouts = self.app.get('/api/whereabouts')

        assert api_node.status_code == 403
        assert api_findNodes.status_code == 403
        assert api_nextNodes.status_code == 403
        assert api_nodeProperties.status_code == 403
        assert api_relationships.status_code == 403
        assert api_findShortestPath.status_code == 403
        assert api_whereabouts.status_code == 403


class LoginUsuario(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    @responses.activate
    @mock.patch("sinapse.start._LOG_ACESSO")
    @mock.patch("sinapse.start._log_response")
    @mock.patch("sinapse.start._autenticar")
    def test_login(self, _autenticar, _log_response, _LOG_ACESSO):
        retorno_esperado = {"saida": "dados"}
        _autenticar.side_effect = ["usuario"]

        retorno = self.app.post(
            "/login",
            data={
                "usuario": "usuario",
                "senha": "senha"
                })
        retorno_compliance = self.app.post(
            "/compliance",
            data={
                "tipoacesso": 1,
                "numeroprocedimento": 1,
                "descricao": 1
            })

        assert retorno.status_code == 302
        assert retorno_compliance.status_code == 200

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
        assert 'Falha no login' in retorno.data.decode('utf-8')


class MetodosConsulta(unittest.TestCase):
    @mock.patch("sinapse.start._LOG_ACESSO")
    def setUp(self, _LOG_ACESSO):
        self.app = app.test_client()
        with mock.patch("sinapse.start._autenticar") as _autenticar:
            _autenticar.side_effect = ["usuario"]
            self.app.post(
                "/login",
                data={
                    "usuario": "usuario",
                    "senha": "senha"
                }
            )
            self.app.post("/compliance",
                data={
                    "tipoacesso": 1,
                    "numeroprocedimento": 1,
                    "descricao": 1
                })

    @mock.patch('sinapse.start.conta_nos')
    @mock.patch('sinapse.start.get_vehicle_photo_asynch')
    @mock.patch('sinapse.start.get_person_photo_asynch')
    @mock_logresponse
    def test_monta_query_dinamica(self, _gpa, _gva, _conta_nos):
        _conta_nos.return_value = 10
        _gpa.__name__ = 'Response'
        query_string = {
            'label': 'Pessoa,Personagem',
            'prop': 'nome,pess_dk',
            'val': 'DANIEL CARVALHO BELCHIOR,24728287'
        }

        responses.add(
            responses.POST,
            _ENDERECO_NEO4J % '/db/data/transaction/commit',
            json=resposta_sensivel_mista_esp
        )

        resposta = self.app.get(
            '/api/findNodes',
            query_string=query_string
        )

        assert resposta.status_code == 200

        statements = json.loads(responses.calls[0].request.body)
        assert statements['statements'] == query_dinamica

    @mock_logresponse
    def test_metodo_consulta_api_node(self):
        responses.add(
            responses.POST,
            _ENDERECO_NEO4J % '/db/data/transaction/commit',
            json=resposta_node_ok
        )
        response = self.app.get(
            'api/node',
            query_string={'node_id': 395989945}
        )

        expected_response = parse_json_to_visjs(deepcopy(resposta_node_ok))
        self.assertEqual(response.get_json(), expected_response)
        self.assertEqual(
            json.loads(responses.calls[-1].request.body),
            request_node_ok
        )

    @mock_logresponse
    def test_metodo_consulta_api_find_shortest_path(self):
        responses.add(
            responses.POST,
            _ENDERECO_NEO4J % '/db/data/transaction/commit',
            json=resposta_findShortestPath_ok
        )
        response = self.app.get(
            'api/findShortestPath',
            query_string={
                "label1": 'Pessoa',
                "label2": 'Pessoa',
                "node_uuid1": '123abc',
                "node_uuid2": '234bcd'
            }
        )
        expected_response = deepcopy(
            parse_json_to_visjs(resposta_findShortestPath_ok))
        expected_response.update(get_path_output)
        parse_paths(expected_response)

        for edge in response.get_json()['edges']:
            assert edge in expected_response['edges']
        for node in response.get_json()['nodes']:
            assert node in expected_response['nodes']
        for path in response.get_json()['paths']:
            assert path in expected_response['paths']
        self.assertEqual(
            json.loads(responses.calls[-1].request.body),
            request_findShortestPath_ok
        )

    @mock_logresponse
    def test_metodo_consulta_api_find_shortest_path_one_filter(self):
        responses.add(
            responses.POST,
            _ENDERECO_NEO4J % '/db/data/transaction/commit',
            json=[]
        )
        self.app.get(
            'api/findShortestPath',
            query_string={
                "label1": "Pessoa",
                "label2": "Pessoa",
                "node_uuid1": 140885160,
                "node_uuid2": 328898991,
                "rel_types": "TRABALHA"
            }
        )

        self.assertEqual(
            json.loads(responses.calls[-1].request.body),
            request_findShortestPath_umfiltro_ok
        )

    @mock_logresponse
    def test_metodo_consulta_api_find_shortest_path_two_filters(self):
        responses.add(
            responses.POST,
            _ENDERECO_NEO4J % '/db/data/transaction/commit',
            json=[]
        )
        self.app.get(
            'api/findShortestPath',
            query_string={
                "label1": "Pessoa",
                "label2": "Pessoa",
                "node_uuid1": 140885160,
                "node_uuid2": 328898991,
                "rel_types": "FILHO,PERSONAGEM"
            }
        )
        self.maxDiff = None
        self.assertEqual(
            json.loads(responses.calls[-1].request.body),
            request_findShortestPath_doisfiltros_ok
        )

    @mock.patch('sinapse.start.get_vehicle_photo_asynch')
    @mock.patch('sinapse.start.get_person_photo_asynch')
    @mock.patch('sinapse.start.vehicle_info')
    @mock.patch('sinapse.start.person_info')
    @mock.patch('sinapse.start.conta_expansoes')
    @mock_logresponse
    def test_metodo_consulta_api_next_nodes(self, _conta_expansoes, _pi, _vi, _gpa, _gva):
        _conta_expansoes.return_value = [73, 73, 73]
        _pi.return_value = 1
        _vi.return_vale = 1
        _gpa.return_value = None
        _gva.return_value = None
        responses.add(
            responses.POST,
            _ENDERECO_NEO4J % '/db/data/transaction/commit',
            json=resposta_nextNodes_ok
        )
        response = self.app.get(
            'api/nextNodes',
            query_string={
                'node_id': 395989945
            }
        )

        expected_response = parse_json_to_visjs(
            deepcopy(resposta_nextNodes_ok)
        )
        expected_response['numero_de_expansoes'] = [73, 73, 73]

        self.assertEqual(response.get_json(), expected_response)
        self.assertEqual(
            json.loads(responses.calls[-1].request.body),
            request_nextNodes_ok
        )

    @mock.patch('sinapse.start.get_vehicle_photo_asynch')
    @mock.patch('sinapse.start.get_person_photo_asynch')
    @mock.patch('sinapse.start.vehicle_info')
    @mock.patch('sinapse.start.person_info')
    @mock.patch('sinapse.start.conta_expansoes')
    @mock_logresponse
    def test_metodo_consulta_api_next_nodes_one_filter(self, _conta_expansoes, _pi, _vi, _gpa, _gva):
        _conta_expansoes.return_value = [73, 73, 73]
        _pi.return_value = None
        _vi.return_value = None
        _gpa.return_value = None
        _gva.return_value = None
        responses.add(
            responses.POST,
            _ENDERECO_NEO4J % '/db/data/transaction/commit',
            json=resposta_nextNodes_ok
        )
    
        self.app.get(
            'api/nextNodes',
            query_string={
                'node_id': 395989945,
                'rel_types': 'FILHO'
            }
        )
        
        self.assertEqual(
            json.loads(responses.calls[-1].request.body),
            request_nextNodes_umfiltro_ok
        )

    @mock.patch('sinapse.start.vehicle_info')
    @mock.patch('sinapse.start.person_info')
    @mock.patch('sinapse.start.conta_expansoes')
    @mock_logresponse
    def test_metodo_consulta_api_next_nodes_two_filters(self,
                                                        _conta_expansoes,
                                                        _pi, _vi):
        _pi.return_value = []
        _vi.return_value = []
        _conta_expansoes.return_value = [73, 73, 73]
        responses.add(
            responses.POST,
            _ENDERECO_NEO4J % '/db/data/transaction/commit',
            json=[]
        )
        self.app.get(
            'api/nextNodes',
            query_string={
                'node_id': 395989945,
                'rel_types': 'FILHO,TRABALHA'
            }
        )

        self.assertEqual(
            json.loads(responses.calls[-1].request.body),
            request_nextNodes_doisfiltros_ok
        )

    @mock_logresponse
    def test_metodo_consulta_api_node_properties(self):
        responses.add(
            responses.POST,
            _ENDERECO_NEO4J % '/db/data/cypher',
            json=resposta_nodeproperties_ok
        )
        response = self.app.get(
            'api/nodeProperties',
            query_string={
                'label': 'Pessoa'
            }
        )

        expected_response = resposta_nodeproperties_ok

        self.assertEqual(response.get_json(), expected_response)
        self.assertEqual(
            json.loads(responses.calls[-1].request.body),
            request_nodeproperties_ok
        )

    @mock_logresponse
    def test_metodo_consulta_api_labels(self):
        responses.add(
            responses.GET,
            _ENDERECO_NEO4J % '/db/data/labels',
            json=resposta_label_ok
        )
        response = self.app.get(
            'api/labels'
        )
        expected_response = resposta_label_ok

        self.assertEqual(response.get_json(), expected_response)

    @mock_logresponse
    def test_metodo_consulta_api_relationships(self):
        responses.add(
            responses.GET,
            _ENDERECO_NEO4J % '/db/data/relationship/types',
            json=resposta_relationships_ok
        )
        response = self.app.get(
            'api/relationships'
        )

        expected_response = resposta_relationships_ok

        self.assertEqual(response.get_json(), expected_response)

    @mock.patch('sinapse.start.vehicle_info')
    @mock.patch('sinapse.start.person_info')
    @mock.patch('sinapse.start.get_vehicle_photo_asynch')
    @mock.patch('sinapse.start.get_person_photo_asynch')
    @mock_logresponse
    def test_resposta_nos(self, _gpa, _gva, _pi, _vi):
        _gpa.__name__ = 'Response'
        responses.add(
            responses.POST,
            _ENDERECO_NEO4J % '/db/data/transaction/commit',
            json=resposta_filterNodes_ok
        )
        resposta_count = {
            'results': [{'data': [{'row': [1]}]}]
        }
        responses.add(
            responses.POST,
            _ENDERECO_NEO4J % '/db/data/transaction/commit',
            json=resposta_count
        )

        query_string = {
            'label': 'Pessoa',
            'prop': 'nome',
            'val': 'DANIEL CARVALHO BELCHIOR'
        }

        resposta = self.app.get(
            '/api/findNodes',
            query_string=query_string
        )
        resposta_esperada = parse_json_to_visjs(
            deepcopy(resposta_filterNodes_ok)
        )
        resposta_esperada['numero_de_nos'] = 1

        self.assertEqual(resposta.get_json(), resposta_esperada)
        self.assertEqual(
            json.loads(responses.calls[-2].request.body),
            request_filterNodes_ok
        )

    @responses.activate
    def test_conta_numero_de_nos(self):
        resp_esperada = {
            'results': [
                {'columns': ['COUNT(p)'],
                 'data': [{'row': [3], 'meta': [None]}]}], 'errors': []
        }
        responses.add(
            responses.POST,
            _ENDERECO_NEO4J % '/db/data/transaction/commit',
            json=resp_esperada
        )

        numero_nos = conta_nos(
            _monta_query_filtro_opcional(
                'Pessoa',
                'nome',
                'Qualquer',
                'a'
            ),
            'a'
        )

        self.assertEqual(numero_nos, 3)

    @mock.patch('sinapse.start.get_vehicle_photo_asynch')
    @mock.patch('sinapse.start.get_person_photo_asynch')
    @mock.patch('sinapse.start.get_node_id', return_value=12345)
    @mock.patch('sinapse.start.conta_nos', return_value=101)
    @mock_logresponse
    def test_conta_numero_de_nos_antes_da_busca(self, _conta_nos, _gni, _gpa,
                                                _gva):
        _gni.__name__ = 'Return'
        _gpa.__name__ = 'Return'
        mock_resposta = mock.MagicMock()
        responses.add(
            responses.POST,
            _ENDERECO_NEO4J % '/db/data/transaction/commit',
            json={}
        )
        responses.add(
            responses.POST,
            _ENDERECO_NEO4J % '/db/data/transaction/commit',
            json=resposta_filterNodes_ok
        )
        query_string = {
            'label': 'Pessoa',
            'prop': 'nome',
            'val': 'Qualquer'
        }

        resposta_esperada = deepcopy(resposta_filterNodes_ok)
        resposta_esperada['numero_de_nos'] = 101
        mock_resposta.json.return_value = resposta_esperada

        resposta = self.app.get(
            '/api/findNodes',
            query_string=query_string
        )

        _conta_nos.assert_called_once_with(
            ["optional match (a:Pessoa {nome:toUpper('Qualquer')})"],
            'a'
        )
        self.assertEqual(resposta.json['numero_de_nos'], 101)

    @mock.patch('sinapse.start.vehicle_info')
    @mock.patch('sinapse.start.person_info')
    @mock.patch('sinapse.start.get_vehicle_photo_asynch')
    @mock.patch('sinapse.start.get_person_photo_asynch')
    @mock_logresponse
    def test_resposta_expansoes(self, _gpa, _gva, _pi, _vi):
        responses.add(
            responses.POST,
            _ENDERECO_NEO4J % '/db/data/transaction/commit',
            json=resposta_nextNodes_ok
        )
        resposta_count = {
            'results': [
                {'columns': ['COUNT(r)', 'COUNT(n)', 'COUNT(x)'],
                 'data': [{'row': [72, 72, 72], 'meta': [None, None, None]}]}],
            'errors': []}

        responses.add(
            responses.POST,
            _ENDERECO_NEO4J % '/db/data/transaction/commit',
            json=resposta_count
        )

        query_string = {
            'node_id': 1234
        }

        resposta = self.app.get(
            '/api/nextNodes',
            query_string=query_string
        )
        resposta_esperada = parse_json_to_visjs(
            deepcopy(resposta_nextNodes_ok)
        )
        resposta_esperada['numero_de_expansoes'] = [72, 72, 72]

        self.assertEqual(resposta.get_json(), resposta_esperada)

    @responses.activate
    def test_conta_numero_de_expansao_de_nos(self):
        resp_esperada = {
            'results': [
                {'columns': ['COUNT(r)', 'COUNT(n)', 'COUNT(x)'],
                 'data': [{'row': [72, 72, 72], 'meta': [None, None, None]}]}],
            'errors': []}
        responses.add(
            responses.POST,
            _ENDERECO_NEO4J % '/db/data/transaction/commit',
            json=resp_esperada
        )

        expansoes = conta_expansoes(n_id=1234)

        self.assertEqual(expansoes, [72, 72, 72])
        self.assertEqual(responses.calls[-1].request.body,
                         '{"statements": [{"statement": "MATCH r ='
                         ' (n)-[*..1]-(x) where id(n) = 1234 return count(r),'
                         ' count(n), count(x)"}]}')

    @mock.patch('sinapse.start.get_vehicle_photo_asynch')
    @mock.patch('sinapse.start.get_person_photo_asynch')
    @mock.patch('sinapse.start.conta_expansoes', return_value=[1, 1, 1])
    @mock_logresponse
    def test_conta_numero_de_expansoes_antes_da_busca(self, _conta_expansoes,
                                                      _gfa, _gva):
        mock_resposta = mock.MagicMock()
        responses.add(
            responses.POST,
            _ENDERECO_NEO4J % '/db/data/transaction/commit',
            json={}
        )
        responses.add(
            responses.POST,
            _ENDERECO_NEO4J % '/db/data/transaction/commit',
            json=resposta_filterNodes_ok
        )
        query_string = {
            'node_id': 1234
        }

        resposta_esperada = deepcopy(resposta_filterNodes_ok)
        resposta_esperada['numero_de_expansoes'] = [1, 1, 1]
        mock_resposta.json.return_value = resposta_esperada

        resposta = self.app.get(
            '/api/nextNodes',
            query_string=query_string
        )

        _conta_expansoes.assert_called_once_with('1234', '')
        self.assertEqual(resposta.json['numero_de_expansoes'], [1, 1, 1])


class LogoutUsuarioFlask(FlaskTestCase):
    @staticmethod
    def create_app():
        return app

    @mock.patch("sinapse.start._autenticar")
    def test_redirect_logout_follow(self, _autenticar):
        _autenticar.side_effect = ["usuario"]
        # Loga usuario
        self.client.post(
            "/login",
            data={
                "usuario": "usuario",
                "senha": "senha"})

        response = self.client.get('/logout', follow_redirects=True)
        self.assert_template_used('login.html')
        assert 'Você foi deslogado com sucesso' in response.data.decode(
            'utf-8'
        )

    def test_redireciona_para_login_quando_nao_logado(self):
        self.client.get('/logout', follow_redirects=True)

        self.assert_template_used('login.html')

    def test_evita_pre_fetch(self):
        response = self.client.get(
            '/logout',
            headers={'x-purpose': 'prefetch'}
        )

        self.assertEqual(response.status_code, 404)


class RemoveInfoSensivel(unittest.TestCase):
    @mock.patch("sinapse.start._LOG_ACESSO")
    def setUp(self, _LOG_ACESSO):
        self.app = app.test_client()
        with mock.patch("sinapse.start._autenticar") as _autenticar:
            _autenticar.side_effect = ["usuario"]
            self.app.post(
                "/login",
                data={
                    "usuario": "usuario",
                    "senha": "senha"})
            self.app.post("/compliance",
                data={
                    "tipoacesso": 1,
                    "numeroprocedimento": 1,
                    "descricao": 1
                })

    def test_remove_nos_sensiveis(self):
        nos = resposta_node_sensivel_ok['results'][0]['data'][0][
            'graph']['nodes']
        info = limpa_nos(nos)

        self.assertNotEqual(info, nos)
        self.assertEqual(info, nos_sensiveis_esp)

    def test_mantem_nos_nao_sensiveis(self):
        nos = resposta_node_ok['results'][0]['data'][0]['graph']['nodes']
        info = limpa_nos(nos)

        self.assertEqual(info, nos)

    def test_remove_relacoes_sensiveis(self):
        info = limpa_relacoes(relacoes_sensiveis)

        self.assertEqual(info, relacoes_sensiveis_esp)

    def test_remove_informacoes_sensiveis(self):
        info = remove_info_sensiveis(resposta_node_sensivel_ok)

        self.assertEqual(info, resposta_node_sensivel_esp)

    def test_remove_informacoes_sensiveis_mistas(self):
        self.maxDiff = None
        info = remove_info_sensiveis(resposta_sensivel_mista)

        self.assertEqual(info, resposta_sensivel_mista_esp)

    # TODO: separar utils de views
    def test_checa_se_informacao_e_sensivel(self):
        self.assertTrue(resposta_sensivel(resposta_node_sensivel_ok))
        self.assertFalse(resposta_sensivel(resposta_node_ok))

    @mock.patch("sinapse.start._log_response")
    @responses.activate
    def test_request_response_com_info_sensivel(self, _log_response):
        responses.add(
            responses.POST,
            _ENDERECO_NEO4J % '/db/data/transaction/commit',
            json=resposta_node_sensivel_ok
        )

        resposta = self.app.get('/api/node?node_id=395989945')

        self.assertEqual(
            resposta.json,
            parse_json_to_visjs(deepcopy(resposta_node_sensivel_esp))
        )

    @mock.patch("sinapse.start._log_response")
    @responses.activate
    def test_request_response_com_info_nao_sensivel(self, _log_response):
        responses.add(
            responses.POST,
            _ENDERECO_NEO4J % '/db/data/transaction/commit',
            json=resposta_node_ok
        )

        resposta = self.app.get('/api/node?node_id=395989945')

        self.assertEqual(
            resposta.json,
            parse_json_to_visjs(deepcopy(resposta_node_ok))
        )

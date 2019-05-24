import json
import unittest
import responses

from unittest import mock

from sinapse.whereabouts.whereabouts import (
    get_whereabouts_receita,
    get_whereabouts_credilink,
    extract_addresses_from_receita,
    extract_addresses_from_credilink,
)
from sinapse.start import (
    app,
    _ENDERECO_NEO4J
)
from .fixtures import (
    request_get_node_from_id,
    resposta_get_node_from_id_ok,
    resposta_get_node_from_id_sensivel_ok,
    input_whereabouts_addresses_receita,
    output_whereabouts_addresses_receita,
    input_whereabouts_addresses_credilink,
    output_whereabouts_addresses_credilink,
    resposta_whereabouts_receita_ok,
    resposta_whereabouts_credilink_ok,
    resposta_whereabouts_ok
)


def test_extract_addresses_from_receita():
    saida = extract_addresses_from_receita(input_whereabouts_addresses_receita)
    assert saida == output_whereabouts_addresses_receita


def test_extract_addresses_from_credilink():
    saida = extract_addresses_from_credilink(
        input_whereabouts_addresses_credilink
    )
    assert saida == output_whereabouts_addresses_credilink


class BuscaDeParadeiro(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        with mock.patch("sinapse.start._autenticar") as _autenticar:
            _autenticar.side_effect = ["usuario"]
            self.app.post(
                "/login",
                data={
                    "usuario": "usuario",
                    "senha": "senha"})

    @mock.patch('sinapse.whereabouts.whereabouts.get_data_from_receita')
    @responses.activate
    def test_whereabouts_receita(self, _get_data_from_receita):
        _get_data_from_receita.return_value = input_whereabouts_addresses_receita

        saida = get_whereabouts_receita(11452244740)

        assert saida == resposta_whereabouts_receita_ok

    @mock.patch('sinapse.whereabouts.whereabouts.get_data_from_credilink')
    @responses.activate
    def test_whereabouts_credilink(self, _get_data_from_credilink):
        _get_data_from_credilink.return_value = input_whereabouts_addresses_credilink

        saida = get_whereabouts_credilink(11452244740)

        assert saida == resposta_whereabouts_credilink_ok

    @mock.patch('sinapse.whereabouts.whereabouts.get_data_from_receita')
    @mock.patch('sinapse.whereabouts.whereabouts.get_data_from_credilink')
    @responses.activate
    def test_whereabouts(self, _get_data_from_credilink, _get_data_from_receita):
        _get_data_from_credilink.return_value = input_whereabouts_addresses_credilink
        _get_data_from_receita.return_value = input_whereabouts_addresses_receita
        query_string = {
            'node_id': 140885160
        }

        responses.add(
            responses.POST,
            _ENDERECO_NEO4J % '/db/data/transaction/commit',
            json=resposta_get_node_from_id_ok
        )

        resposta = self.app.get(
            '/api/whereabouts',
            query_string=query_string
        )

        assert resposta.get_json() == resposta_whereabouts_ok

        request = json.loads(responses.calls[-1].request.body)
        assert request == request_get_node_from_id

    @responses.activate
    def test_whereabouts_sensivel(self):
        query_string = {
            'node_id': 140885160
        }

        responses.add(
            responses.POST,
            _ENDERECO_NEO4J % '/db/data/transaction/commit',
            json=resposta_get_node_from_id_sensivel_ok
        )

        resposta = self.app.get(
            '/api/whereabouts',
            query_string=query_string
        )

        assert resposta.get_json() == []

import json
import unittest
import responses

from unittest import mock

from sinapse.whereabouts.whereabouts import (
    get_whereabouts_lc, 
    get_whereabouts_credilink,
    extract_addresses_from_lc,
    extract_addresses_from_credilink,
    get_data_from_lc,
    get_data_from_credilink
)
from sinapse.queries import get_node_from_id
from sinapse.start import (
    app,
    _ENDERECO_NEO4J
)
from .fixtures import (
    request_get_node_from_id,
    resposta_get_node_from_id_ok,
    resposta_get_node_from_id_sensivel_ok,
    input_whereabouts_addresses_lc,
    output_whereabouts_addresses_lc,
    input_whereabouts_addresses_credilink,
    output_whereabouts_addresses_credilink,
    resposta_whereabouts_lc_ok,
    resposta_whereabouts_credilink_ok,
    resposta_whereabouts_ok
)

def test_extract_addresses_from_lc():
    saida = extract_addresses_from_lc(input_whereabouts_addresses_lc)
    assert saida == output_whereabouts_addresses_lc


def test_extract_addresses_from_credilink():
    saida = extract_addresses_from_credilink(input_whereabouts_addresses_credilink)
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


    @mock.patch('sinapse.whereabouts.whereabouts.get_data_from_lc')
    @responses.activate
    def test_whereabouts_lc(self, _get_data_from_lc):
        _get_data_from_lc.return_value = input_whereabouts_addresses_lc

        saida = get_whereabouts_lc(11452244740)

        assert saida == resposta_whereabouts_lc_ok


    @mock.patch('sinapse.whereabouts.whereabouts.get_data_from_credilink')
    @responses.activate
    def test_whereabouts_credilink(self, _get_data_from_credilink):
        _get_data_from_credilink.return_value = input_whereabouts_addresses_credilink

        saida = get_whereabouts_credilink(11452244740)

        assert saida == resposta_whereabouts_credilink_ok


    @mock.patch('sinapse.whereabouts.whereabouts.get_data_from_lc')
    @mock.patch('sinapse.whereabouts.whereabouts.get_data_from_credilink')
    @responses.activate
    def test_whereabouts(self, _get_data_from_credilink, _get_data_from_lc):
        _get_data_from_credilink.return_value = input_whereabouts_addresses_credilink
        _get_data_from_lc.return_value = input_whereabouts_addresses_lc
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

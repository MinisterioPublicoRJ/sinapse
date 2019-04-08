import json
import unittest
import responses

from unittest import mock

from sinapse.whereabouts.labcontas import get_whereabouts_lc
from sinapse.whereabouts.credilink import get_whereabouts_credilink
from sinapse.queries import get_cpf_from_node
from sinapse.start import (
    app,
    _ENDERECO_NEO4J
)
from .fixtures import (
    request_get_cpf_from_node,
    resposta_get_cpf_from_node_ok
)

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

    def test_get_whereabouts_lc(self):
        pass

    def test_get_whereabouts_credilink(self):
        pass

    @responses.activate
    def test_get_cpf_from_node(self):
        pass

    def test_whereabouts(self):
        query_string = {
            'node_id': 140885160
        }

        responses.add(
            responses.POST,
            _ENDERECO_NEO4J % '/db/data/transaction/commit',
            json=resposta_get_cpf_from_node_ok
        )

        resposta = self.app.get(
            '/api/whereabouts',
            query_string=query_string
        )

        assert resposta.get_json() == '00000000001'

        request = json.loads(responses.calls[-1].request.body)
        assert request == request_get_cpf_from_node

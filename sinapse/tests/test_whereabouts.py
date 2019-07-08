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
from sinapse.start import app, _ENDERECO_NEO4J
from .fixtures import (
    request_get_node_from_id,
    resposta_get_node_from_id_ok,
    resposta_get_node_from_id_sensivel_ok,
    in_whereabouts_addresses_receita,
    output_whereabouts_addresses_receita,
    in_whereabouts_addresses_credilink,
    output_whereabouts_addresses_credilink,
    resposta_whereabouts_receita_ok,
    resp_whereabouts_credilink_ok,
)


def test_extract_addresses_from_receita():
    saida = extract_addresses_from_receita(
        in_whereabouts_addresses_receita
    )
    for s in saida:
        assert s in output_whereabouts_addresses_receita


def test_extract_addresses_from_credilink():
    saida = extract_addresses_from_credilink(
        in_whereabouts_addresses_credilink
    )
    for s in saida:
        assert s in output_whereabouts_addresses_credilink


class BuscaDeParadeiro(unittest.TestCase):
    @mock.patch("sinapse.start._LOG_ACESSO")
    def setUp(self, _LOG_ACESSO):
        self.app = app.test_client()
        with mock.patch("sinapse.start._autenticar") as _autenticar:
            _autenticar.side_effect = ["usuario"]
            self.app.post(
                "/login",
                data={"usuario": "usuario", "senha": "senha"}
            )
            self.app.post(
                "/compliance",
                data={
                    "tipoacesso": 1,
                    "numeroprocedimento": 1,
                    "descricao": 1
                },
            )

    @mock.patch("sinapse.whereabouts.whereabouts.get_data_from_receita")
    @responses.activate
    def test_whereabouts_receita(self, _get_data_from_receita):
        _get_data_from_receita.return_value = in_whereabouts_addresses_receita

        saida = get_whereabouts_receita(1)

        assert saida["type"] == resposta_whereabouts_receita_ok["type"]
        assert len(
            resposta_whereabouts_receita_ok["formatted_addresses"]) == len(
            saida["formatted_addresses"]
        )
        assert (
            resposta_whereabouts_receita_ok["formatted_addresses"][0]
            in saida["formatted_addresses"]
        )

    @mock.patch("sinapse.whereabouts.whereabouts.get_data_from_credilink")
    @responses.activate
    def test_whereabouts_credilink(self, _data_from_credilink):
        _data_from_credilink.return_value = in_whereabouts_addresses_credilink

        saida = get_whereabouts_credilink(1)

        assert saida["type"] == resp_whereabouts_credilink_ok["type"]
        assert len(
            resp_whereabouts_credilink_ok[
                "formatted_addresses"
            ]) == len(saida["formatted_addresses"])
        assert (
            resp_whereabouts_credilink_ok["formatted_addresses"][0]
            in saida["formatted_addresses"]
        )
        assert (
            resp_whereabouts_credilink_ok["formatted_addresses"][1]
            in saida["formatted_addresses"]
        )

    @mock.patch("sinapse.start.get_whereabouts_credilink")
    @responses.activate
    def test_api_whereabouts_credilink(self, _get_whereabouts_credilink):
        _get_whereabouts_credilink.return_value = resp_whereabouts_credilink_ok
        query_string = {"uuid": 140885160}

        responses.add(
            responses.POST,
            _ENDERECO_NEO4J % "/db/data/transaction/commit",
            json=resposta_get_node_from_id_ok,
        )

        resposta = self.app.get(
            "/api/whereaboutsCredilink",
            query_string=query_string
        )
        saida = resposta.get_json()

        assert resp_whereabouts_credilink_ok == saida

        request = json.loads(responses.calls[-1].request.body)
        assert request == request_get_node_from_id

    @mock.patch("sinapse.start.get_whereabouts_receita")
    @responses.activate
    def test_api_whereabouts_receita(self, _get_whereabouts_receita):
        _get_whereabouts_receita.return_value = resposta_whereabouts_receita_ok
        query_string = {"uuid": 140885160}

        responses.add(
            responses.POST,
            _ENDERECO_NEO4J % "/db/data/transaction/commit",
            json=resposta_get_node_from_id_ok,
        )

        resposta = self.app.get(
            "/api/whereaboutsReceita",
            query_string=query_string
        )
        saida = resposta.get_json()

        assert resposta_whereabouts_receita_ok == saida

        request = json.loads(responses.calls[-1].request.body)
        assert request == request_get_node_from_id

    @responses.activate
    def test_whereabouts_credilink_sensivel(self):
        query_string = {"node_id": 140885160}

        responses.add(
            responses.POST,
            _ENDERECO_NEO4J % "/db/data/transaction/commit",
            json=resposta_get_node_from_id_sensivel_ok,
        )

        resposta = self.app.get(
            "/api/whereaboutsCredilink",
            query_string=query_string
        )

        assert resposta.get_json() == {}

    @responses.activate
    def test_whereabouts_receita_sensivel(self):
        query_string = {"node_id": 140885160}

        responses.add(
            responses.POST,
            _ENDERECO_NEO4J % "/db/data/transaction/commit",
            json=resposta_get_node_from_id_sensivel_ok,
        )

        resposta = self.app.get(
            "/api/whereaboutsReceita",
            query_string=query_string
        )

        assert resposta.get_json() == {}

import unittest

import responses

from decouple import config

from sinapse.detran.client import send_rg_query, get_processed_rg
from sinapse.detran.utils import parse_content, get_node_id
from sinapse.tests.fixtures import (
    response_rg,
    response_processado_rg,
    resposta_node_ok)


class Photo(unittest.TestCase):
    @responses.activate
    def test_consulta_rg(self):
        responses.add(
            responses.POST,
            config('URL_CONSULTA_RG'),
            body=response_rg,
            status=200,
            content_type='application/soap+xml; charset=utf-8'
        )

        rg = '1234'
        status, content = send_rg_query(rg)

        self.assertEqual(status, 200)
        self.assertEqual(content, response_rg)
        self.assertIn(b'sucesso', content)

    @responses.activate
    def test_busca_rg_processado(self):
        responses.add(
            responses.POST,
            config('URL_PROCESSADO_RG'),
            body=response_processado_rg,
            status=200,
            content_type='application/soap+xml; charset=utf-8'
        )

        rg = '1234'
        status, content = get_processed_rg(rg)

        self.assertEqual(status, 200)
        self.assertEqual(content, response_processado_rg)
        self.assertIn(b'fotoCivil', content)


class Utils(unittest.TestCase):
    def test_paser_xml_content(self):
        foto_civil = parse_content(response_processado_rg)
        expected = 'abcd'

        self.assertEqual(foto_civil, expected)

    def test_find_node_ids(self):
        node_id = get_node_id(resposta_node_ok)
        expected = '395989945'

        self.assertEqual(node_id, expected)


if __name__ == "__main__":
    unittest.main()

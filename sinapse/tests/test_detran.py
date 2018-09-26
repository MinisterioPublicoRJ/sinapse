import unittest

import responses

from decouple import config

from sinapse.detran.client import send_rg_query
from sinapse.tests.fixtures import response_rg


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


if __name__ == "__main__":
    unittest.main()

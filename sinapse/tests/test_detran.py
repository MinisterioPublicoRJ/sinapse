import unittest

import responses

from decouple import config

from sinapse.detran.client import busca_foto


class TestClient(unittest.TestCase):
    @responses.activate
    def test_consulta_api_fotos(self):
        rg = "12345"
        url_busca = config("URL_BUSCA_FOTO")
        token_busca = config("TOKEN_BUSCA_FOTO")
        responses.add(
            responses.GET,
            url_busca.format(rg=rg) + "?proxy-token={}".format(token_busca),
            json={"photo": "img_b64"},
            status=200
        )

        photo = busca_foto(rg)

        assert photo == "img_b64"

    @responses.activate
    def test_consulta_api_fotos_fail(self):
        rg = "12345"
        url_busca = config("URL_BUSCA_FOTO")
        token_busca = config("TOKEN_BUSCA_FOTO")
        responses.add(
            responses.GET,
            url_busca.format(rg=rg) + "?proxy-token={}".format(token_busca),
            status=404
        )

        photo = busca_foto(rg)

        assert photo == ""


if __name__ == "__main__":
    unittest.main()

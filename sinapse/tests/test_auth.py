import unittest
import jwt

from freezegun import freeze_time
from sinapse.url import (
    app
)


class Autorizacao(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    @freeze_time("2018-07-24 14:30:00")
    def test_autorizacao(self):
        resposta = self.app.post(
            '/api/autorizar',
            data={
                'sistema': '1234',
                'usuario': 'ministerio.publico'
            }
        )

        assert resposta.status_code == 200

        mensagem = jwt.decode(
            resposta.get_data(),
            app.secret_key,
            algorithms=['HS256']
        )

        assert mensagem['usuario'] == 'ministerio.publico'
        assert mensagem['validade'] == '2018-07-24 14:31:00'

    def test_sistema_invalido(self):
        resposta = self.app.post(
            '/api/autorizar',
            data={
                'sistema': '0000',
                'usuario': 'ministerio.publico'
            }
        )

        assert resposta.status_code == 401

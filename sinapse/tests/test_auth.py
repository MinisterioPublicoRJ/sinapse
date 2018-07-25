import unittest
import jwt

from freezegun import freeze_time
from unittest import mock

from sinapse.url import (
    app
)
from sinapse.auth import autenticadorjwt


# Patch para mocks de dicionários
dicio = {}


def getitem(name):
    return dicio[name]


def setitem(name, val):
    dicio[name] = val


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
            app.secret_key
        )

        assert mensagem['usuario'] == 'ministerio.publico'
        assert mensagem['exp'] == 1532442660

    def test_sistema_invalido(self):
        resposta = self.app.post(
            '/api/autorizar',
            data={
                'sistema': '0000',
                'usuario': 'ministerio.publico'
            }
        )

        assert resposta.status_code == 403

    @freeze_time("2018-07-24 14:30:00")
    def test_api_filtra(self):
        resposta = self.app.post(
            '/api/autorizar',
            data={
                'sistema': '1234',
                'usuario': 'ministerio.publico'
            }
        )

        assert resposta.status_code == 200

        resposta = self.app.post(
            '/api/filtrar',
            data={
                'label': 'pessoa',
                'prop': 'nome',
                'val': 'DANIEL CARVALHO BELCHIOR'
            },
            headers={
                'Authorization': ' JWT %s' % resposta.get_data()
            }
        )

        assert resposta.status_code == 200
        conteudo = resposta.get_data().decode('utf-8')
        assert 'window.filtroInicial' in conteudo
        assert 'DANIEL CARVALHO BELCHIOR' in conteudo

    @mock.patch('sinapse.auth.session', spec_set=dict)
    @mock.patch('sinapse.auth.request')
    def test_autenticadorjwt(self, _request, _session):
        @autenticadorjwt
        def metodo_decorado():
            return True

        data = {
            'sistema': '1234',
            'usuario': 'ministerio.publico'
        }

        _request.form = data

        resposta = self.app.post(
            '/api/autorizar',
            data=data
        )

        _request.headers = {
            'authorization': ' JWT %s' % resposta.get_data().decode('utf-8')
        }

        _session.__getitem__.side_effect = getitem
        _session.__setitem__.side_effect = setitem

        assert metodo_decorado() is True
        assert _session['usuario'] == 'ministerio.publico'

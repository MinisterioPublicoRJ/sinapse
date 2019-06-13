import unittest
import jwt

from freezegun import freeze_time
from unittest import mock

from sinapse.url import (
    app
)
from sinapse.auth import (
    autenticadorjwt,
    _gerarjwt
)


# Patch para mocks de dicionários
dicio = {}


def getitem(name):
    return dicio[name]


def setitem(name, val):
    dicio[name] = val


@autenticadorjwt
def metodo_decorado():
    return True


class Autorizacao(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    @freeze_time("2018-07-24 14:30:00")
    def test_autorizacao(self):
        resposta = self.app.post(
            '/api/autorizar',
            data={
                'sistema': 'DOMINIO',
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

    def test_api_filtra(self):
        token = _gerarjwt('ministerio.publico')

        resposta = self.app.get(
            '/api/filtroinicial',
            query_string={
                'authorization': token,
                'label': 'pessoa',
                'prop': 'nome',
                'val': 'DANIEL CARVALHO BELCHIOR'
            }
        )

        assert resposta.status_code == 200
        conteudo = resposta.get_data().decode('utf-8')
        assert 'window.filtroInicial' in conteudo
        assert 'DANIEL CARVALHO BELCHIOR' in conteudo

    @mock.patch('sinapse.auth.session', spec_set=dict)
    @mock.patch('sinapse.auth.request')
    def test_autenticadorjwt(self, _request, _session):
        token = _gerarjwt('ministerio.publico')
        _request.args = {
            'authorization': token.decode('utf-8')
        }

        _session.__getitem__.side_effect = getitem
        _session.__setitem__.side_effect = setitem

        assert metodo_decorado() is True
        self.assertEqual(_session['usuario'], 'ministerio.publico')

    @mock.patch('sinapse.auth.request')
    def test_autenticadorjwt_embranco(self, _request):
        _request.args.get.return_value = None
        self.assertEqual(metodo_decorado(), ('', 403))
        _request.args.get.assert_called_once_with('authorization')

    @mock.patch('sinapse.auth.request')
    def test_autenticadorjwt_temperado(self, _request):
        token = _gerarjwt('ministerio.publico')
        _request.headers = {
            'authorization': ' JWT %s' % token.decode('utf-8') + 'abc'
        }

        self.assertEqual(metodo_decorado(), ('Erro de Assinatura', 403))

    @mock.patch('sinapse.auth.request')
    def test_autenticadorjwt_expirado(self, _request):
        with freeze_time("2018-07-24 14:30:00"):
            token = _gerarjwt('ministerio.publico')

        _request.args = {
            'authorization': token.decode('utf-8')
        }

        with freeze_time("2018-07-24 14:32:00"):
            self.assertEqual(metodo_decorado(), ('Expirado', 401))

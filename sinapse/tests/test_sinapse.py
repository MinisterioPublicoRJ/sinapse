import unittest
from sinapse import start


class CasoGlobal(unittest.TestCase):

    def setUp(self):
        self.app = start.app.test_client()

    def test_raiz(self):
        resposta = self.app.get('/')
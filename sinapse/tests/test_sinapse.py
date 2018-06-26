import unittest

from unittest import mock

from sinapse import start
from sinapse.buildup import (
    _AUTH,
    _HEADERS
)


class CasoGlobal(unittest.TestCase):

    def setUp(self):
        self.app = start.app.test_client()

    def test_raiz(self):
        resposta = self.app.get('/')

        assert resposta.status_code == 200

        assert resposta.status_code == 200
        _post.assert_called_once_with(
            'http://neo4j.cloud.mprj.mp.br/db/data/transaction/commit',
            data=('{"statements": [{"statement": "MATCH  (n) where id(n) = 1'
                  ' return n", "resultDataContents": ["row", "graph"]}]}'),
            auth=_AUTH,
            headers=_HEADERS
        )

import json

from unittest import TestCase, mock

from sinapse.queries import find_next_nodes

from sinapse.buildup import (
    _ENDERECO_NEO4J,
    _AUTH,
    _HEADERS
)


class FindNextNodes(TestCase):
    @mock.patch('sinapse.queries.requests.post')
    def test_find_next_nodes(self, _post):
        """
            Check if Neo4j API is called with the correct query
        """
        parameters = {
            'relation_type': 'family',
            'path_size': 1,
            'node_type': ':person',
            'limit': 'limit 100',
            'where': 'id(n) = 1234'
        }

        find_next_nodes(parameters)

        expected_query = {"statements": [{
            "statement": "MATCH r = (n)-[family*..1]-(x:person) where id(n)"
            " = 1234"
            " return r,n,x limit 100",
            "resultDataContents": ["row", "graph"]
        }]}
        _post.assert_called_once_with(
            _ENDERECO_NEO4J % '/db/data/transaction/commit',
            data=json.dumps(expected_query),
            auth=_AUTH,
            headers=_HEADERS
        )

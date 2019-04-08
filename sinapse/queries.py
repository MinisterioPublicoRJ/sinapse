import json

import requests

from sinapse.buildup import (
    _ENDERECO_NEO4J,
    _AUTH,
    _HEADERS,
)


def find_next_nodes(node_id, rel_types=''):
    query = {"statements": [{
        "statement": "MATCH r = (n)-[%s*..1]-(x) where id(n) = %s"
        " return r,n,x limit 100" % (rel_types, node_id),
        "resultDataContents": ["row", "graph"]
    }]}
    response = requests.post(
        _ENDERECO_NEO4J % '/db/data/transaction/commit',
        data=json.dumps(query),
        auth=_AUTH,
        headers=_HEADERS)

    return response

def get_cpf_from_node(node_id):
    query = {"statements": [{
        "statement": "MATCH (n:pessoa) WHERE id(n) = %s"
        " RETURN n.cpf as num_cpf" % (node_id),
        "resultDataContents": ["row"]
    }]}

    response = requests.post(
        _ENDERECO_NEO4J % '/db/data/transaction/commit',
        data=json.dumps(query),
        auth=_AUTH,
        headers=_HEADERS)

    return response
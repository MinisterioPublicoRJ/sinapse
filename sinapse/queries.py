import json
import re
import requests

from decouple import config

from sinapse.buildup import (
    _ENDERECO_NEO4J,
    _AUTH,
    _HEADERS,
)


def find_next_nodes(node_id):
    query = {"statements": [{
        "statement": "MATCH r = (n)-[*..1]-(x) where id(n) = %s"
        " return r,n,x limit 100" % node_id,
        "resultDataContents": ["row", "graph"]
    }]}
    response = requests.post(
        _ENDERECO_NEO4J % '/db/data/transaction/commit',
        data=json.dumps(query),
        auth=_AUTH,
        headers=_HEADERS)

    return response


def search_by_name(name):
    f_name = re.sub(r'\s+', '+', name)
    query = """pessoa_fisica_shard1_replica1/select?q=%22{f_name}%22&fl=uuid+nome+nome_mae&wt=json&indent=true&defType=edismax&qf=nome%5E10+nome_mae%5E5&qs=1&stopwords=true&lowercaseOperators=true&hl=true&hl.simple.pre=%3Cem%3E&hl.simple.post=%3C%2Fem%3E""".format(f_name=f_name)
    query += config('HOST_SOLR')
    return requests.get(query)

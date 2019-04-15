import json
import re
import requests

from datetime import datetime

from decouple import config

from sinapse.buildup import (
    _ENDERECO_NEO4J,
    _AUTH,
    _HEADERS,
    _LOG_SOLR
)


def find_next_nodes(node_id, rel_types='', path_size=1):
    query = {"statements": [{
        "statement": "MATCH r = (n)-[%s*..%s]-(x) where id(n) = %s"
        " return r,n,x limit 100" % (rel_types, path_size, node_id),
        "resultDataContents": ["row", "graph"]
    }]}
    response = requests.post(
        _ENDERECO_NEO4J % '/db/data/transaction/commit',
        data=json.dumps(query),
        auth=_AUTH,
        headers=_HEADERS)

    return response

def get_node_from_id(node_id):
    query = {"statements": [{
        "statement": "MATCH (n:pessoa) WHERE id(n) = %s"
        " RETURN n" % (node_id),
        "resultDataContents": ["graph"]
    }]}

    response = requests.post(
        _ENDERECO_NEO4J % '/db/data/transaction/commit',
        data=json.dumps(query),
        auth=_AUTH,
        headers=_HEADERS)

    return response

def search_info(q, solr_queries):
    f_q = re.sub(r'\s+', '+', q)
    resp = dict()
    for label, query in solr_queries.items():
        if query:
            resp[label] = _solr_search(f_q, query)
    return resp


def clean_info(func):
    def wrapper(f_q, query):
        resp = func(f_q, query)
        resp_copy = resp.json().copy()
        resp_copy.pop('responseHeader')
        return resp_copy
    return wrapper


@clean_info
def _solr_search(f_q, query):
    query = config('HOST_SOLR') + query.format(f_q=f_q)
    return requests.get(query)


def log_solr_response(user, sessionid, query):
    _LOG_SOLR.insert_one({
        'usuario': user,
        'sessionid': sessionid,
        'datahora': datetime.now(),
        'resposta': query
    })

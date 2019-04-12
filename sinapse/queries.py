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


SOLR_QUERIES = json.load(open(config('SOLR_QUERIES'), 'r'))


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


def search_info(q):
    f_q = re.sub(r'\s+', '+', q)
    person = _search_person(f_q)
    auto = _search_auto(f_q)
    company = _search_company(f_q)
    return person, auto, company


def clean_info(func):
    def wrapper(f_q):
        resp = func(f_q)
        resp_copy = resp.json().copy()
        resp_copy.pop('responseHeader')
        return resp_copy
    return wrapper


@clean_info
def _search_person(f_q):
    query = SOLR_QUERIES['pessoa'].format(f_q=f_q)
    query = config('HOST_SOLR') + query
    return requests.get(query)


@clean_info
def _search_auto(f_q):
    query = SOLR_QUERIES['veiculo'].format(f_q=f_q)
    query = config('HOST_SOLR') + query
    return requests.get(query)


@clean_info
def _search_company(f_q):
    query = SOLR_QUERIES['empresa'].format(f_q=f_q)
    query = config('HOST_SOLR') + query
    return requests.get(query)


def log_solr_response(user, sessionid, query):
    _LOG_SOLR.insert_one({
        'usuario': user,
        'sessionid': sessionid,
        'datahora': datetime.now(),
        'resposta': query
    })

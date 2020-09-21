import json
import re
import requests
import urllib

from datetime import datetime
from urllib.parse import quote
from urllib.error import URLError
from urllib.request import Request, urlopen

from decouple import config
from requests_kerberos import HTTPKerberosAuth

from sinapse.buildup import (
    _ENDERECO_NEO4J,
    _AUTH,
    _HEADERS,
    _LOG_SOLR
)
from sinapse.detran.utils import find_relations_info


IMG_HEADERS = {}
IMG_HEADERS['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1)"\
    " AppleWebKit/537.36 (KHTML, like Gecko)"\
    " Chrome/41.0.2228.0 Safari/537.36"


def find_next_nodes(parameters):
    query = {"statements": [{
        "statement": "MATCH r = (n)-[{relation_type}*..{path_size}]-"
        "(x{node_type}) where {where}"
        " return r,n,x {limit}".format(**parameters),
        "resultDataContents": ["row", "graph"]
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
            try:
                resp[label] = _solr_search(f_q, query)
            except BaseException:
                pass
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
    return requests.get(query, auth=HTTPKerberosAuth())


def log_solr_response(user, sessionid, query):
    _LOG_SOLR.insert_one({
        'usuario': user,
        'sessionid': sessionid,
        'datahora': datetime.now(),
        'resposta': query
    })


def download_google_image(term):
    url = 'https://www.google.com/search?q='\
        + quote(term)\
        + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch'\
        + '&tbs=isz:l&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'

    req = urllib.request.Request(url, headers=IMG_HEADERS)
    resp = urllib.request.urlopen(req)
    content = str(resp.read())
    return extact_img(content)


def extact_img(content):
    limit = 1000
    count = 1
    while count < limit + 1:
        img = ''
        obj_content, end_content = _get_next_item(content)
        img_url = obj_content['ou']

        try:
            img = download_image(img_url)
        except URLError:
            pass

        if img != '':
            return img

        content = content[end_content:]
        count += 1

    return ''


def download_image(image_url):
    req = Request(image_url, headers=IMG_HEADERS)
    response = urlopen(req, None, timeout=10)
    data = response.read()
    return data


def _get_next_item(s):
    start_line = s.find('rg_meta notranslate')
    if start_line == -1:  # If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = s.find('class="rg_meta notranslate">')
        start_object = s.find('{', start_line + 1)
        end_object = s.find('</div>', start_object + 1)
        object_raw = str(s[start_object:end_object])
        object_decode = bytes(
            object_raw, "utf-8").decode("unicode_escape")
        final_object = json.loads(object_decode)
        return final_object, end_object


# Person Info
def person_info(node_id):
    person_query = {
        'where': 'id(n) = {id}'.format(id=node_id),
        'relation_type': '',
        'path_size': 1,
        'limit': '',
        'node_type': ':Pessoa'
    }
    person_nodes = find_next_nodes(person_query)
    fri = find_relations_info(
        person_nodes.json(),
        pks=['num_rg'],
        label='Pessoa',
        props=['num_rg']
    )
    fri = [item._asdict() for item in fri]
    return fri


# Vehicle Info
def vehicle_info(node_id):
    vehicle_query = {
        'where': 'id(n) = {id}'.format(id=node_id),
        'relation_type': '',
        'path_size': 1,
        'limit': '',
        'node_type': ''
    }
    vehicle_nodes = find_next_nodes(vehicle_query)
    return find_relations_info(
        vehicle_nodes.json(),
        pks=['marca', 'modelo', 'cor'],
        label='veiculo',
        props=['marca', 'modelo', 'cor']  # Add UUID
    )

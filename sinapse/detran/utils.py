from collections import namedtuple

import lxml.etree as et


def parse_content(content, tag_name):
    xml_obj = et.fromstring(content)
    prefix = '*//{http://www.detran.rj.gov.br}' + tag_name
    try:
        content = xml_obj.find(prefix).text
    except AttributeError:
        return ''
    if not content:
        content = xml_obj.find(prefix).find('*').text

    return content


def get_node_id(response_json):
    return response_json['nodes'][0]['id']


def find_relations_info(response_json):
    person_info = namedtuple('Pessoa', ['rg', 'node_id'])
    saved_rg = []
    info = []
    for data in response_json['results'][0]['data']:
        for node in data['graph']['nodes']:
            if node['labels'] == ['pessoa']:
                rg = node['properties'].get('rg')
                if rg is not None and rg not in saved_rg:
                    info.append(
                        person_info(
                            node['properties']['rg'],
                            node['id'])
                    )
                    saved_rg.append(rg)

    return info

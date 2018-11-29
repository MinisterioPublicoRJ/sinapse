from collections import namedtuple

import lxml.etree as et


def parse_content(content, tag_name):
    xml_obj = et.fromstring(content)
    prefix = '*//{http://www.detran.rj.gov.br}' + tag_name
    content = xml_obj.find(prefix).text
    if not content:
        content = xml_obj.find(prefix).find('*').text

    return content


def get_node_id(response_json):
    return response_json['results'][0]['data'][0]['meta'][0]['id']


def find_relations_info(response_json):
    person_info = namedtuple('Pessoa', ['rg', 'node_id'])
    info = []
    for data in response_json['results'][0]['data']:
        for node in data['graph']['nodes']:
            if node['labels'] == ['pessoa']:
                info.append(
                    person_info(
                        node['properties']['rg'],
                        node['id'])
                )

    return list(set(info))

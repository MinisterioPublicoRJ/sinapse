from collections import namedtuple

import lxml.etree as et


def parse_content(content):
    xml_obj = et.fromstring(content)
    level = xml_obj.findall('*')
    while len(level) == 1:
        level = level[0].find('*')

    for ele in level:
        if 'foto' in ele.tag:
            return ele.find('*').text


def get_node_id(response_json):
    return response_json['nodes'][0]['id']


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

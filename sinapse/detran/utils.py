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
    return response_json['results'][0]['data'][0]['graph']['nodes'][0]['id']


def find_relations_info(response_json, pks, label, props):
    info_obj = namedtuple(label.capitalize(), ['uuid'] + props)
    saved_pk = []
    info = []
    for data in response_json['results'][0]['data']:
        for node in data['graph']['nodes']:
            if node['labels'] == [label]:
                pk_ = ' '.join([node['properties'].get(pk, '') for pk in pks])
                if pk_ and pk_ not in saved_pk:
                    props_val = [node['properties'][p] for p in props]
                    info.append(
                        info_obj(
                            *[node['properties']['uuid']] +
                            props_val
                        )
                    )
                    saved_pk.append(pk_)

    return info

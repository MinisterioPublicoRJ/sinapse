import lxml.etree as et


def parse_content(content):
    xml_obj = et.fromstring(content)
    return xml_obj.find('*').find('*').find('*').find('*').findall('*')[23].\
        find('*').text


def get_node_id(response_json):
    return response_json['results'][0]['data'][0]['meta'][0]['id']


def find_relations_info(response_json):
    info = []
    for row in response_json['results'][0]['data']:
        info.append(
            {
                'node_id': row['graph']['nodes'][0]['id'],
                'rg': row['graph']['nodes'][0]['properties']['rg']
             }
        )

    return info

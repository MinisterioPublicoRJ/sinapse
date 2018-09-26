import lxml.etree as et


def parse_content(content):
    xml_obj = et.fromstring(content)
    return xml_obj.find('*').find('*').find('*').find('*').findall('*')[23].\
        find('*').text

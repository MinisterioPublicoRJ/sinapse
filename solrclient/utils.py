from collections import namedtuple


def solr2info(solr_resp, label, props):
    info = namedtuple(label, props)
    return [info(*[doc[key] for key in props]) for doc in solr_resp['docs']]

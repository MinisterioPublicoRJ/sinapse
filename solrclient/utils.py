from collections import namedtuple


def solr2info(solr_resp, label, props):
    info = namedtuple(label, props)
    return [
        info(
            *[str(doc[key]).strip() for key in props]
        )._asdict()
        for doc in solr_resp['response']['docs'] if set(props).issubset(doc)
    ]

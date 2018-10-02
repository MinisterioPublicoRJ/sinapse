import requests

from decouple import config

from sinapse.buildup import _MONGO_CLIENT
from sinapse.detran.utils import find_relations_info, parse_content
from sinapse.queries import find_next_nodes


COLLECTION_FOTOS = _MONGO_CLIENT.mmps.fotos


RG_BODY = """<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xmlns:xsd="http://www.w3.org/2001/XMLSchema"
xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <consultarRG xmlns="http://www.detran.rj.gov.br">
      <CNPJ>{cnpj}</CNPJ>
      <chave>{chave}</chave>
      <perfil>{perfil}</perfil>
      <IDCidadao>{idcidadao}</IDCidadao>
      <RG>{rg}</RG>
      <CPF>{cpf}</CPF>
    </consultarRG>
  </soap12:Body>
</soap12:Envelope>"""

RG_PROCESSED_BODY = """<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xmlns:xsd="http://www.w3.org/2001/XMLSchema"
xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
      <BuscarProcessados xmlns="http://www.detran.rj.gov.br">
       <CNPJ>{cnpj}</CNPJ>
       <chave>{chave}</chave>
       <perfil>{perfil}</perfil>
       <IDCidadao>{idcidadao}</IDCidadao>
      </BuscarProcessados>
    </soap12:Body>
</soap12:Envelope>"""


def send_rg_query(rg):
    body = RG_BODY.format(
        cnpj=config('CNPJ'),
        chave=config('CHAVE'),
        perfil=config('PERFIL'),
        idcidadao=rg,
        rg=rg.zfill(10),
        cpf=config('CPF')
    )
    body = body.encode('utf-8')

    headers = {
        'Content-Type': 'application/soap+xml; charset=utf-8',
        'Content-Length': str(len(body))
    }

    response = requests.post(
        config('URL_CONSULTA_RG'),
        data=body,
        headers=headers
    )

    return response.status_code, response.content


def get_processed_rg(rg):
    body = RG_PROCESSED_BODY.format(
        cnpj=config('CNPJ'),
        chave=config('chave'),
        perfil=config('perfil'),
        idcidadao=rg
    )

    headers = {
        'Content-Type': 'application/soap+xml; charset=utf-8',
        'Content-Length': str(len(body))
    }

    response = requests.post(
        config('URL_PROCESSADO_RG'),
        data=body,
        headers=headers
    )

    return response.status_code, response.content


def get_photos(node_id):
    next_nodes = find_next_nodes(node_id)
    infos = find_relations_info(next_nodes.json())

    successes = []
    for info in infos:
        photo_document = COLLECTION_FOTOS.find_one(
            {'rg': info.rg,
             'foto': {'$exists': True}}
        )
        if photo_document is None:
            status, content = send_rg_query(info.rg)
            if b'sucesso' in content.lower()\
                    or b'foi finalizada' in content.lower():
                successes.append(info)

    for success in successes:
        status, content = get_processed_rg(success.rg)
        photo = parse_content(content)
        if photo is not None:
            COLLECTION_FOTOS.update(
                {'rg': success.rg},
                {'$set': {'foto': photo}},
                upsert=True
            )

import json

import requests

from decouple import config

from sinapse.buildup import (
    _ENDERECO_NEO4J,
    _HEADERS,
    _AUTH,
)


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


def find_persons(node_id):
    query = {"statements": [{
        "statement": "MATCH (p1:pessoa) WHERE id(p1) = " + node_id +
        " WITH p1 match (p2:pessoa) match r = (p1)-[*..1]-(p2) return p2",
        "resultDataContents": ["row", "graph"]
    }]}

    return requests.post(
        _ENDERECO_NEO4J % '/db/data/transaction/commit',
        data=json.dumps(query),
        auth=_AUTH,
        headers=_HEADERS).json()

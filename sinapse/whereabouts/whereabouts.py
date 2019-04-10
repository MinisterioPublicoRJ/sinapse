from impala.dbapi import connect
from decouple import config
from zeep import Client

import xml.etree.ElementTree as ET

IMPALA_HOST = config('BDA_URL')
IMPALA_PORT = config('IMPALA_PORT', default=21050, cast=int)

CREDILINK_URL = config('CREDILINK_URL')
CREDILINK_USUARIO = config('CREDILINK_USUARIO')
CREDILINK_SENHA = config('CREDILINK_SENHA')
CREDILINK_SIGLA = config('CREDILINK_SIGLA')

def get_whereabouts_lc(num_cpf):
    whereabouts = {'type': 'receita_federal'}

    with connect(host=IMPALA_HOST, port=IMPALA_PORT) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT tipo_logradouro, 
            descr_logradouro, 
            num_logradouro, 
            descr_complemento_logradouro, 
            nome_bairro,
            num_cep,
            nome_municipio,
            sigla_uf,
            num_ddd, num_telefone 
            FROM bases.lc_cpf 
            WHERE num_cpf = '{}'""".format(num_cpf))
        addresses = []
        for data in cursor.fetchall():
            address = {
                'endereco': data[0] + " " + data[1], 
                'numero': data[2],
                'complemento': data[3],
                'bairro': data[4],
                'cep': data[5],
                'cidade': data[6],
                'sigla_uf': data[7],
                'telefone': data[8] + data[9]
            }
            addresses.append(address)
        whereabouts['formatted_addresses'] = addresses

    return whereabouts

def get_whereabouts_credilink(num_cpf):
    whereabouts = {'type': 'credilink'}

    cliente = Client(CREDILINK_URL)

    response = cliente.service.completo(
        usuario=CREDILINK_USUARIO,
        senha=CREDILINK_SENHA,
        sigla=CREDILINK_SIGLA,
        cpfcnpj=num_cpf,
        nome='',
        telefone=''
    )

    root = ET.fromstring(response)

    telefones = root.find('consulta_telefone_proprietario').findall('telefone')

    addresses = []
    for tel in telefones:
        address = {
            'endereco': tel.find('endereco').text, 
            'numero': tel.find('numero').text,
            'complemento': tel.find('complemento').text,
            'bairro': tel.find('bairro').text,
            'cep': tel.find('cep').text,
            'cidade': tel.find('cidade').text,
            'sigla_uf': tel.find('uf').text,
            'telefone': tel.find('telefone').text
        }
        addresses.append(address)
    whereabouts['formatted_addresses'] = addresses

    return whereabouts
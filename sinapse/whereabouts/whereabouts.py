from impala.dbapi import connect
from decouple import config
from zeep import Client

import xml.etree.ElementTree as ET
import ast

IMPALA_HOST = config('BDA_URL')
IMPALA_PORT = config('IMPALA_PORT', default=21050, cast=int)

CREDILINK_URL = config('CREDILINK_URL')
CREDILINK_USUARIO = config('CREDILINK_USUARIO')
CREDILINK_SENHA = config('CREDILINK_SENHA')
CREDILINK_SIGLA = config('CREDILINK_SIGLA')


def get_data_from_receita(num_cpf):
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
        rows = cursor.fetchall()
    return rows


def extract_addresses_from_receita(rows):
    addresses = []
    for data in rows:
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
    return addresses


def get_whereabouts_receita(num_cpf):
    rows = get_data_from_receita(num_cpf)

    addresses = extract_addresses_from_receita(rows)

    whereabouts = {'type': 'receita_federal'}
    whereabouts['formatted_addresses'] = addresses

    return whereabouts


def get_data_from_credilink(num_cpf):
    cliente = Client(CREDILINK_URL)

    response = cliente.service.completo(
        usuario=CREDILINK_USUARIO,
        senha=CREDILINK_SENHA,
        sigla=CREDILINK_SIGLA,
        cpfcnpj=num_cpf,
        nome='',
        telefone=''
    )

    return response


def extract_addresses_from_credilink(response):
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

    #Remove duplicate addresses
    addresses = [ast.literal_eval(s) for s in set([str(d) for d in addresses])]

    return addresses


def get_whereabouts_credilink(num_cpf):
    response = get_data_from_credilink(num_cpf)

    addresses = extract_addresses_from_credilink(response)

    whereabouts = {'type': 'credilink'}
    whereabouts['formatted_addresses'] = addresses

    return whereabouts

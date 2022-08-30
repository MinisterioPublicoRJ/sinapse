from impala.dbapi import connect
from decouple import config
import xml.etree.ElementTree as ET
import requests
import ast

IMPALA_HOST = config('BDA_URL')
IMPALA_PORT = config('IMPALA_PORT', default=21050, cast=int)
KERBEROS_SERVICE_NAME = config('KERBEROS_SERVICE_NAME', default='impala')
KERBEROS_USER = config('KERBEROS_USER')

PREVINITY_URL = config('PREVINITY_URL')
PREVINITY_USER = config('PREVINITY_USER')
PREVINITY_PASS = config('PREVINITY_PASS')

def get_data_from_receita(num_cpf):
    with connect(
        host=IMPALA_HOST,
        port=IMPALA_PORT,
        use_ssl=False,
        user=KERBEROS_USER,
        kerberos_service_name=KERBEROS_SERVICE_NAME,
        auth_mechanism='GSSAPI'
    ) as conn:
        with conn.cursor() as cursor:
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

def get_data_from_previnity(num_cpf):
	response = requests.get(f"{PREVINITY_URL}?usuario={PREVINITY_USER}&senha={PREVINITY_PASS}&ws=S&tipocons=pnn006&cpfcnpj={num_cpf}",verify = True)
	return response.content

def extract_addresses_from_previnity(response):
    root = ET.fromstring(response)
    telefones= root.find('telefone_proprietario').findall('informacoes')
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
            'telefone': tel.find('telefone').text,
            'dt_instalacao': tel.find('istalacao').text
        }
        addresses.append(address)
    # Remove duplicate addresses
    addresses = [ast.literal_eval(s) for s in set([str(d) for d in addresses])]
    return addresses

# Nome deve ser mudado na próxima versão (credilink -> previnity)
def get_whereabouts_credilink(num_cpf):
    response = get_data_from_previnity(num_cpf)
    addresses = extract_addresses_from_previnity(response)
    whereabouts = {'type': 'credilink'}
    whereabouts['formatted_addresses'] = addresses
    return whereabouts
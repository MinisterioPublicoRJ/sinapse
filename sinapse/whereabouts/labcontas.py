from impala.dbapi import connect
from decouple import config

IMPALA_HOST = config('BDA_URL')
IMPALA_PORT = config('IMPALA_PORT', default=21050, cast=int)

def get_whereabouts_lc(num_cpf):
    whereabouts = {'type': 'labcontas'}

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
        for data in cursor.fetchall():
            address = {
                'tipo_logradouro': data[0], 
                'descr_logradouro': data[1],
                'num_logradouro': data[2],
                'descr_complemento_logradouro': data[3],
                'nome_bairro': data[4],
                'num_cep': data[5],
                'nome_municipio': data[6],
                'sigla_uf': data[7],
                'num_ddd': data[8],
                'num_telefone': data[9]
            }
            whereabouts['formatted_addresses'] = address

    return whereabouts
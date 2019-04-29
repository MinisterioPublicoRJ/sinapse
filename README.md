[![Build Status](https://travis-ci.org/MinisterioPublicoRJ/sinapse.svg?branch=master)](https://travis-ci.org/MinisterioPublicoRJ/sinapse)
[![Coverage Status](https://codecov.io/gh/MinisterioPublicoRJ/sinapse/branch/master/graph/badge.svg)](https://codecov.io/gh/MinisterioPublicoRJ/sinapse) 
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/664b2e55beb940bea57b853d61fab391)](https://www.codacy.com/app/SamambaMan/sinapse?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=MinisterioPublicoRJ/sinapse&amp;utm_campaign=Badge_Grade)

# Sinapse

Ferramenta gráfica de análise de vínculo, conectando dados oficiais da Receita, DETRAN, dentre outros órgãos.


## Objetivo
Encontrar padrões e conexões muitas vezes não evidentes entre servidores, pessoas físicas e jurídicas em contratos com o Estado, de forma gráfica e intuitiva, a fim de facilitar a análise das promotorias de justiça podendo trazer *insights* de onde pode partir uma investigação, ou prover insumos para inquéritos já em curso.

As buscas podem ser relacionadas a parentesco, relação societária, propriedades, bens, utilizando os caminhos que estas conexões fazem, que podem muitas vezes em conflito de interesse com a sociedade civil.

![Sinapse](sinapse.png)

## Configuração e ambiente

O projeto utiliza decouple para variáveis de configuração e ambiente, é necessário utilizar um arquivo *settings.ini* ou exportar no ambiente as seguintes variáveis:

```
NEO4J_USUARIO=(usuário do banco Neo4J)
NEO4J_SENHA=(senha do usuário)
NEO4J_DOMINIO=(FQDN do banco Neo4J)
MONGO_USUARIO=(usuário do banco MongoDB para log de acesso)
MONGO_SENHA=(senha do usuário MongoDB)
MONGO_HOST=(host do MongoDB)
MONGO_AUTHDB=(domínio de autorização)
SECRET=(secret key única segura)
AUTH_MPRJ=(FQDN do autorizador web MPRJ)
USERINFO_MPRJ=(FQDN do sistema de roles MPRJ)
DEV=True/False(Em DEV não precisa de autenticação)
SISTEMAS=???
```

## Dependências, Instalação e Execução

O projeto foi testado nas versões 3.5 e 3.6 do Python.

Para instalação das dependências do projeto é necessário instalar os pacotes da seguinte forma:

### Configurando ambiente no Linux

    sudo apt-get install redis-server
    virtualenv venv
    source venv/bin/activate
    pip install -r dev-requirements.txt

### Configurando ambiente no Mac

    brew install redis
    brew services start redis
    virtualenv --python=$(which python3.6) venv
    source venv/bin/activate
    pip install -r dev-requirements.txt

### Rodando no Linux ou Mac

Você precisará abrir dois terminais. No primeiro:

    source venv/bin/activate
    export WORKER=1
    sh app.sh

No segundo:

    source venv/bin/activate
    sh app.sh

Caso você tenha o erro

    app.sh: line X: syntax error: unexpected end of file

execute

    vim app.sh
    :set fileformat=unix
    :wq

### Desenvolvendo no Windows

    virtualenv venv
    venv\bin\activate.bat
    pip install -r dev-requirements.txt

### Rodando no Windows

    venv\bin\activate.bat
    app.bat

O servidor *waitress* está configurado para rodar no endereço:
`http://127.0.0.1:8080`

## Endpoints

A API exposta pelo backend tem os seguintes endpoints:

### /api/labels

Retorna array de strings com os tipos de entidades disponíveis.

### /api/search?q=

Retorna entidades que contenham os termos buscados.

    {
        "tipo_da_entidade": {
            "highlighting": {
                "id_aleatorio": {
                    "chave": [
                        "<em>texto que deu match</em>"
                    ]
                }
            },
            "response": {
                "docs": [
                    {
                        "chave": "valor",
                        "uuid": "id único"
                    }
                ],
                "numFound": quantidade_de_elementos_encontrados,
                "start": item_inicial_retornado_(0)
            }
        }
    }

### /api/nodeProperties?label=

Retorna objeto com as propriedades disponíveis para a entidade buscada, no formato:

    {
        "columns": [
            "keys(n)"
        ],
        "data": [
            [
                [
                    "prop1", "prop2"
                ]
            ]
        ]
    }

### /api/findNodes?label=&prop=&val=

Retorna as propriedades de uma dada entidade, em um objeto no formato:

    {
        "nodes": [
            "id": 1,
            "type": [
                "type1"
            ],
            "properties": {
                "prop1": "val1"
            }
        ]
    }

### /api/nextNodes?node_id=

Retorna as ligações de uma dada entiade, em um objeto no formato:

    {
        "edges": [
            {
                "arrows":"to",
                "dashes":false,
                "from":"1",
                "to":"2"
                "id":"3",
                "label":"um label",
                "properties":{
                    "prop1":"val1"
                },
            }
        ],
        "nodes":[
            {
                "id":"1",
                "properties":{
                    "prop1": "val1"
                },
                "type":[
                    "type1"
                ]
            }
        ]
    }

### /api/foto?rg=1234 ou api/foto?node_id=1234

Busca da foto de uma pessoa no DETRAN. A resposta é objeto vazio (```{}```) ou um objeto no formato:

    {
        "imagem": "foto em base 64",
        "rg": "número do rg",
        "tipo": "pessoa",
        "uuid": "identificador único da pessoa no banco"
    }

### /api/foto-veiculo?caracteristicas=VW/SANTANA 2000 MI 1998 CINZA

Busca da foto do veículo. As caracteristicas são o resultado da concatenação separada por espaço da marca, modelo e cor do veículo. A resposta é um objeto vazio (```{}```) ou um objeto no formato:

    {
        "caracteristicas": "string passada",
        "imagem": "foto em base64",
        "tipo": "veiculo",
        "uuid": "identificador único do veículo no banco"
    }

### /api/findShortestPath?node_id1=1234&node_id2=5678&rel_types=opcional"

Busca do caminho mais curto entre dois nós

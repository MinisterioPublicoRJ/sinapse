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
```

## Dependências, Instalação e Execução

O projeto foi testado nas versões 3.5 e 3.6 do Python.

Para instalação das dependências do projeto é necessário instalar os pacotes da seguinte forma:

### Configurando ambiente no Linux

    virtualenv venv
    source venv/bin/activate
    pip install -r dev-requirements.txt

### Configurando ambiente no Mac

    virtualenv --python=$(which python3.6) venv
    source venv/bin/activate
    pip install -r dev-requirements.txt

### Rodando no Linux ou Mac

    source venv/bin/activate
    sh app.sh

### Desenvolvendo no Windows

    virtualenv venv
    venv\bin\activate.bat
    pip install -r dev-requirements.txt

### Rodando no Windows

    venv\bin\activate.bat
    app.bat

O servidor *waitress* está configurado para rodar no endereço:  
`http://127.0.0.1:8080`

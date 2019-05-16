import responses


request_node_ok = {
    'statements': [
        {
            'statement': 'MATCH  (n) where id(n) = 395989945 return n',
            'resultDataContents': [
                'graph'
            ]
        }
    ]
}

resposta_node_ok = {
    'results': [
        {
            'columns': ['a'],
            'data': [
                {
                    'graph': {
                        'nodes': [
                            {
                                'id': '140885160',
                                'labels': ['pessoa'],
                                'properties': {
                                    'nome_pai': 'FRANCISCO IVAN FONTELE BELCHIOR',
                                    'filho_rel_status_pai': 1,
                                    'nome': 'DANIEL CARVALHO BELCHIOR',
                                    'uuid': '607056258864169709',
                                    'idade': 36,
                                    'uf': 'RJ',
                                    'rg': '131242950',
                                    'visitado': False,
                                    'cpf': '11452244740',
                                    'filho_rel_status': 1,
                                    'nome_mae': 'MARTA CARVALHO BELCHIOR',
                                    'sexo': '1',
                                    'nome_rg': 'DANIEL CARVALHO BELCHIOR',
                                    'dt_nasc': '19850522'
                                },
                                'type': [],
                            }
                        ],
                        'relationships': [
                            {
                                'id': 1,
                                'labels': [],
                                'type': [],
                                'startNode': 1,
                                'endNode': 2
                            }
                        ]
                    }
                }
            ]
        }
    ],
    'errors': []
}

resposta_node_sensivel_ok = {
    'errors': [],
    'results': [
        {
            'columns': ['n'],
            'data': [
                {
                    'graph': {
                        'nodes': [
                            {
                                'id': '395989945',
                                'labels': ['personagem'],
                                'properties': {
                                    'cpf': '11452244740',
                                    'nome': 'DANIEL CARVALHO BELCHIOR',
                                    'pess_dk': 15535503,
                                    'sensivel': True,
                                }
                            }],
                        'relationships': []
                    }
                }
            ]
        }
    ]
}

nos_sensiveis_esp = [
        {
            'id': '395989945',
            'labels': ['sigiloso'],
            'properties': {
            }
        }
]


relacoes_sensiveis = [{
    'id': '282346165',
    'type': 'filho',
    'startNode': '12075099',
    'endNode': '10844320',
    'properties': {'sensivel': True},
    }]

relacoes_sensiveis_esp = [{
    'id': '282346165',
    'type': 'sigiloso',
    'startNode': '12075099',
    'endNode': '10844320',
    'properties': {},
    }]

resposta_node_sensivel_esp = {
    'errors': [],
    'results': [
        {
            'columns': ['n'],
            'data': [
                {
                    'graph': {
                        'nodes': [
                            {
                                'id': '395989945',
                                'labels': ['sigiloso'],
                                'properties': {
                                }
                            }],
                        'relationships': []
                    }
                }
            ]
        }
    ]
}


request_filterNodes_ok = {
    'statements': [
        {'statement': "MATCH (n: pessoa { "
         "nome:toUpper('DANIEL CARVALHO BELCHIOR')}) return n limit 100",
         'resultDataContents': [
             'row',
             'graph'
         ]
         }
    ]
}


resposta_filterNodes_ok = {
    'results': [
        {
            'columns': ['r', 'n', 'x'], 
'data': [{
    'graph': {
        'nodes': [{
            'id': '140885160',
            'type': ['pessoa'],
            'properties': {
                'cpf': '11452244740',
                'dt_nasc': '19850522',
                'filho_rel_status': 1,
                'filho_rel_status_pai': 1,
                'nome': 'DANIEL CARVALHO BELCHIOR',
                'nome_mae': 'MARTA CARVALHO BELCHIOR',
                'nome_pai': 'FRANCISCO IVAN FONTELE BELCHIOR',
                'nome_rg': 'DANIEL CARVALHO BELCHIOR',
                'rg': '131242950',
                'sexo': '1',
                'uf': 'RJ',
                'visitado': False,
            },
            'labels': [],
        }],
        'edges': [], 
        'relationships': [{
            'id': '282236618',
            'type': 'filho',
            'startNode': '85604696',
            'endNode': '10844320',
            'properties': {},
    }]
    }}]
}]}

request_nextNodes_ok = {
    'statements': [
        {
            'statement': 'MATCH r = (n)-[*..1]-(x) '
            'where id(n) = 395989945 return r,n,x limit 100',
            'resultDataContents': ['row', 'graph']}
    ]
}

resposta_nextNodes_ok = {'results': [
        {
            'columns': ['r', 'n', 'x'], 
'data': [{
    'graph': {
    'nodes': [
        {
            'id': '395989945',
            'type': ['personagem'],
            'properties': {
                'cpf': '11452244740',
                'nome': 'DANIEL CARVALHO BELCHIOR',
                'pess_dk': 15535503
            },
            'labels': [],
            'type': []
        },
        {
            'id': '359754850',
            'type': ['mgp'],
            'properties': {
                'cdorgao': 400749,
                'classe': 'Notícia de Fato',
                'docu_dk': 17430731,
                'dt_cadastro': '12/01/2018 15:46:42',
                'nr_mprj': 201800032105
            },
            'labels': [],
            'type': []
        },
        {
            'id': '140885160',
            'type': ['pessoa'],
            'properties': {
                'cpf': '11452244740',
                'dt_nasc': '19850522',
                'filho_rel_status': 1,
                'filho_rel_status_pai': 1,
                'nome': 'DANIEL CARVALHO BELCHIOR',
                'nome_mae': 'MARTA CARVALHO BELCHIOR',
                'nome_pai': 'FRANCISCO IVAN FONTELE BELCHIOR',
                'nome_rg': 'DANIEL CARVALHO BELCHIOR',
                'rg': '131242950',
                'sexo': '1',
                'uf': 'RJ',
                'visitado': False
            },
            'labels': [],
            'type': []
        }
    ],
    'edges': [
        {
            'to': '359754850',
            'id': '256806410',
            'properties': {
                'papel': 'NOTICIANTE'
            },
            'from': '395989945',
            'arrows': 'to',
            'dashes': False,
            'label': 'personagem'
        },
        {
            'to': '395989945',
            'id': '277481565',
            'properties': {
                'papel': 'NOTICIANTE'
            },
            'from': '140885160',
            'arrows': 'to',
            'dashes': False,
            'label': 'personagem'
        }
    ],
        'relationships': [
            {
                'id': 1,
                'type': 'person',
                'startNode': 1,
                'endNode': 2
            }
        ]
    }}]}],
    'numero_de_expansoes': [73, 73, 73]
}


resposta_sensivel_mista = {
    'results': [
        {
            'columns': ['r', 'n', 'x'], 
            'data': [{
                'graph': {
                    'nodes': [{'id': '85604696', 'labels': ['pessoa'],
                    'properties': {
                        'uf': 'RJ',
                        'nome_pai': 'E P R',
                        'rg': '0004',
                        'cpf': '0004',
                        'filho_rel_status': 1,
                        'filho_rel_status_pai': 8,
                        'nome_mae': 'M H P R',
                        'nome': 'N R P',
                        'sexo': '2',
                        'nome_rg': 'N R P',
                        'dt_nasc': '20180709',
                        }}, {'id': '10844320', 'labels': ['pessoa'], 'properties': {
                        'uf': 'RJ',
                        'cpf': '005',
                        'nome_mae': 'H M P',
                        'nome': 'M H P R',
                        'sensivel': True,
                        'sexo': '2',
                        'dt_nasc': '20180709',
                        }}], 'relationships': [{
                        'id': '282236618',
                        'type': 'filho',
                        'startNode': '85604696',
                        'endNode': '10844320',
                        'properties': {},
    }]}}, {'graph': {'nodes': [{'id': '12075099', 'labels': ['pessoa'],
                  'properties': {
    'uf': 'RJ',
    'nome_pai': 'E P R',
    'rg': '008',
    'cpf': '008',
    'filho_rel_status': 1,
    'filho_rel_status_pai': 8,
    'nome_mae': 'M H P R',
    'nome': 'A P R',
    'sensivel': True,
    'sexo': '1',
    'nome_rg': 'A P R',
    'dt_nasc': '20180709',
    }}, {'id': '10844320', 'labels': ['pessoa'], 'properties': {
    'uf': 'RJ',
    'cpf': '020',
    'nome_mae': 'H M P',
    'nome': 'M H P R',
    'sensivel': True,
    'sexo': '2',
    'dt_nasc': '20180709',
    }}], 'relationships': [{
    'id': '282346165',
    'type': 'filho',
    'startNode': '12075099',
    'endNode': '10844320',
    'properties': {'sensivel': True},
    }]}}, 
        {'graph': {'nodes': [{'id': '57161336', 'labels': ['pessoa'],
                  'properties': {
    'uf': 'RJ',
    'nome_pai': 'E P R',
    'rg': '011',
    'cpf': '011',
    'filho_rel_status': 1,
    'filho_rel_status_pai': 8,
    'nome_mae': 'M H P R',
    'nome': 'S P R',
    'sexo': '1',
    'nome_rg': 'S P R',
    'dt_nasc': '20180709',
    }}, {'id': '10844320', 'labels': ['pessoa'], 'properties': {
    'uf': 'RJ',
    'cpf': '020',
    'nome_mae': 'H M P',
    'nome': 'M H P R',
    'sensivel': True,
    'sexo': '2',
    'dt_nasc': '20180709',
    }}], 'relationships': [{
    'id': '286160836',
    'type': 'filho',
    'startNode': '57161336',
    'endNode': '10844320',
    'properties': {},
    }]}}, 
        {'graph': {'nodes': [{'id': '10844320', 'labels': ['pessoa'],
                  'properties': {
    'uf': 'RJ',
    'cpf': '015',
    'nome_mae': 'H M P',
    'nome': 'M H P R',
    'sensivel': True,
    'sexo': '2',
    'dt_nasc': '20180709',
    }}, {'id': '116929750', 'labels': ['pessoa'], 'properties': {
    'uf': 'RJ',
    'nome_pai': 'E P R',
    'rg': '016',
    'cpf': '016',
    'filho_rel_status_pai': 8,
    'filho_rel_status': 1,
    'nome_mae': 'M H P R',
    'nome': 'M T R DE A',
    'sexo': '2',
    'nome_rg': 'M T R DE A',
    'dt_nasc': '20180709',
    }}], 'relationships': [{
    'id': '288798795',
    'type': 'filho',
    'startNode': '116929750',
    'endNode': '10844320',
    'properties': {},
    }]}}]}], 'errors': []}

resposta_sensivel_mista_esp = {
    'results': [{'columns': ['r', 'n', 'x'], 'data': [{
        'graph': {'nodes': [{'id': '85604696', 'labels': ['pessoa'],
                  'properties': {
    'uf': 'RJ',
    'nome_pai': 'E P R',
    'rg': '0004',
    'cpf': '0004',
    'filho_rel_status': 1,
    'filho_rel_status_pai': 8,
    'nome_mae': 'M H P R',
    'nome': 'N R P',
    'sexo': '2',
    'nome_rg': 'N R P',
    'dt_nasc': '20180709',
    }}, {'id': '10844320', 'labels': ['sigiloso'], 'properties': {
    }}], 'relationships': [{
    'id': '282236618',
    'type': 'filho',
    'startNode': '85604696',
    'endNode': '10844320',
    'properties': {},
    }]}}, {
        'graph': {'nodes': [{'id': '12075099', 'labels': ['sigiloso'],
                  'properties': {
    }}, {'id': '10844320', 'labels': ['sigiloso'], 'properties': {
    }}], 'relationships': [{
    'id': '282346165',
    'type': 'sigiloso',
    'startNode': '12075099',
    'endNode': '10844320',
    'properties': {},
    }]}}, {
        'graph': {'nodes': [{'id': '57161336', 'labels': ['pessoa'],
                  'properties': {
    'uf': 'RJ',
    'nome_pai': 'E P R',
    'rg': '011',
    'cpf': '011',
    'filho_rel_status': 1,
    'filho_rel_status_pai': 8,
    'nome_mae': 'M H P R',
    'nome': 'S P R',
    'sexo': '1',
    'nome_rg': 'S P R',
    'dt_nasc': '20180709',
    }}, {'id': '10844320', 'labels': ['sigiloso'], 'properties': {
    }}], 'relationships': [{
    'id': '286160836',
    'type': 'filho',
    'startNode': '57161336',
    'endNode': '10844320',
    'properties': {},
    }]}}, {
        'graph': {'nodes': [{'id': '10844320', 'labels': ['sigiloso'],
                  'properties': {
    }}, {'id': '116929750', 'labels': ['pessoa'], 'properties': {
    'uf': 'RJ',
    'nome_pai': 'E P R',
    'rg': '016',
    'cpf': '016',
    'filho_rel_status_pai': 8,
    'filho_rel_status': 1,
    'nome_mae': 'M H P R',
    'nome': 'M T R DE A',
    'sexo': '2',
    'nome_rg': 'M T R DE A',
    'dt_nasc': '20180709',
    }}], 'relationships': [{
    'id': '288798795',
    'type': 'filho',
    'startNode': '116929750',
    'endNode': '10844320',
    'properties': {},
    }]}}]}], 'errors': []}

request_nodeproperties_ok = {
    'query': 'MATCH (n:pessoa)  RETURN  keys(n) limit 1'
}

resposta_nodeproperties_ok = {
    'columns': ['keys(n)'],
    'data': [
        [['nome_mae', 'cpf', 'dt_nasc', 'sexo', 'uf', 'nome']]
    ]
}

resposta_label_ok = [
    'multa',
    'veiculo',
    'personagem',
    'telefone',
    'mgp',
    'empresa',
    'orgao',
    'pessoa'
]

resposta_relationships_ok = [
    'filho',
    'proprietario',
    'autuado',
    'socio',
    'membro',
    'membro_inativo',
    'servidor_mprj',
    'responsavel',
    'personagem',
    'orgao_responsavel',
    'telefonema'
]

request_nextNodes_doisfiltros_ok = {
    'statements': [
        {
            'statement': 'MATCH r = (n)-[:filho|:trabalha*..1]-(x) '
            'where id(n) = 395989945 return r,n,x limit 100',
            'resultDataContents': ['row', 'graph']}
    ]
}

resposta_nextNodes_doisfiltros_ok = {
    "edges":[
        {
            "arrows":"to",
            "dashes":False,
            "from":"140885160",
            "id":"324218666",
            "label":"trabalha",
            "properties":{
                "dt_admissao":"29102013",
                "vinculo":"Servidor p\ufffdblico n\ufffdo-efetivo (demiss\ufffdvel ad nutum ou admitido por meio "
                    "de legisla\ufffd\ufffdo especial, n\ufffdo-regido pela CLT)."
            },
            "to":"329437779"
        },
        {
            "arrows":"to",
            "dashes":False,
            "from":"205537878",
            "id":"288234032",
            "label":"filho",
            "properties":{},
            "to":"140885160"
        },
        {
            "arrows":"to",
            "dashes":False,
            "from":"205176041",
            "id":"288487160",
            "label":"filho",
            "properties":{},
            "to":"140885160"
        },
        {
            "arrows":"to",
            "dashes":False,
            "from":"411356688",
            "id":"298556380",
            "label":"filho",
            "properties":{},
            "to":"140885160"
        },
        {
            "arrows":"to",
            "dashes":False,
            "from":"140885160",
            "id":"280039851",
            "label":"filho",
            "properties":{},
            "to":"119932160"
        },
        {
            "arrows":"to",
            "dashes":False,
            "from":"140885160",
            "id":"281035845",
            "label":"filho",
            "properties":{},
            "to":"107380408"
        }
    ],
    "nodes":[
        {
            "id":"329437779",
            "properties":{
                "cnae":"8411600",
                "cnpj":"28305936000140",
                "cpf_responsavel":"01090266758",
                "data_inicio":"19830829",
                "filial":"1",
                "municipio":"RIO DE JANEIRO",
                "nome_responsavel":"MARCELO VIEIRA DE AZEVEDO",
                "razao_social":"MINISTERIO PUBLICO DO ESTADO DO RIO DE JANEIRO",
                "uf":"RJ"
            },
            "type":["empresa"]
        },
        {
            "id":"140885160",
            "properties":{
                "cpf":"11452244740",
                "dt_nasc":"19850522",
                "filho_rel_status":1,
                "filho_rel_status_pai":1,
                "nome":"DANIEL CARVALHO BELCHIOR",
                "nome_mae":"MARTA CARVALHO BELCHIOR",
                "nome_pai":"FRANCISCO IVAN FONTELE BELCHIOR",
                "nome_rg":"DANIEL CARVALHO BELCHIOR",
                "rg":"131242950",
                "sexo":"1",
                "uf":"RJ",
                "visitado":False
            },
            "type":["pessoa"]
        },
        {
            "id":"205537878",
            "properties":{
                "cpf":"17937488700",
                "dt_nasc":"20120924",
                "filho_rel_status":7,
                "filho_rel_status_pai":1,
                "nome":"LUIZA LIMA DE ALMEIDA BELCHIOR",
                "nome_mae":"SILVIA LIMA DE ALMEIDA",
                "nome_pai":"DANIEL CARVALHO BELCHIOR",
                "nome_rg":"LUIZA LIMA DE ALMEIDA BELCHIOR",
                "rg":"298572447",
                "sexo":"2",
                "uf":"RJ"
            },
            "type":["pessoa"]
        },
        {
            "id":"205176041",
            "properties":{
                "cpf":"17902261718",
                "dt_nasc":"20090320",
                "filho_rel_status":7,
                "filho_rel_status_pai":1,
                "nome":"MARCOS CESAR LIMA DE ALMEIDA BELCHIOR",
                "nome_mae":"SILVIA LIMA DE ALMEIDA",
                "nome_pai":"DANIEL CARVALHO BELCHIOR",
                "nome_rg":"MARCOS CESAR LIMA DE ALMEIDA BELCHIOR",
                "rg":"308716588",
                "sexo":"1",
                "uf":"RJ"
            },
            "type":["pessoa"]
        },
        {
            "id":"411356688",
            "properties":{
                "cpf":"20102028729",
                "dt_nasc":"20170725",
                "filho_rel_status_pai":1,
                "nome":"JULIA LIMA DE ALMEIDA BELCHIOR",
                "nome_mae":"SILVIA LIMA DE ALMEIDA",
                "nome_pai":"DANIEL CARVALHO BELCHIOR",
                "nome_rg":"JULIA LIMA DE ALMEIDA BELCHIOR",
                "origem":"DETRAN",
                "rg":"332462886",
                "uf":"RJ"
            },
            "type":["pessoa"]
        },
        {
            "id":"119932160",
            "properties":{
                "cpf":"77626591704",
                "dt_nasc":"19640427",
                "filho_rel_status":6,
                "filho_rel_status_pai":6,
                "nome":"MARTA LIMA CARVALHO",
                "nome_mae":"RUTH LIMA CARVALHO",
                "nome_pai":"ANTONIO SILVEIRA CARVALHO",
                "nome_rg":"MARTA CARVALHO BELCHIOR",
                "rg":"66900655",
                "sexo":"2",
                "uf":"RJ"
            },
            "type":["pessoa"]
        },
        {
            "id":"107380408",
            "properties":{
                "cpf":"66760607791",
                "dt_nasc":"19610502",
                "filho_rel_status":1,
                "filho_rel_status_pai":1,
                "nome":"FRANCISCO IVAN FONTELE BELCHIOR",
                "nome_mae":"VANDA FONTELE BELCHIOR",
                "nome_pai":"BENEDITO CHAVES BELCHIOR",
                "nome_rg":"FRANCISCO IVAN FONTELE BELCHIOR",
                "rg":"39846522",
                "sexo":"1",
                "uf":"RJ"
            },
            "type":["pessoa"]
        }
    ],
    'numero_de_expansoes': [73, 73, 73]
}

request_nextNodes_umfiltro_ok = {
    'statements': [
        {
            'statement': 'MATCH r = (n)-[:filho*..1]-(x) '
            'where id(n) = 395989945 return r,n,x limit 100',
            'resultDataContents': ['row', 'graph']}
    ]
}

resposta_nextNodes_umfiltro_ok = {
    "edges":[
        {
            "arrows":"to",
            "dashes":False,
            "from":"205537878",
            "id":"288234032",
            "label":"filho",
            "properties":{},
            "to":"140885160"
        },
        {
            "arrows":"to",
            "dashes":False,
            "from":"205176041",
            "id":"288487160",
            "label":"filho",
            "properties":{},
            "to":"140885160"
        },
        {
            "arrows":"to",
            "dashes":False,
            "from":"411356688",
            "id":"298556380",
            "label":"filho",
            "properties":{},
            "to":"140885160"
        },
        {
            "arrows":"to",
            "dashes":False,
            "from":"140885160",
            "id":"280039851",
            "label":"filho",
            "properties":{},
            "to":"119932160"
        },
        {
            "arrows":"to",
            "dashes":False,
            "from":"140885160",
            "id":"281035845",
            "label":"filho",
            "properties":{},
            "to":"107380408"
        }
    ],
    "nodes":[
        {
            "id":"205537878",
            "properties":{
                "cpf":"17937488700",
                "dt_nasc":"20120924",
                "filho_rel_status":7,
                "filho_rel_status_pai":1,
                "nome":"LUIZA LIMA DE ALMEIDA BELCHIOR",
                "nome_mae":"SILVIA LIMA DE ALMEIDA",
                "nome_pai":"DANIEL CARVALHO BELCHIOR",
                "nome_rg":"LUIZA LIMA DE ALMEIDA BELCHIOR",
                "rg":"298572447",
                "sexo":"2",
                "uf":"RJ"
            },
            "type":["pessoa"]
        },
        {
            "id":"140885160",
            "properties":{
                "cpf":"11452244740",
                "dt_nasc":"19850522",
                "filho_rel_status":1,
                "filho_rel_status_pai":1,
                "nome":"DANIEL CARVALHO BELCHIOR",
                "nome_mae":"MARTA CARVALHO BELCHIOR",
                "nome_pai":"FRANCISCO IVAN FONTELE BELCHIOR",
                "nome_rg":"DANIEL CARVALHO BELCHIOR",
                "rg":"131242950",
                "sexo":"1",
                "uf":"RJ",
                "visitado":False
            },
            "type":["pessoa"]
        },
        {
            "id":"205176041",
            "properties":{
                "cpf":"17902261718",
                "dt_nasc":"20090320",
                "filho_rel_status":7,
                "filho_rel_status_pai":1,
                "nome":"MARCOS CESAR LIMA DE ALMEIDA BELCHIOR",
                "nome_mae":"SILVIA LIMA DE ALMEIDA",
                "nome_pai":"DANIEL CARVALHO BELCHIOR",
                "nome_rg":"MARCOS CESAR LIMA DE ALMEIDA BELCHIOR",
                "rg":"308716588",
                "sexo":"1",
                "uf":"RJ"
            },
            "type":["pessoa"]
        },
        {
            "id":"411356688",
            "properties":{
                "cpf":"20102028729",
                "dt_nasc":"20170725",
                "filho_rel_status_pai":1,
                "nome":"JULIA LIMA DE ALMEIDA BELCHIOR",
                "nome_mae":"SILVIA LIMA DE ALMEIDA",
                "nome_pai":"DANIEL CARVALHO BELCHIOR",
                "nome_rg":"JULIA LIMA DE ALMEIDA BELCHIOR",
                "origem":"DETRAN",
                "rg":"332462886",
                "uf":"RJ"
            },
            "type":["pessoa"]
        },
        {
            "id":"119932160",
            "properties":{
                "cpf":"77626591704",
                "dt_nasc":"19640427",
                "filho_rel_status":6,
                "filho_rel_status_pai":6,
                "nome":"MARTA LIMA CARVALHO",
                "nome_mae":"RUTH LIMA CARVALHO",
                "nome_pai":"ANTONIO SILVEIRA CARVALHO",
                "nome_rg":"MARTA CARVALHO BELCHIOR",
                "rg":"66900655",
                "sexo":"2",
                "uf":"RJ"
            },
            "type":["pessoa"]
        },
        {
            "id":"107380408",
            "properties":{
                "cpf":"66760607791",
                "dt_nasc":"19610502",
                "filho_rel_status":1,
                "filho_rel_status_pai":1,
                "nome":"FRANCISCO IVAN FONTELE BELCHIOR",
                "nome_mae":"VANDA FONTELE BELCHIOR",
                "nome_pai":"BENEDITO CHAVES BELCHIOR",
                "nome_rg":"FRANCISCO IVAN FONTELE BELCHIOR",
                "rg":"39846522",
                "sexo":"1",
                "uf":"RJ"
            },
            "type":["pessoa"]
        }
    ],
    'numero_de_expansoes': [73, 73, 73]
}

request_findShortestPath_doisfiltros_ok = {
    "statements": [
        {
        "statement": "MATCH p = allShortestPaths((a)-[:filho|:personagem*]-(b)) "
            "WHERE id(a) = 140885160 AND id(b) = 328898991 RETURN p",
        "resultDataContents": ["row", "graph"]
        }
    ]
}

resposta_findShortestPath_doisfiltros_ok = {
    "edges":[],
    "nodes":[]
} 

request_findShortestPath_umfiltro_ok = {
    "statements": [
        {
        "statement": "MATCH p = allShortestPaths((a)-[:trabalha*]-(b)) "
            "WHERE id(a) = 140885160 AND id(b) = 328898991 RETURN p",
        "resultDataContents": ["row", "graph"]
        }
    ]
}

resposta_findShortestPath_umfiltro_ok = {
    "edges":[
        {
            "arrows":"to",
            "dashes":False,
            "from":"170754553",
            "id":"385418473",
            "label":"trabalha",
            "properties":{
                "dt_admissao":"20180119"
            },
            "to":"329437779"
        },
        {
            "arrows":"to",
            "dashes":False,
            "from":"170754553",
            "id":"324980622",
            "label":"trabalha",
            "properties":{
                "dt_admissao":"20180604"
            },
            "to":"304029249"
        },
        {
            "arrows":"to",
            "dashes":False,
            "from":"24000446",
            "id":"384945540",
            "label":"trabalha",
            "properties":{
                "dt_admissao":"20171101"
            },
            "to":"328898991"
        },
        {
            "arrows":"to",
            "dashes":False,
            "from":"140885160",
            "id":"324218666",
            "label":"trabalha",
            "properties":{
                "dt_admissao":"29102013",
                "vinculo":"Servidor p\ufffdblico n\ufffdo-efetivo (demiss\ufffdvel ad nutum ou admitido por meio "
                    "de legisla\ufffd\ufffdo especial, n\ufffdo-regido pela CLT)."
            },
            "to":"329437779"
        },
        {
            "arrows":"to",
            "dashes":False,
            "from":"24000446",
            "id":"324954277",
            "label":"trabalha",
            "properties":{
                "dt_admissao":"20170207"
            },
            "to":"304029249"
        }
    ],
    "nodes":[
        {
            "id":"24000446",
            "properties":{
                "cpf":"07223334711",
                "dt_nasc":"19780523",
                "filho_rel_status":6,
                "filho_rel_status_pai":3,
                "nome":"BIANCA CHAGAS AMANCIO DA SILVA",
                "nome_mae":"SANDRA CHAGAS DA SILVA",
                "nome_pai":"RONALDO AMANCIO DA SILVA",
                "nome_rg":"BIANCA CHAGAS AMANCIO DA SILVA",
                "rg":"104029277",
                "sexo":"2",
                "uf":"RJ"
            },
            "type":["pessoa"]
        },
        {
            "id":"329437779",
            "properties":{
                "cnae":"8411600",
                "cnpj":"28305936000140",
                "cpf_responsavel":"01090266758",
                "data_inicio":"19830829",
                "filial":"1",
                "municipio":"RIO DE JANEIRO",
                "nome_responsavel":"MARCELO VIEIRA DE AZEVEDO",
                "razao_social":"MINISTERIO PUBLICO DO ESTADO DO RIO DE JANEIRO",
                "uf":"RJ"
            },
            "type":["empresa"]
        },
        {
            "id":"170754553",
            "properties":{
                "cpf":"14277070736",
                "dt_nasc":"19900509",
                "filho_rel_status":1,
                "filho_rel_status_pai":1,
                "nome":"MARCIO DOS SANTOS CHAGAS",
                "nome_mae":"ROSANGELA GLORIA DOS SANTOS CHAGAS",
                "nome_pai":"WILTON MORAES DAS CHAGAS",
                "nome_rg":"MARCIO DOS SANTOS CHAGAS",
                "rg":"242651156",
                "sexo":"1",
                "uf":"RJ"
            },
            "type":["pessoa"]
        },
        {
            "id":"328898991",
            "properties":{},
            "type":["sigiloso"]
        },
        {
            "id":"140885160",
            "properties":{
                "cpf":"11452244740",
                "dt_nasc":"19850522",
                "filho_rel_status":1,
                "filho_rel_status_pai":1,
                "nome":"DANIEL CARVALHO BELCHIOR",
                "nome_mae":"MARTA CARVALHO BELCHIOR",
                "nome_pai":"FRANCISCO IVAN FONTELE BELCHIOR",
                "nome_rg":"DANIEL CARVALHO BELCHIOR",
                "rg":"131242950",
                "sexo":"1",
                "uf":"RJ",
                "visitado":False
            },
            "type":["pessoa"]
        },
        {
            "id":"304029249",
            "properties":{
                "cnae":"8220200",
                "cnpj":"02879250005308",
                "cpf_responsavel":"00000000000",
                "data_inicio":"20110914",
                "filial":"2",
                "municipio":"RIO DE JANEIRO",
                "nome_fantasia":"ATENTO BRASIL S/A",
                "nome_responsavel":"CPF NAO CONSTA NA BASE-CPF",
                "razao_social":"ATENTO BRASIL S/A",
                "uf":"RJ"
            },
            "type":["empresa"]
        }
    ]
}

request_findShortestPath_ok = {
    "statements": [
        {
        "statement": "MATCH p = allShortestPaths((a)-[*]-(b)) "
            "WHERE id(a) = 140885160 AND id(b) = 328898991 RETURN p",
        "resultDataContents": ["row", "graph"]
        }
    ]
}

resposta_findShortestPath_ok = {
    "edges": [
        {
            "arrows":"to",
            "dashes":False,
            "from":"81208568",
            "id":"384945543",
            "label":"trabalha",
            "properties":{
                "dt_admissao":"20180601"
                },
            "to":"328898991"
        },
        {
            "arrows":"to",
            "dashes":False,
            "from":"205537878",
            "id":"304651477",
            "label":"filho",
            "properties":{},
            "to":"81208568"
        },
        {
            "arrows":"to",
            "dashes":False,
            "from":"205537878",
            "id":"288234032",
            "label":"filho",
            "properties":{},
            "to":"140885160"
        }
    ],
    "nodes":[
        {
            "id":"328898991",
            "properties":{},
            "type":["sigiloso"]
        },
        {
            "id":"205537878",
            "properties":{
                "cpf":"17937488700",
                "dt_nasc":"20120924",
                "filho_rel_status":7,
                "filho_rel_status_pai":1,
                "nome":"LUIZA LIMA DE ALMEIDA BELCHIOR",
                "nome_mae":"SILVIA LIMA DE ALMEIDA",
                "nome_pai":"DANIEL CARVALHO BELCHIOR",
                "nome_rg":"LUIZA LIMA DE ALMEIDA BELCHIOR",
                "rg":"298572447",
                "sexo":"2",
                "uf":"RJ"},
            "type":["pessoa"]
        },
        {
            "id":"140885160",
            "properties":{
                "cpf":"11452244740",
                "dt_nasc":"19850522",
                "filho_rel_status":1,
                "filho_rel_status_pai":1,
                "nome":"DANIEL CARVALHO BELCHIOR",
                "nome_mae":"MARTA CARVALHO BELCHIOR",
                "nome_pai":"FRANCISCO IVAN FONTELE BELCHIOR",
                "nome_rg":"DANIEL CARVALHO BELCHIOR",
                "rg":"131242950",
                "sexo":"1",
                "uf":"RJ",
                "visitado":False},
            "type":["pessoa"]
        },
        {
            "id":"81208568",
            "properties":{
                "cpf":"10069222703",
                "dt_nasc":"19820723",
                "filho_rel_status":3,
                "filho_rel_status_pai":1,
                "nome":"SILVIA LIMA DE ALMEIDA",
                "nome_mae":"MARIA FREITAS DE LIMA",
                "nome_pai":"AMARO JOSE DE ALMEIDA PINHEIRO",
                "nome_rg":"SILVIA LIMA DE ALMEIDA",
                "rg":"203556378",
                "sexo":"2",
                "uf":"RJ"},
            "type":["pessoa"]
        }
    ]
}

casos_servicos = [
    {
        'nome': 'api_relationships',
        'endereco': '/db/data/relationship/types',
        'servico': '/api/relationships',
        'resposta': resposta_relationships_ok,
        'requisicao': None,
        'query_string': {},
        'metodo': responses.GET
    },
]

query_dinamica = [
    {'statement': "optional match (a:pessoa {nome:toUpper('DANIEL CARVALHO BELCHIOR')}) "
                  "optional match (b:personagem {pess_dk:24728287}) return a,b limit 100",
                  'resultDataContents': ['graph']}]

# Vis.js Parser

parser_test_input = {'results': [{'columns': ['p', 'a', 'b'],
    'data': [{'graph': {'nodes': [{'id': '413827112',
        'labels': ['teste2'],
        'properties': {'nome': 'maria'}},
        {'id': '413827111',
        'labels': ['teste'],
        'properties': {'nome': 'jose'}}],
        'relationships': [{'id': '402463320',
        'type': 'relacao',
        'startNode': '413827111',
        'endNode': '413827112',
        'properties': {}}]}},
    {'graph': {'nodes': [{'id': '413827152',
        'labels': ['teste'],
        'properties': {'nome': 'a'}},
        {'id': '413827172', 'labels': ['teste'], 'properties': {'nome': 'b'}}],
        'relationships': [{'id': '402463342',
        'type': 'testeRel',
        'startNode': '413827172',
        'endNode': '413827152',
        'properties': {}}]}},
    {'graph': {'nodes': [{'id': '413827152',
        'labels': ['teste'],
        'properties': {'nome': 'a'}},
        {'id': '413827172', 'labels': ['teste'], 'properties': {'nome': 'b'}}],
        'relationships': [{'id': '402463341',
        'type': 'testeRel',
        'startNode': '413827152',
        'endNode': '413827172',
        'properties': {}}]}},
    {'graph': {'nodes': [{'id': '413827152',
        'labels': ['teste'],
        'properties': {'nome': 'a'}},
        {'id': '413827172', 'labels': ['teste'], 'properties': {'nome': 'b'}}],
        'relationships': [{'id': '402463342',
        'type': 'testeRel',
        'startNode': '413827172',
        'endNode': '413827152',
        'properties': {}}]}},
    {'graph': {'nodes': [{'id': '413827152',
        'labels': ['teste'],
        'properties': {'nome': 'a'}},
        {'id': '413827172', 'labels': ['teste'], 'properties': {'nome': 'b'}}],
        'relationships': [{'id': '402463341',
        'type': 'testeRel',
        'startNode': '413827152',
        'endNode': '413827172',
        'properties': {}}]}}]}],
    'errors': []
}

parser_test_output = {
    'nodes': [
        {
            'id': '413827112',
            'properties': {'nome': 'maria'},
            'type': ['teste2']
        },
        {
            'id': '413827111',
            'properties': {'nome': 'jose'},
            'type': ['teste']
        },
        {
            'id': '413827152',
            'properties': {'nome': 'a'},
            'type': ['teste']
        },
        {
            'id': '413827172',
            'properties': {'nome': 'b'},
            'type': ['teste']
        }
    ],
    'edges': [
        {
            'id': '402463320',
            'properties': {},
            'label': 'relacao',
            'from': '413827111',
            'to': '413827112',
            'arrows': 'to',
            'dashes': False
        },
        {
            'id': '402463342', 
            'properties': {}, 
            'label': 'testeRel', 
            'from': '413827172', 
            'to': '413827152', 
            'arrows': 'to', 
            'dashes': False
        },
        {
            'id': '402463341',
            'properties': {},
            'label': 'testeRel',
            'from': '413827152',
            'to': '413827172',
            'arrows': 'to',
            'dashes': False
        }
    ]
}

# Whereabouts

request_get_node_from_id = {
    'statements': [
        {
            'statement': 'MATCH (n:pessoa) WHERE id(n) = 140885160' 
            ' RETURN n',
            'resultDataContents': ['graph']
        }
    ]
}

resposta_get_node_from_id_ok = {
    'results':[
        {
            'columns': ['n'],
            'data':[
                {
                    'graph': {
                        'nodes': [
                            {
                                'id': '140885160', 
                                'labels': ['pessoa'], 
                                'properties': {
                                    'nome_pai': 'FRANCISCO IVAN FONTELE BELCHIOR', 
                                    'filho_rel_status_pai': 1, 
                                    'nome': 'DANIEL CARVALHO BELCHIOR', 
                                    'uuid': '607056258864169709', 
                                    'idade': 36, 
                                    'uf': 'RJ', 
                                    'rg': '131242950', 
                                    'visitado': False, 
                                    'cpf': '11452244740', 
                                    'filho_rel_status': 1, 
                                    'nome_mae': 'MARTA CARVALHO BELCHIOR', 
                                    'sexo': '1', 
                                    'nome_rg': 'DANIEL CARVALHO BELCHIOR', 
                                    'dt_nasc': '19850522'
                                }
                            }
                        ],
                        'relationships': []
                    }
                }
            ]
        }
    ],
    'errors': []
}

resposta_get_node_from_id_sensivel_ok = {
    'results':[
        {
            'columns': ['n'],
            'data':[
                {
                    'graph': {
                        'nodes': [
                            {
                                'id': '140885160', 
                                'labels': ['pessoa'], 
                                'properties': {
                                    'nome_pai': 'FRANCISCO IVAN FONTELE BELCHIOR', 
                                    'filho_rel_status_pai': 1, 
                                    'nome': 'DANIEL CARVALHO BELCHIOR', 
                                    'uuid': '607056258864169709', 
                                    'idade': 36, 
                                    'uf': 'RJ', 
                                    'rg': '131242950', 
                                    'visitado': False, 
                                    'cpf': '11452244740', 
                                    'filho_rel_status': 1, 
                                    'nome_mae': 'MARTA CARVALHO BELCHIOR', 
                                    'sexo': '1', 
                                    'nome_rg': 'DANIEL CARVALHO BELCHIOR', 
                                    'dt_nasc': '19850522',
                                    'sensivel': True
                                }
                            }
                        ],
                        'relationships': []
                    }
                }
            ]
        }
    ],
    'errors': []
}

input_whereabouts_addresses_receita = [(
    'RUA',
    'DE TESTE',
    '123',
    'APTO 101',
    'BAIRRO DE TESTE',
    '20000000',
    'RIO DE JANEIRO',
    'RJ',
    '21',
    '25696969'
)]

output_whereabouts_addresses_receita = [{
    'endereco': 'RUA DE TESTE', 
    'numero': '123',
    'complemento': 'APTO 101',
    'bairro': 'BAIRRO DE TESTE',
    'cep': '20000000',
    'cidade': 'RIO DE JANEIRO',
    'sigla_uf': 'RJ',
    'telefone': '2125696969'
}]

input_whereabouts_addresses_credilink = ("<?xml version='1.0' encoding='iso-8859-1'?>"
    "<credilink_webservice>"
    "<consulta_telefone_proprietario>"
    "<telefone>"
    "<contador>1</contador><nome>FULANO DE TESTE DA SILVA</nome>"
    "<telefone>2125696969</telefone><dt_istalacao>01/01/2000</dt_istalacao>"
    "<endereco>RUA DE TESTE</endereco><numero>123</numero><complemento>APT 101</complemento>"
    "<bairro>BAIRRO DE TESTE</bairro><cep>20000000</cep><cidade>RIO DE JANEIRO</cidade><uf>RJ</uf>"
    "<cpfcnpj>00000000001</cpfcnpj><sexo>M</sexo><mae>CICLANA DE TESTE</mae>"
    "<nasc>01/01/1990</nasc><titulo_eleitor></titulo_eleitor><statustelefone>1</statustelefone>"
    "<atualizacao>SAT</atualizacao><operadora>EMBRATEL</operadora><procon>(NAO TEM)</procon>"
    "<emails></emails><whatsapp></whatsapp><estadocivil></estadocivil>"
    "</telefone>"
    "<telefone>"
    "<contador>1</contador><nome>FULANO DE TESTE DA SILVA</nome>"
    "<telefone>2138522500</telefone><dt_istalacao>01/01/2002</dt_istalacao>"
    "<endereco>RUA ALPHA BETA</endereco><numero>100</numero><complemento>APT 202</complemento>"
    "<bairro>BAIRRO DE TESTE</bairro><cep>20000000</cep><cidade>RIO DE JANEIRO</cidade><uf>RJ</uf>"
    "<cpfcnpj>00000000001</cpfcnpj><sexo>M</sexo><mae>CICLANA DE TESTE</mae>"
    "<nasc>01/01/1990</nasc><titulo_eleitor></titulo_eleitor><statustelefone>1</statustelefone>"
    "<atualizacao>SAT</atualizacao><operadora>EMBRATEL</operadora><procon>(NAO TEM)</procon>"
    "<emails></emails><whatsapp></whatsapp><estadocivil></estadocivil>"
    "</telefone>"
    "</consulta_telefone_proprietario>"
    "</credilink_webservice>"
)

output_whereabouts_addresses_credilink = [
    {
        'endereco': 'RUA DE TESTE', 
        'numero': '123',
        'complemento': 'APT 101',
        'bairro': 'BAIRRO DE TESTE',
        'cep': '20000000',
        'cidade': 'RIO DE JANEIRO',
        'sigla_uf': 'RJ',
        'telefone': '2125696969'
    },
    {
        'endereco': 'RUA ALPHA BETA', 
        'numero': '100',
        'complemento': 'APT 202',
        'bairro': 'BAIRRO DE TESTE',
        'cep': '20000000',
        'cidade': 'RIO DE JANEIRO',
        'sigla_uf': 'RJ',
        'telefone': '2138522500'
    }
]

resposta_whereabouts_receita_ok = {
    'type': 'receita_federal',
    'formatted_addresses': output_whereabouts_addresses_receita
}

resposta_whereabouts_credilink_ok = {
    'type': 'credilink',
    'formatted_addresses': output_whereabouts_addresses_credilink
}

resposta_whereabouts_ok = [
    resposta_whereabouts_receita_ok, 
    resposta_whereabouts_credilink_ok
]

# Detran
response_rg = b'<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><consultarRGResponse xmlns="http://www.detran.rj.gov.br"><consultarRGResult>0000 - Inclus\xc3\xa3o realizada com sucesso. Aguardar processamento</consultarRGResult></consultarRGResponse></soap:Body></soap:Envelope>'

response_processado_rg=b'<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><BuscarProcessadosResponse xmlns="http://www.detran.rj.gov.br"><BuscarProcessadosResult><dadosCivil><Base>1</Base><IdCidadao>1234</IdCidadao><RG>1234</RG><DtExpedicao>10/10/1990</DtExpedicao><NoCidadao>Nome Cidadao</NoCidadao><NoPaiCidadao>Pai Cidadao</NoPaiCidadao><NoMaeCidadao>Mae Cidadao</NoMaeCidadao><DtNascimento>10/10/1990 00:00:00</DtNascimento><EstadoCivil>1</EstadoCivil><EdLogradouro>rua</EdLogradouro><EdComplemento>100</EdComplemento><EdNumero>1234</EdNumero><EdBairro>Bairro</EdBairro><UFLogradouro>RJ</UFLogradouro><TpCertidao>1</TpCertidao><NuCertidaoLivro>1234</NuCertidaoLivro><NuCertidaoFolha>98</NuCertidaoFolha><NuCertidaoTermo>87294</NuCertidaoTermo><NuCertidaoCircunscricao>8</NuCertidaoCircunscricao><PossuiObito>N</PossuiObito><DtObito /><CoRetorno>1</CoRetorno><MsgRetorno>Cidad\xc3\xa3o encontrado, atrav\xc3\xa9s do RG</MsgRetorno><fotoCivil><string>abcd</string></fotoCivil></dadosCivil></BuscarProcessadosResult></BuscarProcessadosResponse></soap:Body></soap:Envelope>'

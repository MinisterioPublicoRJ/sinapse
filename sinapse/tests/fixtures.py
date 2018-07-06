import responses


request_node_ok = {
    'statements': [
        {
            'statement': (
                'MATCH  (n) where id(n) = 395989945 and'
                ' n.sensivel is null return n'),
            'resultDataContents': [
                'row',
                'graph'
            ]
        }
    ]
}

resposta_node_ok = {
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
                                    'pess_dk': 15535503
                                }
                            }],
                        'relationships': []
                    },
                    'meta': [{
                        'deleted': False,
                        'id': 395989945,
                        'type': 'node'
                    }],
                    'row': [{
                        'cpf': '11452244740',
                        'nome': 'DANIEL CARVALHO BELCHIOR',
                        'pess_dk': 15535503
                    }]
                }
            ]
        }
    ]
}

request_filterNodes_ok = {
    'statements': [
        {'statement': "MATCH (n: pessoa { "
         "nome:toUpper('DANIEL CARVALHO BELCHIOR')}) where n.sensivel is"
         " null return n",
         'resultDataContents': [
             'row',
             'graph'
         ]
         }
    ]
}


resposta_filterNodes_ok = {
    'errors': [],
    'results': [
        {'columns': ['n'],
         'data': [
             {
                 'graph': {
                     'nodes': [{
                         'id': '140885160',
                         'labels': ['pessoa'],
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
                         }
                     }],
                     'relationships': []
                 },
                 'meta': [{
                     'deleted': False,
                     'id': 140885160, 'type': 'node'
                 }],
                 'row': [{
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
                 }]
             }]
         }
    ]
}

request_nextNodes_ok = {
    'statements': [
        {
            'statement': 'MATCH r = (n)-[*..1]-(x) '
            'where id(n) = 395989945 return r,n,x',
            'resultDataContents': ['row', 'graph']}
    ]
}

resposta_nextNodes_ok = {
    'errors': [],
    'results': [
        {'columns': ['r', 'n', 'x'],
         'data': [
            {'graph': {
                'nodes': [
                    {
                        'id': '395989945',
                        'labels': ['personagem'],
                        'properties': {'cpf': '11452244740',
                                       'nome': 'DANIEL '
                                       'CARVALHO '
                                       'BELCHIOR',
                                       'pess_dk': 15535503}},
                    {'id': '359754850',
                     'labels': ['mgp'],
                     'properties': {'cdorgao': 400749,
                                    'classe': 'Notícia '
                                    'de Fato',
                                    'docu_dk': 17430731,
                                    'dt_cadastro': '12/01/2018 '
                                    '15:46:42',
                                    'nr_mprj': 201800032105}}],
                'relationships': [{'endNode': '359754850',
                                   'id': '256806410',
                                   'properties': {'papel': 'NOTICIANTE'},
                                   'startNode': '395989945',
                                   'type': 'personagem'}]},
             'meta': [[{'deleted': False,
                        'id': 395989945,
                        'type': 'node'},
                       {'deleted': False,
                        'id': 256806410,
                        'type': 'relationship'},
                       {'deleted': False,
                        'id': 359754850,
                        'type': 'node'}],
                      {'deleted': False,
                       'id': 395989945,
                       'type': 'node'},
                      {'deleted': False,
                       'id': 359754850,
                       'type': 'node'}],
             'row': [[{'cpf': '11452244740',
                       'nome': 'DANIEL CARVALHO BELCHIOR',
                       'pess_dk': 15535503},
                      {'papel': 'NOTICIANTE'},
                      {'cdorgao': 400749,
                       'classe': 'Notícia de Fato',
                       'docu_dk': 17430731,
                       'dt_cadastro': '12/01/2018 15:46:42',
                       'nr_mprj': 201800032105}],
                     {'cpf': '11452244740',
                      'nome': 'DANIEL CARVALHO BELCHIOR',
                      'pess_dk': 15535503},
                     {'cdorgao': 400749,
                      'classe': 'Notícia de Fato',
                      'docu_dk': 17430731,
                      'dt_cadastro': '12/01/2018 15:46:42',
                      'nr_mprj': 201800032105}]},
            {
                'graph': {
                    'nodes': [
                        {'id': '395989945',
                         'labels': ['personagem'],
                         'properties': {'cpf': '11452244740',
                                        'nome': 'DANIEL '
                                        'CARVALHO '
                                        'BELCHIOR',
                                        'pess_dk': 15535503}},
                        {'id': '140885160',
                         'labels': ['pessoa'],
                         'properties': {'cpf': '11452244740',
                                        'dt_nasc': '19850522',
                                        'filho_rel_status': 1,
                                        'filho_rel_status_pai': 1,
                                        'nome': 'DANIEL '
                                        'CARVALHO '
                                        'BELCHIOR',
                                        'nome_mae': 'MARTA '
                                        'CARVALHO '
                                        'BELCHIOR',
                                        'nome_pai': 'FRANCISCO '
                                        'IVAN '
                                        'FONTELE '
                                        'BELCHIOR',
                                        'nome_rg': 'DANIEL '
                                        'CARVALHO '
                                        'BELCHIOR',
                                        'rg': '131242950',
                                        'sexo': '1',
                                        'uf': 'RJ',
                                        'visitado': False}}],
                    'relationships': [{'endNode': '395989945',
                                       'id': '277481565',
                                       'properties': {'papel': 'NOTICIANTE'},
                                       'startNode': '140885160',
                                       'type': 'personagem'}]},
                'meta': [[{'deleted': False,
                           'id': 395989945,
                           'type': 'node'},
                          {'deleted': False,
                           'id': 277481565,
                           'type': 'relationship'},
                          {'deleted': False,
                           'id': 140885160,
                           'type': 'node'}],
                         {'deleted': False,
                          'id': 395989945,
                          'type': 'node'},
                         {'deleted': False,
                          'id': 140885160,
                          'type': 'node'}],
                'row': [[{'cpf': '11452244740',
                          'nome': 'DANIEL CARVALHO BELCHIOR',
                          'pess_dk': 15535503},
                         {'papel': 'NOTICIANTE'},
                         {'cpf': '11452244740',
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
                          'visitado': False}],
                        {'cpf': '11452244740',
                         'nome': 'DANIEL CARVALHO BELCHIOR',
                         'pess_dk': 15535503},
                        {'cpf': '11452244740',
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
                         'visitado': False}]}]}]}

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


casos_servicos = [
    {
        'nome': 'api_node',
        'endereco': '/db/data/transaction/commit',
        'servico': '/api/node',
        'resposta': resposta_node_ok,
        'requisicao': request_node_ok,
        'query_string': {
            "node_id": 395989945
        },
        'metodo': responses.POST
    },
    {
        'nome': 'api_findNodes',
        'endereco': '/db/data/transaction/commit',
        'servico': '/api/findNodes',
        'resposta': resposta_filterNodes_ok,
        'requisicao': request_filterNodes_ok,
        'query_string': {
            'label': 'pessoa',
            'prop': 'nome',
            'val': 'DANIEL CARVALHO BELCHIOR'
        },
        'metodo': responses.POST
    },
    {
        'nome': 'api_nextNodes',
        'endereco': '/db/data/transaction/commit',
        'servico': '/api/nextNodes',
        'resposta': resposta_nextNodes_ok,
        'requisicao': request_nextNodes_ok,
        'query_string': {
            "node_id": 395989945
        },
        'metodo': responses.POST
    },
    {
        'nome': 'api_nodeProperties',
        'endereco': '/db/data/cypher',
        'servico': '/api/nodeProperties',
        'resposta': resposta_nodeproperties_ok,
        'requisicao': request_nodeproperties_ok,
        'query_string': {
            "label": "pessoa"
        },
        'metodo': responses.POST
    },
    {
        'nome': 'api_labels',
        'endereco': '/db/data/labels',
        'servico': '/api/labels',
        'resposta': resposta_label_ok,
        'requisicao': None,
        'query_string': {},
        'metodo': responses.GET
    },
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

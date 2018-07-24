import responses


request_node_ok = {
    'statements': [
        {
            'statement': 'MATCH  (n) where id(n) = 395989945 return n',
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
                    },
                    'meta': [{
                        'deleted': False,
                        'id': 395989945,
                        'type': 'node'
                    }],
                    'row': [{
                        'cpf': '11452244740',
                        'nome': 'DANIEL CARVALHO BELCHIOR',
                        'pess_dk': 15535503,
                        'sensivel': True
                    }]
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
                    },
                    'meta': [{
                        'deleted': False,
                        'id': 395989945,
                        'type': 'node'
                    }],
                    'row': [{
                    }]
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
            'where id(n) = 395989945 return r,n,x limit 100',
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


resposta_sensivel_mista = {
    'results': [{'columns': ['r', 'n', 'x'], 'data': [{'row': [[{
    'uf': 'RJ',
    'cpf': '001',
    'nome_mae': 'H M P',
    'nome': 'M H P R',
    'sensivel': True,
    'sexo': '2',
    'dt_nasc': '20180709',
    }, {}, {
    'uf': 'RJ',
    'nome_pai': 'E P R',
    'rg': '0001',
    'cpf': '001',
    'filho_rel_status': 1,
    'filho_rel_status_pai': 8,
    'nome_mae': 'M H P R',
    'nome': 'N R P',
    'sexo': '2',
    'nome_rg': 'N R P',
    'dt_nasc': '20180709',
    }], {
    'uf': 'RJ',
    'cpf': '001',
    'nome_mae': 'H M P',
    'nome': 'M H P R',
    'sensivel': True,
    'sexo': '2',
    'dt_nasc': '20180709',
    }, {
    'uf': 'RJ',
    'nome_pai': 'E P R',
    'rg': '0003',
    'cpf': '0002',
    'filho_rel_status': 1,
    'filho_rel_status_pai': 8,
    'nome_mae': 'M H P R',
    'nome': 'N R P',
    'sexo': '2',
    'nome_rg': 'N R P',
    'dt_nasc': '20180709',
    }], 'meta': [[{'id': 10844320, 'type': 'node', 'deleted': False},
                 {'id': 282236618, 'type': 'relationship',
                 'deleted': False}, {'id': 85604696, 'type': 'node',
                 'deleted': False}], {'id': 10844320, 'type': 'node',
                 'deleted': False}, {'id': 85604696, 'type': 'node',
                 'deleted': False}],
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
    }]}}, {'row': [[{
    'uf': 'RJ',
    'cpf': '020',
    'nome_mae': 'H M P',
    'nome': 'M H P R',
    'sensivel': True,
    'sexo': '2',
    'dt_nasc': '20180709',
    }, {'sensivel': True}, {
    'uf': 'RJ',
    'nome_pai': 'E P R',
    'rg': '006',
    'cpf': '006',
    'filho_rel_status': 1,
    'filho_rel_status_pai': 8,
    'nome_mae': 'M H P R',
    'nome': 'A P R',
    'sensivel': True,
    'sexo': '1',
    'nome_rg': 'A P R',
    'dt_nasc': '20180709',
    }], {
    'uf': 'RJ',
    'cpf': '006',
    'nome_mae': 'H M P',
    'nome': 'M H P R',
    'sensivel': True,
    'sexo': '2',
    'dt_nasc': '20180709',
    }, {
    'uf': 'RJ',
    'nome_pai': 'E P R',
    'rg': '007',
    'cpf': '007',
    'filho_rel_status': 1,
    'filho_rel_status_pai': 8,
    'nome_mae': 'M H P R',
    'nome': 'A P R',
    'sensivel': True,
    'sexo': '1',
    'nome_rg': 'A P R',
    'dt_nasc': '20180709',
    }], 'meta': [[{'id': 10844320, 'type': 'node', 'deleted': False},
                 {'id': 282346165, 'type': 'relationship',
                 'deleted': False}, {'id': 12075099, 'type': 'node',
                 'deleted': False}], {'id': 10844320, 'type': 'node',
                 'deleted': False}, {'id': 12075099, 'type': 'node',
                 'deleted': False}],
        'graph': {'nodes': [{'id': '12075099', 'labels': ['pessoa'],
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
    }]}}, {'row': [[{
    'uf': 'RJ',
    'cpf': '008',
    'nome_mae': 'H M P',
    'nome': 'M H P R',
    'sensivel': True,
    'sexo': '2',
    'dt_nasc': '20180709',
    }, {}, {
    'uf': 'RJ',
    'nome_pai': 'E P R',
    'rg': '009',
    'cpf': '009',
    'filho_rel_status': 1,
    'filho_rel_status_pai': 8,
    'nome_mae': 'M H P R',
    'nome': 'S P R',
    'sexo': '1',
    'nome_rg': 'S P R',
    'dt_nasc': '20180709',
    }], {
    'uf': 'RJ',
    'cpf': '010',
    'nome_mae': 'H M P',
    'nome': 'M H P R',
    'sensivel': True,
    'sexo': '2',
    'dt_nasc': '20180709',
    }, {
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
    }], 'meta': [[{'id': 10844320, 'type': 'node', 'deleted': False},
                 {'id': 286160836, 'type': 'relationship',
                 'deleted': False}, {'id': 57161336, 'type': 'node',
                 'deleted': False}], {'id': 10844320, 'type': 'node',
                 'deleted': False}, {'id': 57161336, 'type': 'node',
                 'deleted': False}],
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
    }]}}, {'row': [[{
    'uf': 'RJ',
    'cpf': '012',
    'nome_mae': 'M M P',
    'nome': 'M H P R',
    'sensivel': True,
    'sexo': '2',
    'dt_nasc': '20180709',
    }, {}, {
    'uf': 'RJ',
    'nome_pai': 'E P R',
    'rg': '013',
    'cpf': '013',
    'filho_rel_status_pai': 8,
    'filho_rel_status': 1,
    'nome_mae': 'M H P R',
    'nome': 'M T R DE A',
    'sexo': '2',
    'nome_rg': 'M T R DE A',
    'dt_nasc': '20180709',
    }], {
    'uf': 'RJ',
    'cpf': '014',
    'nome_mae': 'H M P',
    'nome': 'M H P R',
    'sensivel': True,
    'sexo': '2',
    'dt_nasc': '20180709',
    }, {
    'uf': 'RJ',
    'nome_pai': 'E P R',
    'rg': '015',
    'cpf': '015',
    'filho_rel_status_pai': 8,
    'filho_rel_status': 1,
    'nome_mae': 'M H P R',
    'nome': 'M T R DE A',
    'sexo': '2',
    'nome_rg': 'M T R DE A',
    'dt_nasc': '20180709',
    }], 'meta': [[{'id': 10844320, 'type': 'node', 'deleted': False},
                 {'id': 288798795, 'type': 'relationship',
                 'deleted': False}, {'id': 116929750, 'type': 'node',
                 'deleted': False}], {'id': 10844320, 'type': 'node',
                 'deleted': False}, {'id': 116929750, 'type': 'node',
                 'deleted': False}],
        'graph': {'nodes': [{'id': '10844320', 'labels': ['pessoa'],
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
    'results': [{'columns': ['r', 'n', 'x'], 'data': [{'row': [[{
    }, {}, {
    'uf': 'RJ',
    'nome_pai': 'E P R',
    'rg': '0001',
    'cpf': '001',
    'filho_rel_status': 1,
    'filho_rel_status_pai': 8,
    'nome_mae': 'M H P R',
    'nome': 'N R P',
    'sexo': '2',
    'nome_rg': 'N R P',
    'dt_nasc': '20180709',
    }], {
    }, {
    'uf': 'RJ',
    'nome_pai': 'E P R',
    'rg': '0003',
    'cpf': '0002',
    'filho_rel_status': 1,
    'filho_rel_status_pai': 8,
    'nome_mae': 'M H P R',
    'nome': 'N R P',
    'sexo': '2',
    'nome_rg': 'N R P',
    'dt_nasc': '20180709',
    }], 'meta': [[{'id': 10844320, 'type': 'node', 'deleted': False},
                 {'id': 282236618, 'type': 'relationship',
                 'deleted': False}, {'id': 85604696, 'type': 'node',
                 'deleted': False}], {'id': 10844320, 'type': 'node',
                 'deleted': False}, {'id': 85604696, 'type': 'node',
                 'deleted': False}],
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
    }]}}, {'row': [[{
    }, {}, {
    }], {
    }, {
    }], 'meta': [[{'id': 10844320, 'type': 'node', 'deleted': False},
                 {'id': 282346165, 'type': 'relationship',
                 'deleted': False}, {'id': 12075099, 'type': 'node',
                 'deleted': False}], {'id': 10844320, 'type': 'node',
                 'deleted': False}, {'id': 12075099, 'type': 'node',
                 'deleted': False}],
        'graph': {'nodes': [{'id': '12075099', 'labels': ['sigiloso'],
                  'properties': {
    }}, {'id': '10844320', 'labels': ['sigiloso'], 'properties': {
    }}], 'relationships': [{
    'id': '282346165',
    'type': 'sigiloso',
    'startNode': '12075099',
    'endNode': '10844320',
    'properties': {},
    }]}}, {'row': [[{
    }, {}, {
    'uf': 'RJ',
    'nome_pai': 'E P R',
    'rg': '009',
    'cpf': '009',
    'filho_rel_status': 1,
    'filho_rel_status_pai': 8,
    'nome_mae': 'M H P R',
    'nome': 'S P R',
    'sexo': '1',
    'nome_rg': 'S P R',
    'dt_nasc': '20180709',
    }], {
    }, {
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
    }], 'meta': [[{'id': 10844320, 'type': 'node', 'deleted': False},
                 {'id': 286160836, 'type': 'relationship',
                 'deleted': False}, {'id': 57161336, 'type': 'node',
                 'deleted': False}], {'id': 10844320, 'type': 'node',
                 'deleted': False}, {'id': 57161336, 'type': 'node',
                 'deleted': False}],
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
    }]}}, {'row': [[{
    }, {}, {
    'uf': 'RJ',
    'nome_pai': 'E P R',
    'rg': '013',
    'cpf': '013',
    'filho_rel_status_pai': 8,
    'filho_rel_status': 1,
    'nome_mae': 'M H P R',
    'nome': 'M T R DE A',
    'sexo': '2',
    'nome_rg': 'M T R DE A',
    'dt_nasc': '20180709',
    }], {
    }, {
    'uf': 'RJ',
    'nome_pai': 'E P R',
    'rg': '015',
    'cpf': '015',
    'filho_rel_status_pai': 8,
    'filho_rel_status': 1,
    'nome_mae': 'M H P R',
    'nome': 'M T R DE A',
    'sexo': '2',
    'nome_rg': 'M T R DE A',
    'dt_nasc': '20180709',
    }], 'meta': [[{'id': 10844320, 'type': 'node', 'deleted': False},
                 {'id': 288798795, 'type': 'relationship',
                 'deleted': False}, {'id': 116929750, 'type': 'node',
                 'deleted': False}], {'id': 10844320, 'type': 'node',
                 'deleted': False}, {'id': 116929750, 'type': 'node',
                 'deleted': False}],
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

query_dinamica = [
    {'statement': "optional match (a:pessoa {nome:toUpper('DANIEL CARVALHO BELCHIOR')}) "
                  "optional match (b:personagem {pess_dk:24728287}) return a,b limit 100",
                  'resultDataContents': ['row', 'graph']}]

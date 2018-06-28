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

request_filterNodes_ok = {
    'statements': [
        {'statement': "MATCH (n: pessoa { "
         "nome:toUpper('DANIEL CARVALHO BELCHIOR')}) return n",
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

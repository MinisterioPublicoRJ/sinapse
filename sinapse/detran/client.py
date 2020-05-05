import requests

from decouple import config

from sinapse.buildup import _IMAGENS


def busca_foto(rg):
    url_busca = config("URL_BUSCA_FOTO").format(rg=rg)
    token_busca = config("TOKEN_BUSCA_FOTO")
    resp = requests.get(url_busca, params={"proxy-token": token_busca})
    return resp.json()['photo']


def get_person_photo(infos, label):
    successes = []
    for info in infos:
        if 'rg' in info:
            rg_field = 'rg'
        else:
            rg_field = 'num_rg'
        status, content = send_rg_query(info[rg_field])
        if b'sucesso' in content.lower()\
                or b'foi finalizada' in content.lower():
            successes.append(info)

    for success in successes:
        status, content = get_processed_rg(success[rg_field])
        print('--->', status, success[rg_field])
        photo = parse_content(content, 'fotoCivil')
        if photo is not None and photo != '':
            _IMAGENS.update(
                {'num_rg': success[rg_field]},
                {'$set': {
                    'imagem': photo,
                    'uuid': success['uuid'],
                    'tipo': label
                }},
                upsert=True
            )

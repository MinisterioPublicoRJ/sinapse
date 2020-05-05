import requests

from decouple import config

from sinapse.buildup import _IMAGENS


def busca_foto(rg):
    url_busca = config("URL_BUSCA_FOTO").format(rg=rg)
    token_busca = config("TOKEN_BUSCA_FOTO")
    resp = requests.get(url_busca, params={"proxy-token": token_busca})

    photo = ""
    if resp.status_code == 200:
        photo = resp.json()['photo']

    return photo


def get_person_photo(infos, label):
    for info in infos:
        if 'rg' in info:
            rg_field = 'rg'
        else:
            rg_field = 'num_rg'

        photo = busca_foto(info[rg_field])
        if photo != '':
            _IMAGENS.update(
                {'num_rg': info[rg_field]},
                {'$set': {
                    'imagem': photo,
                    'uuid': info['uuid'],
                    'tipo': label
                }},
                upsert=True
            )

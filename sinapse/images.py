import base64

from sinapse.buildup import _IMAGENS
from sinapse.queries import download_google_image


def get_vehicle_photo(infos, label):
    keys = ['marca_modelo', 'ano_modelo', 'cor']

    for info in infos:
        vehicle_characteristic = ' '.join([info[k] for k in keys])
        img_exists = _IMAGENS.find_one(
            {'caracteristicas': vehicle_characteristic},
            {'_id': 0, 'imagem': 1}
        )
        if not img_exists:
            img = download_google_image(vehicle_characteristic)
            if img:
                _IMAGENS.update(
                    {'caracteristicas': vehicle_characteristic},
                    {'$set': {
                        'imagem': base64.encodestring(img).decode(),
                        'uuid': info['uuid'],
                        'tipo': label
                    }},
                    upsert=True
                )

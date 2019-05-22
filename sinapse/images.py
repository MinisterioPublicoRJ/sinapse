import base64

from sinapse.buildup import _IMAGENS
from sinapse.queries import download_google_image


def get_vehicle_photo(infos, label):
    for info in infos:
        vehicle_characteristic = ' '.join(info[1:])
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
                        'uuid': info.node_id,
                        'tipo': label
                    }},
                    upsert=True
                )

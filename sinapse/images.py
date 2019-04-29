import base64

from sinapse.buildup import _IMAGENS
from sinapse.detran.utils import find_relations_info
from sinapse.queries import find_next_nodes, download_google_image


def get_vehicle_photo(node_id):
    next_nodes = find_next_nodes(node_id, node_type=':veiculo', path_size=2)
    label = 'veiculo'
    infos = find_relations_info(
        next_nodes.json(),
        pks=['marca', 'modelo', 'cor'],
        label=label,
        props=['marca', 'modelo', 'cor']
    )
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
                        'tipo': label
                    }},
                    upsert=True
                )
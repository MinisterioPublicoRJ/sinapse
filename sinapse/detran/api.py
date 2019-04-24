from flask import request, jsonify

from sinapse.buildup import app, _IMAGENS
from sinapse.start import login_necessario


@app.route('/api/foto', methods=['GET'])
@login_necessario
def api_photo():
    node_id = request.args.get('node_id')
    rg = request.args.get('rg')

    photo_doc = _IMAGENS.find_one(
        {'$or': [{'rg': rg}, {'node_id': node_id}]},
        {'_id': 0}
    )

    if photo_doc:
        return jsonify(photo_doc)

    return jsonify({})

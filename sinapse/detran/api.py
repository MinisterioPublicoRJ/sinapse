from flask import request, jsonify

from sinapse.buildup import app, _FOTOS_DETRAN
from sinapse.start import login_necessario


@app.route('/api/foto', methods=['GET'])
@login_necessario
def api_photo():
    node_id = request.args.get('node_id')
    rg = request.args.get('rg')

    photo_doc = _FOTOS_DETRAN.find_one(
        {'$or': [{'rg': rg}, {'node_id': node_id}]}
    )

    if photo_doc:
        return jsonify(photo_doc)

    return jsonify({})

from flask import request, jsonify

from sinapse.buildup import app, _MONGO_CLIENT
from sinapse.start import login_necessario, respostajson

COLLECTION_FOTOS = _MONGO_CLIENT.mmps.fotos


@app.route('/api/foto', methods=['GET'])
@login_necessario
def api_photo():
    rg = request.args.get('rg')
    photo_doc = COLLECTION_FOTOS.find_one({'rg': rg}, {'_id': 0})
    if photo_doc:
        return jsonify(photo_doc)

    return jsonify({})

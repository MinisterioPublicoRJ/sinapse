import json

from decouple import config

from flask import (
    request,
    render_template,
    jsonify,
    session
)
from .auth import autenticadorjwt
from .buildup import app, _IMAGENS
from .queries import search_info, log_solr_response
from .start import login_necessario


@app.route("/api/filtroinicial", methods=['GET'])
@autenticadorjwt
def filtro_inicial():
    label = request.args.get('label')
    prop = request.args.get('prop')
    val = request.args.get('val')

    return render_template(
        'index.html',
        filtroinicial={
            'label': label,
            'prop': prop,
            'val': val
        }
    )


@app.route("/api/search", methods=['GET'])
@login_necessario
def api_search():
    solr_queries = json.load(open(config('SOLR_QUERIES'), 'r'))
    q = request.args.get('q')
    info = search_info(q, solr_queries)

    # Log query response
    user = session.get('usuario', "dummy")
    sessionid = request.cookies.get('session')
    log_solr_response(user, sessionid, info)
    return jsonify(info)


@app.route('/api/foto', methods=['GET'])
@login_necessario
def api_photo():
    node_id = request.args.get('node_id', '')
    rg = request.args.get('rg', '')

    photo_doc = _IMAGENS.find_one(
        {'$or': [{'num_rg': rg}, {'node_id': node_id}], 'tipo': 'Pessoa'},
        {'_id': 0}
    ) or {}

    return jsonify(photo_doc)


@app.route('/api/foto-veiculo', methods=['GET'])
@login_necessario
def api_photo_vehicle():
    characteristics = request.args.get('caracteristicas', '')

    photo_doc = _IMAGENS.find_one(
        {'caracteristicas': characteristics, 'tipo': 'Veiculo'},
        {'_id': 0}
    ) or {}

    return jsonify(photo_doc)

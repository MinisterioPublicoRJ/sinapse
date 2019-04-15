import json

from decouple import config

from flask import (
    request,
    render_template,
    jsonify,
    session
)
from .auth import autenticadorjwt
from .buildup import app
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

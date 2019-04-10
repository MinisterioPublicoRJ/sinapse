from flask import (
    request,
    render_template,
    jsonify
)
from .auth import autenticadorjwt
from .buildup import app
from .queries import search_info
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
    q = request.args.get('q')
    info = {}
    resp_person, resp_auto, resp_comp = search_info(q)
    info['pf'] = resp_person
    info['auto'] = resp_auto
    info['company'] = resp_comp
    return jsonify(info)

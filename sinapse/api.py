from flask import (
    request,
    render_template,
    jsonify
)
from .auth import autenticadorjwt
from .buildup import app
from .queries import search_by_name
from .start import login_necessario


class RespWrapper:
    def __init__(self, resp_content):
        self.content = resp_content


class PersonWrapper(RespWrapper):
    def json(self):
        clean_content = self.content.copy()
        clean_content.pop('responseHeader')
        return clean_content


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
    name = request.args.get('name')
    resp = search_by_name(name)
    person_info = PersonWrapper(resp.json())
    return jsonify(person_info.json())

from flask import (
    request,
    render_template
)
from .auth import autenticadorjwt
from .buildup import app


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

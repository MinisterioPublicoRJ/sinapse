from flask import (
    request,
    render_template
)
from .auth import autenticadorjwt
from .buildup import app


@autenticadorjwt
@app.route("/api/filtrar", methods=['POST'])
def api_filtrar():
    label = request.form.get('label')
    prop = request.form.get('prop')
    val = request.form.get('val')

    return render_template(
        'index.html',
        filtroinicial={
            'label': label,
            'prop': prop,
            'val': val
        }
    )

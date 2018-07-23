import jwt

from datetime import datetime, timedelta

from flask import request
from sinapse.buildup import (
    app
)


@app.route('/api/autorizar', methods=['POST'])
def autorizar():
    sistema = request.form['sistema']
    usuario = request.form['usuario']

    if sistema not in app.config['SISTEMAS']:
        return '', 401

    validade = datetime.now() + timedelta(seconds=60)

    saida = jwt.encode(
        {
            'usuario': usuario,
            'validade': validade.strftime('%Y-%m-%d %H:%M:%S')
        },
        app.secret_key,
        algorithm='HS256'
    )

    return saida, 200

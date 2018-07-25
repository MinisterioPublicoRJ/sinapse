import jwt

from datetime import datetime, timedelta
from functools import wraps

from flask import (
    request,
    session
)
from jwt.exceptions import (
    InvalidSignatureError,
    DecodeError,
    ExpiredSignatureError
)
from sinapse.buildup import (
    app
)


def autenticadorjwt(funcao):
    @wraps(funcao)
    def funcao_decorada(*args, **kwargs):
        token_jwt = request.headers.get('authorization')
        if not token_jwt:
            return '', 403
        try:
            token_jwt = token_jwt.split(' JWT ')[1]
            mensagem = jwt.decode(
                token_jwt,
                app.secret_key)

            session['usuario'] = mensagem['usuario']
            return funcao(*args, **kwargs)
        except (InvalidSignatureError, DecodeError):
            return 'Erro de Assinatura', 403
        except ExpiredSignatureError:
            return 'Expirado', 401

    return funcao_decorada


@app.route('/api/autorizar', methods=['POST'])
def autorizar():
    sistema = request.form['sistema']
    usuario = request.form['usuario']

    if sistema not in app.config['SISTEMAS']:
        return '', 403

    validade = datetime.utcnow() + timedelta(seconds=60)

    saida = jwt.encode(
        {
            'usuario': usuario,
            'exp': validade
        },
        app.secret_key
    )

    return saida, 200

from functools import wraps
from flask import request, jsonify

from dotenv import load_dotenv
load_dotenv()

from .message import IS_ERROR, STATUS
from .routes import med_bp as app
from .token import token_obj

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            resp = IS_ERROR["ERR_AUTH_TOKEN_MISSING"]
            status = STATUS["BAD_REQUEST"]
            return jsonify(resp), status
        token = token.split(" ")[1] if " " in token else token
        resp, status = token_obj.isTokenValid(token)
        if status != STATUS["OK"]:
            return jsonify(resp), status
        return f(*args, **kwargs)
    return decorated
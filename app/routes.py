from flask import Blueprint, render_template, jsonify, request
med_bp = Blueprint('med', __name__)
import requests

from .database import db
from .message import IS_SUCCESS, IS_ERROR, STATUS
from .log import logger
from .redis import cache

@med_bp.route('/')
def hello():
    return render_template('index.html')


@med_bp.route('/init-db',methods=['POST'])
def init_db():
    try:
        db.initialize_database()
        resp = IS_SUCCESS["DATABASE_INITIALIZED"]
        status = STATUS["OK"]

    except Exception as e:
        logger.error(f"Database Error: {e}")
        resp = IS_ERROR["ERR_DATABASE_INITIALIZATION"]
        status = STATUS["INTERNAL_SERVER_ERROR"]
    
    return jsonify(resp), status



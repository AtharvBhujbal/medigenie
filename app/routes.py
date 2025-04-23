from flask import Blueprint, render_template, jsonify, request
med_bp = Blueprint('med', __name__)
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
load_dotenv()

from .database import db
from .message import IS_SUCCESS, IS_ERROR, STATUS
from .log import logger
from .redis import cache
from .user import User

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

@med_bp.route('/login',methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            resp = IS_ERROR["ERR_INVALID_CREDENTIALS"]
            status = STATUS["BAD_REQUEST"]

        user = User(email, password)
        valid, user_id = user.isUserValid()
        if not valid:
            resp = IS_ERROR["ERR_USER_NOT_FOUND"]
            status = STATUS["NOT_FOUND"]
        
        else:
            token = jwt.encode({
                'user_id': user_id,
                'exp': datetime.utcnow() + timedelta(hours=1)
            }, os.getenv('AUTH_SECRET_KEY'), algorithm='HS256')

            resp = IS_SUCCESS["LOGIN_SUCCESS"]
            status = STATUS["OK"]
            resp['token'] = token

    except Exception as e:
        logger.error(f"Login Error: {e}")
        resp = IS_ERROR["ERR_LOGIN_FAILED"]
        status = STATUS["INTERNAL_SERVER_ERROR"]
    
    return jsonify(resp), status

@med_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        phone_number = data.get('phone_number')
        # aadhaar_number = data.get('aadhaar_number')
        # dob = data.get('dob')
        user = User(email, password, name, phone_number)
        registered, user_id = user.register()
        if not registered:
            resp = IS_ERROR["ERR_USER_ALREADY_EXISTS"]
            status = STATUS["BAD_REQUEST"]
        else:
            resp = IS_SUCCESS["REGISTRATION_SUCCESS"]
            status = STATUS["OK"]
            resp['user_id'] = user_id

    except Exception as e:
        logger.error(f"Registration Error: {e}")
        resp = IS_ERROR["ERR_REGISTRATION_FAILED"]
        status = STATUS["INTERNAL_SERVER_ERROR"]

    return jsonify(resp), status
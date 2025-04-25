from flask import Blueprint, render_template, jsonify, request
import psycopg2
med_bp = Blueprint('med', __name__)

from .database import db
from .message import IS_SUCCESS, IS_ERROR, STATUS
from .log import logger
from .redis import cache
from .user import User
from .token import token_obj
from .decorator import token_required, admin_required, sudo_admin_required

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
            token = token_obj.generate_token(user_id)
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
        aadhaar_number = data.get('aadhaar_number')
        dob = data.get('dob')
        gender = data.get('gender')
        chronic_diseases = data.get('chronic_diseases')
        user = User(
            email=email,
            password=password,
            name=name,
            phone_number=phone_number,
            adhaar_number=aadhaar_number,
            dob=dob,
            gender=gender,
            chronic_diseases=chronic_diseases
        )
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

@med_bp.route('/register-organization',methods=['POST'])
@admin_required
def register_org():
    try:
        data = request.get_json()
        org_name = data.get("organization_name")
        license_no = data.get("license_no")
        address = data.get("address")
        contact_number = data.get("contact_number")
        admin_email = data.get("admin_email")
        user = User(email=admin_email,password=None)
        user_exits, admin_id = user.get_user_id_by_email()
        if not user_exits:
            resp = IS_ERROR["ERR_ADMIN_NOT_FOUND"]
            status = STATUS["BAD_REQUEST"]
        else:
            organization = db.create_organization(user.user_id,org_name,license_no,address,contact_number,admin_id)
            resp = IS_SUCCESS["REGISTRATION_SUCCESS"]
            status = STATUS["OK"]
            resp["organization"] = organization

    except psycopg2.errors.UniqueViolation as e:
        logger.error(f"Unique Violation Error: {e}")
        resp = IS_ERROR["ERR_ADMIN_ORG_DUPLICATE"]
        status = STATUS["BAD_REQUEST"]
    except Exception as e:
        logger.error(f"Oragnization Registration Error: {e}")
        resp = IS_ERROR["ERR_REGISTRATION_FAILED"]
        status = STATUS["INTERNAL_SERVER_ERROR"]

    return jsonify(resp), status

@med_bp.route('/update-user-privilege',methods=['POST'])
@sudo_admin_required
def update_user_privilege():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        is_admin = data.get("is_admin")
        if user_id is None:
            resp = IS_ERROR["ERR_USER_ID_MISSING"]
            status = STATUS["BAD_REQUEST"]
        elif is_admin is None:
            resp = IS_ERROR["ERR_USER_PRIVILEGE_MISSING"]
            status = STATUS["BAD_REQUEST"]
        else:
            db.update_user_privilage(user_id,is_admin)
            resp = IS_SUCCESS["REGISTRATION_SUCCESS"]
            status = STATUS["OK"]

    except Exception as e:
        logger.error(f"Update User Privilege Error: {e}")
        resp = IS_ERROR["ERR_USER_UPDATE_FAILED"]
        status = STATUS["INTERNAL_SERVER_ERROR"]

    return jsonify(resp), status
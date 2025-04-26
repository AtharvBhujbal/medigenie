from flask import Blueprint, render_template, jsonify, request
import psycopg2
med_bp = Blueprint('med', __name__)

from .database import db
from .message import IS_SUCCESS, IS_ERROR, STATUS
from .log import logger
from .redis import cache
from .user import User
from .doctor import Doctor
from .organization import Organization
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
            resp = IS_ERROR["ERR_USER_INVALID_CREDENTIALS"]
            status = STATUS["BAD_REQUEST"]

        user = User(email=email, password=password)
        valid, user_id = user.isUserValid()
        if not valid:
            resp = IS_ERROR["ERR_USER_NOT_FOUND"]
            status = STATUS["NOT_FOUND"]
        else:
            token = token_obj.generate_token(user_id)
            resp = IS_SUCCESS["LOGIN_SUCCESS"]
            status = STATUS["OK"]
            resp['user_id'] = user_id
            resp['token'] = token

    except Exception as e:
        logger.error(f"Login Error: {e}")
        resp = IS_ERROR["ERR_USER_LOGIN_FAILED"]
        status = STATUS["INTERNAL_SERVER_ERROR"]
    
    return jsonify(resp), status

@med_bp.route('/create', methods=['POST'])
def create():
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
        created, user_id = user.create()
        if not created:
            resp = IS_ERROR["ERR_USER_ALREADY_EXISTS"]
            status = STATUS["BAD_REQUEST"]
        else:
            resp = IS_SUCCESS["USER_CREATED"]
            status = STATUS["OK"]
            resp['user_id'] = user_id

    except Exception as e:
        logger.error(f"Registration Error: {e}")
        resp = IS_ERROR["ERR_USER_CREATION_FAILED"]
        status = STATUS["INTERNAL_SERVER_ERROR"]

    return jsonify(resp), status

@med_bp.route('/create-organization',methods=['POST'])
@admin_required
def create_organization():
    try:
        data = request.get_json()
        org_name = data.get("organization_name")
        license_number = data.get("license_number")
        address = data.get("address")
        contact_number = data.get("contact_number")
        admin_email = data.get("admin_email")
        user = User(email=admin_email,password=None)
        user_exits, admin_id = user.get_user_id_by_email()
        if not user_exits:
            resp = IS_ERROR["ERR_ADMIN_NOT_FOUND"]
            status = STATUS["BAD_REQUEST"]
        else:
            organization = Organization(
                name=org_name,
                license_number=license_number,
                address=address,
                contact_number=contact_number,
                admin_id=admin_id
            )
            created, organization_id = organization.create()
            if not created:
                resp = IS_ERROR["ERR_ORG_ALREADY_EXISTS"]
                status = STATUS["BAD_REQUEST"]
            else:
                resp = IS_SUCCESS["REGISTRATION_SUCCESS"]
                status = STATUS["OK"]
                resp["organization_id"] = organization_id

    except psycopg2.errors.UniqueViolation as e:
        logger.error(f"Unique Violation Error: {e}")
        resp = IS_ERROR["ERR_ADMIN_ORG_DUPLICATE"]
        status = STATUS["BAD_REQUEST"]
    except Exception as e:
        logger.error(f"Oragnization Registration Error: {e}")
        resp = IS_ERROR["ERR_ORG_CREATION_FAILED"]
        status = STATUS["INTERNAL_SERVER_ERROR"]

    return jsonify(resp), status

@med_bp.route('/update-user-privilege',methods=['POST'])
@sudo_admin_required
def update_user_privilege():
    try:
        data = request.get_json()
        user_email = data.get('user_email')
        is_admin = data.get("is_admin")
        if user_email is None:
            resp = IS_ERROR["ERR_USER_MAIL_MISSING"]
            status = STATUS["BAD_REQUEST"]
        elif is_admin is None:
            resp = IS_ERROR["ERR_USER_PRIVILEGE_MISSING"]
            status = STATUS["BAD_REQUEST"]
        user = User(email=user_email,password=None)
        user_exits, user_id = user.get_user_id_by_email()
        if not user_exits:
            resp = IS_ERROR["ERR_USER_NOT_FOUND"]
            status = STATUS["BAD_REQUEST"]
        else:
            db.update_user_privilage(user_id,is_admin)
            resp = IS_SUCCESS["USER_UPDATED"]
            status = STATUS["OK"]

    except Exception as e:
        logger.error(f"Update User Privilege Error: {e}")
        resp = IS_ERROR["ERR_USER_UPDATE_FAILED"]
        status = STATUS["INTERNAL_SERVER_ERROR"]

    return jsonify(resp), status

@med_bp.route('/register-doctor',methods=['POST'])
def register_doctor():
    try:
        data = request.get_json()
        doctor_mail = data.get('doctor_mail')
        organization_id = data.get('organization_id')
        specialization = data.get('specialization')
        license_number = data.get('license_number')
        user = User(email=doctor_mail,password=None)
        user_exits, user_id = user.get_user_id_by_email()
        if not user_exits:
            resp = IS_ERROR["ERR_USER_NOT_FOUND"]
            status = STATUS["BAD_REQUEST"]
        else:
            doctor = Doctor(
                user_id=user_id,
                organization_id=organization_id,
                specialization=specialization,
                license_number=license_number
            )
            doctor_registered, doctor_id = doctor.register()
            if not doctor_registered:
                resp = IS_ERROR["ERR_USER_ALREADY_EXISTS"]
                status = STATUS["BAD_REQUEST"]
            else:
                resp = IS_SUCCESS["REGISTRATION_SUCCESS"]
                status = STATUS["OK"]
                resp['doctor_id'] = doctor_id
                resp['user_id'] = user_id
    except Exception as e:
        logger.error(f"Doctor Registration Error: {e}")
        resp = IS_ERROR["ERR_REGISTRATION_FAILED"]
        status = STATUS["INTERNAL_SERVER_ERROR"]

    return jsonify(resp), status

@med_bp.route('/get-doctor-organization',methods=['GET'])
def get_doctor_organization():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        if user_id is None:
            resp = IS_ERROR["ERR_USER_ID_MISSING"]
            status = STATUS["BAD_REQUEST"]
        else:
            doctor = Doctor(user_id=user_id)
            organization = doctor.get_doctor_organization_by_user_id()
            if not organization:
                resp = IS_ERROR["ERR_ORG_NOT_FOUND"]
                status = STATUS["NOT_FOUND"]
            else:
                resp = IS_SUCCESS["ORG_FOUND"]
                status = STATUS["OK"]
                resp['organization'] = organization
    except Exception as e:
        logger.error(f"Get Doctor Organization Error: {e}")
        resp = IS_ERROR["ERR_ORG_NOT_FOUND"]
        status = STATUS["INTERNAL_SERVER_ERROR"]

    return jsonify(resp), status
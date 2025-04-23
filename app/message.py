IS_SUCCESS = {
    "DATABASE_INITIALIZED": {"code": "db_init", "message": "Database initialized successfully"},
    "LOGIN_SUCCESS": {"code": "login_success", "message": "Login successful"},
    "REGISTRATION_SUCCESS": {"code": "registration_success", "message": "Registration successful"},
}

IS_ERROR = {
    "ERR_DATABASE_INITIALIZATION": {"code": "db_init", "message": "Database initialization failed"},
    "ERR_USER_NOT_FOUND": {"code": "user_not_found", "message": "User not found"},
    "ERR_INVALID_CREDENTIALS": {"code": "invalid_credentials", "message": "Invalid credentials"},
    "ERR_LOGIN_FAILED": {"code": "login_failed", "message": "Login failed"},
    "ERR_USER_ALREADY_EXISTS": {"code": "user_already_exists", "message": "User already exists"},
    "ERR_REGISTRATION_FAILED": {"code": "registration_failed", "message": "Registration failed"},
}


STATUS = {
    "INTERNAL_SERVER_ERROR": 500,
    "BAD_REQUEST": 400,
    "NOT_FOUND": 404,
    "OK": 200,
}
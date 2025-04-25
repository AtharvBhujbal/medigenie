IS_SUCCESS = {
    "DATABASE_INITIALIZED": {"code": "db_init", "message": "Database initialized successfully"},
    "LOGIN_SUCCESS": {"code": "login_success", "message": "Login successful"},
    "REGISTRATION_SUCCESS": {"code": "registration_success", "message": "Registration successful"},

    # Token-related success messages
    "AUTH_TOKEN_VALID": {"code": "auth_token_valid", "message": "Authentication token is valid"},
}

IS_ERROR = {
    "ERR_DATABASE_INITIALIZATION": {"code": "db_init", "message": "Database initialization failed"},

    # User-related errors
    "ERR_USER_NOT_FOUND": {"code": "user_not_found", "message": "User not found"},
    "ERR_INVALID_CREDENTIALS": {"code": "invalid_credentials", "message": "Invalid credentials"},
    "ERR_LOGIN_FAILED": {"code": "login_failed", "message": "Login failed"},
    "ERR_USER_ALREADY_EXISTS": {"code": "user_already_exists", "message": "User already exists"},
    "ERR_REGISTRATION_FAILED": {"code": "registration_failed", "message": "Registration failed"},
    "ERR_USER_ID_MISSING": {"code": "user_id_missing", "message": "User ID is missing in the request"},
    "ERR_USER_UNAUTHORIZED": {"code": "user_unauthorized", "message": "User is not authorized to perform this action"},
    "ERR_USER_PRIVILEGE_MISSING": {"code": "user_privilege_missing", "message": "User privilege is missing"},
    "ERR_USER_UPDATE_FAILED": {"code": "user_update_failed", "message": "User update failed"},

    # Admin-related errors
    "ERR_ADMIN_NOT_FOUND": {"code": "admin_not_found", "message": "Admin email not found"},
    "ERR_ADMIN_ORG_DUPLICATE": {"code": "admin_org_duplicate", "message": "Cannot create multiple organizations with the same Email ID"},

    # Token-related errors
    "ERR_AUTH_TOKEN_MISSING": {"code": "auth_token_missing", "message": "Authentication token is missing"},
    "ERR_AUTH_TOKEN_INVALID": {"code": "auth_token_invalid", "message": "Invalid authentication token"},
    "ERR_AUTH_TOKEN_EXPIRED": {"code": "auth_token_expired", "message": "Authentication token has expired"},
}


STATUS = {
    "INTERNAL_SERVER_ERROR": 500,
    "BAD_REQUEST": 400,
    "NOT_FOUND": 404,
    "OK": 200,
}
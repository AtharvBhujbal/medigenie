from .database import db
import hashlib


class User:
    def __init__(self, email, password, name=None, phone_number=None, dob=None):
        self.email = email
        self.password = password
        self.name = name
        self.phone_number = phone_number
        self._db = db

    def _check_password(self, stored_password_hash, provided_password):
        return self._hash_password(provided_password) == stored_password_hash
    
    def _hash_password(self,password):
        password_bytes = password.encode('utf-8')
        hash_object = hashlib.sha256(password_bytes)
        return str(hash_object.hexdigest())
    
    def isUserValid(self) -> tuple[bool, int]:
        """
        Validates the user's credentials.

        Returns:
            tuple: A tuple containing a boolean and a value:
                - (False, None): If the user does not exist or the password is invalid.
                - (True, user_id): If the user exists and the password is valid.
        """
        user = self._db.get_user_by_email(self.email)
        if not user:
            return False, None
        if not self._check_password(user['password_hash'], self.password):
            return False, None
        return True, user['user_id']
    
    def register(self) -> bool:
        """
        Registers a new user.
        Returns:
            bool: True if registration is successful, False if the user already exists.
        """
        if self._db.get_user_by_email(self.email):
            return False
        hashed_password = self._hash_password(self.password)
        self._db.create_user(self.email, hashed_password, self.name, self.phone_number)
        return True

    


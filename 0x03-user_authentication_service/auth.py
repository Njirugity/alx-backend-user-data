#!/usr/bin/env python3
from db import DB
import bcrypt
from user import User
import uuid   


def _hash_password(password):
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        exisiting_user = self._db.find_user_by(email=email )
        if exisiting_user:
            raise ValueError(f"User {email} already exists.")
        new_user= self._db.add_user(email, _hash_password(password))
        return new_user
    def valid_login(self, email: str, password: str) -> bool:
        exisiting_user = self._db.find_user_by(email=email )
        # hash_passwd = self._hash_password(password)
        if exisiting_user:
            byte_passwd = password.encode("utf-8")
            check_passwd = bcrypt.checkpw(byte_passwd, exisiting_user.hashed_password)
            if check_passwd:
                return True
            else:
                return False
        else:
            return False

    def _generate_uuid(self)->str:
        """
        Generates a new UUID and returns its string representation.
        This function is intended for internal use within the module.
        """
        return str(uuid.uuid4())

    def create_session(self, email: str)-> str:
                
        
        user = self._db.find_user_by(email=email)
        if not user:
            raise ValueError(f"User with email {email} not found.")

        session_id = self._generate_uuid() 
        updated_user = self._db.update_user(user.id, session_id=session_id)

        if updated_user:
            return session_id
        else:
            False

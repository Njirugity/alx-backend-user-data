#!/usr/bin/env python3
""" to manage the Basic API authentication.
"""


from api.v1.auth.auth import Auth
import base64
import binascii
from models.user import User
from models.base import Base
from typing import TypeVar


class BasicAuth(Auth):
    """Class for basic authentication.

    Args:
        Auth (type): The auth authentication class.
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """_summary_

        Args:
            authorization_header (str): _description_

        Returns:
            str: _description_
        """
        if isinstance(authorization_header, str) and authorization_header.startswith("Basic "):
            last_str = authorization_header.split()
            return last_str[-1]
        else:
            return None

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str) -> str:
        """ returns the decoded value of a Base64 string
        """
        if base64_authorization_header is None:
            return None
        elif not isinstance(base64_authorization_header, str):
            return None
        try:
            encoded_header = base64_authorization_header.encode("ascii")
            decoded_header = base64.b64decode(encoded_header, validate=True)

            return decoded_header.decode("utf-8")
        except binascii.Error:
            return None
        
    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str) -> (str, str):
        """
        Returns user email and password from Base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return None
        if not isinstance(decoded_base64_authorization_header, str):
            return None
        else:
            separated_header = tuple(decoded_base64_authorization_header.split(":"))
            if len(separated_header) == 2:
                return separated_header
            else:
                return None
    def user_object_from_credentials(self,
                                     user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Return a User instance based on email and password
     """
        if not isinstance(user_email, str) and user_email is None:
            return None
        if not isinstance(user_pwd, str) and user_pwd is None:
            return None
        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            for i in users:
                if i.is_valid_password(user_pwd):
                    return i
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns a User instance based on a received request
        """
        Auth_header = self.authorization_header(request)
        if Auth_header is not None:
            token = self.extract_base64_authorization_header(Auth_header)
            if token is not None:
                decoded = self.decode_base64_authorization_header(token)
                if decoded is not None:
                    email, pword = self.extract_user_credentials(decoded)
                    if email is not None:
                        return self.user_object_from_credentials(email, pword)
        return

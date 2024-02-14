#!/usr/bin/env python3
"""
 authentication using Basic auth
"""


from typing import TypeVar
from api.v1.auth.auth import Auth
import base64
from models.user import User


class BasicAuth(Auth):
    """basic authclass
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """

        Args:
                 authorization_header

        Returns:
                 str
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None

        token = authorization_header.split(' ')[-1]
        return token

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """

        Args:
                 base64_authorization_header

        Returns:
                  str:
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            item = base64_authorization_header.encode('utf-8')
            decod = base64.b64decode(item)
            return decod.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """user credentials

        Args:
                                      self
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        email, password = decoded_base64_authorization_header.split(':')
        return (email, password)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """user credential objects

        Args:
                      self
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        get current user
        """
        auth_header = self.authorization_header(request)
        if auth_header is not None:
            tok = self.extract_base64_authorization_header(auth_header)
            if tok is not None:
                decod = self.decode_base64_authorization_header(tok)
                if decod is not None:
                    email, password = self.extract_user_credentials(decod)
                    if email is not None:
                        return self.user_object_from_credentials(
                            email, password)

        return

#!/usr/bin/env python3
""" auth model script
"""


import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4

from typing import Union


def _hash_password(password: str) -> str:
    """ password hashing function

    Args:
        password (str): description

    Returns:
        bytes: hashed password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """generate a uuid4 string
    """
    id = uuid4()
    return str(id)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """initialize the Auth class
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> Union[None, User]:
        """_register a user in the database
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

        else:
            raise ValueError('User {} already exists'.format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """ on valid login
        """
        try:
            actual_user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        hash_pass = actual_user.hashed_password
        return bcrypt.checkpw(password.encode('utf-8'), hash_pass)

    def create_session(self, email: str) -> str:
        """ create a session for user
        """
        try:
            actual_user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        else:
            actual_user.session_id = _generate_uuid()
            return actual_user.session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """get user from session id
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        else:
            return user

    def destroy_session(self, user_id: str) -> None:
        """ destroy a session
        """
        try:
            the_user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None
        else:
            the_user.session_id = None
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        reset password token
        """
        try:
            the_user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        else:
            the_user.reset_token = _generate_uuid()
            return the_user.reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        update password
        """
        try:
            the_user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        else:
            the_user.hashed_password = _hash_password(password)
            the_user.reset_token = None
            return None

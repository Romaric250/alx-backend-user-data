#!/usr/bin/env python3
"""
This module defines the User class for the user authentication service.

The User class represents a user in the system and contains information such as their email,
hashed password, session ID, and reset token.
"""


from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class User(Base):
    """This module defines the User class for the user authentication service.
    Args:
        Base (type): The base class for the SQLAlchemy declarative base.

    Attributes:
        __tablename__ (str): The name of the database table for storing user information.
        id (int): The unique identifier for each user.
        email (str): The email address of the user.
        hashed_password (str): The hashed password of the user.
        session_id (str): The session ID of the user.
        reset_token (str): The reset token for the user's password reset.

    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
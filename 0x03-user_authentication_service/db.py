#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        args:
            _session: the session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ adds the user to session
        args:
            email: the email of the user
            hashed_password: the hashed password of the user
        """
        new_user = User(email=email, hashed_password=hashed_password)
        
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """ finds the user by the given keyword arguments

        Returns:
            User: _description_
        """
        if not kwargs:
            raise InvalidRequestError

        the_user = self._session.query(User).filter_by(**kwargs).first()
        if not the_user:
            raise NoResultFound
        return the_user

    def update_user(self, user_id: int, **kwargs) -> None:
        """updates the user with the given keyword arguments

        Args:
            user_id (int): _description_
        """
        the_user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(the_user, key):
                raise ValueError
            setattr(the_user, key, value)

        self._session.commit()
        return None
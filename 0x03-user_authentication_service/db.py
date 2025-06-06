#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError, SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound 
from user import User, Base


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session
    
    def add_user(self, email: str, hashed_password: str) -> User | None:
        """
        Create a User object and save it to the database
        Args:
            email (str): user's email address
            hashed_password (str): password hashed by bcrypt's hashpw
        Return:
            Newly created User object
        """
        new_user = User(email= email,hashed_password = hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Return a user who has an attribute matching the attributes passed
        as arguments
        Args:
            attributes (dict): a dictionary of attributes to match the user
        Return:
            matching user or raise error
        """
        try:
            query_result = self._session.query(User).filter_by(**kwargs).first()
            return query_result
        except SQLAlchemyError as e:
            print(f"A database error occurred during find_user_by: {e}")
            self._session.rollback()
            return None
        except Exception as e:
            print(f"An unexpected error occurred during find_user_by: {e}")
            self._session.rollback()
            return None
        # single_user = self._session.query(User).filter_by(**kwargs).first()
        # return single_user
    def update_user(self,user_id: int, **kwargs) -> None:
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError()
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise ValueError
        self._session.commit()

import sqlalchemy as db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin
import bcrypt


Base = declarative_base()


class User(Base, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    login = Column(String(128), index=True,
                   unique=True, nullable=False)
    password = Column(String(128), nullable=False)


    def __repr__(self):
        return "<User(login={})>".format(self.login)


    def hash_password(self, password):
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(password.encode('utf8'), salt)


    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf8'), self.password)

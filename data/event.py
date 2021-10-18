import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Event(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'event'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    images = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="")
    znach = sqlalchemy.Column(sqlalchemy.BOOLEAN)

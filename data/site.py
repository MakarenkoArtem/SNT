import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Site(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'site'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    #author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="")
    images = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="")
    docs_image = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="")
    #oplata_image = sqlalchemy.Column(sqlalchemy.LargeBinary, nullable=True)
    oplata_image = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="")
    oplata_text = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="")
    #dolgi_image = sqlalchemy.Column(sqlalchemy.LargeBinary, nullable=True)
    dolgi_image = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="")

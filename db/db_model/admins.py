import sqlalchemy
from .db_session import SqlAlchemyBase


class Admins(SqlAlchemyBase):
    __tablename__ = 'Admins'

    key = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True)
    username = sqlalchemy.Column(sqlalchemy.String)

import sqlalchemy
from .db_session import SqlAlchemyBase


class Users(SqlAlchemyBase):
    __tablename__ = 'Users'

    ADMIN_FATHER = 1
    ADMIN = 2
    INTERN = 3

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True)
    username = sqlalchemy.Column(sqlalchemy.String)
    role = sqlalchemy.Column(sqlalchemy.Integer)
    surname = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    middle_name = sqlalchemy.Column(sqlalchemy.String)

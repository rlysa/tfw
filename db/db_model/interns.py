import sqlalchemy
from .db_session import SqlAlchemyBase


class Interns(SqlAlchemyBase):
    __tablename__ = 'Interns'

    username = sqlalchemy.Column(sqlalchemy.String, primary_key=True, unique=True)
    skills = sqlalchemy.Column(sqlalchemy.String)
    admin = sqlalchemy.Column(sqlalchemy.String)

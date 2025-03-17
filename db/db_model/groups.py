import sqlalchemy
from .db_session import SqlAlchemyBase


class Groups(SqlAlchemyBase):
    __tablename__ = 'Groups'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    admin = sqlalchemy.Column(sqlalchemy.String)
    interns = sqlalchemy.Column(sqlalchemy.String)

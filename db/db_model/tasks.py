import sqlalchemy
from .db_session import SqlAlchemyBase


class Tasks(SqlAlchemyBase):
    __tablename__ = 'Tasks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    interns = sqlalchemy.Column(sqlalchemy.String)
    admin = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    deadline = sqlalchemy.Column(sqlalchemy.Date)
    report_format = sqlalchemy.Column(sqlalchemy.Date)
    report = sqlalchemy.Column(sqlalchemy.String)
    done = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

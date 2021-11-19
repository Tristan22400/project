import marshmallow
import sqlalchemy

from .entity import Entity
from .base import Base


class Auth(Entity, Base):
    __tablename__ = 'auth'

    login = sqlalchemy.Column(sqlalchemy.String)
    password = sqlalchemy.Column(sqlalchemy.String)

    def __init__(self, login, password, created_by):
        Entity.__init__(self, created_by)
        self.login = login
        self.password = password


class AuthSchema(marshmallow.Schema):
    id = marshmallow.fields.Number()
    login = marshmallow.fields.Str()
    password = marshmallow.fields.Str()

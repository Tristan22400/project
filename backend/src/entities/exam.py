import marshmallow
import sqlalchemy

from .entity import Entity, Base


class Exam(Entity, Base):
    __tablename__ = 'exams'

    title = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)

    def __init__(self, title, description, created_by):
        Entity.__init__(self, created_by)
        self.title = title
        self.description = description


class ExamSchema(marshmallow.Schema):
    id = marshmallow.fields.Number()
    title = marshmallow.fields.Str()
    description = marshmallow.fields.Str()
    created_at = marshmallow.fields.DateTime()
    updated_at = marshmallow.fields.DateTime()
    last_updated_by = marshmallow.fields.Str()

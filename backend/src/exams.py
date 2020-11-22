import flask

from .auth import login_required
from .db import get_session
from .entities.exam import Exam, ExamSchema


blueprint = flask.Blueprint('exams', __name__)


@blueprint.route('/exams')
def get_exams():
    # fetching from the database
    session = get_session()
    exam_objects = session.query(Exam).all()

    # transforming into JSON-serializable objects
    schema = ExamSchema(many=True)
    exams = schema.dump(exam_objects)

    # serializing as JSON
    session.close()
    return flask.jsonify(exams)


@blueprint.route('/exams', methods=['POST'])
#@login_required
def add_exam():
    # mount exam object
    posted_exam = ExamSchema(
        only=('title', 'description')).load(flask.request.get_json())

    exam = Exam(**posted_exam, created_by="HTTP post request")

    # persist exam
    session = get_session()
    session.add(exam)
    session.commit()

    # return created exam
    new_exam = ExamSchema().dump(exam)
    session.close()
    return flask.jsonify(new_exam), 201

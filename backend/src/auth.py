import functools

import flask
import werkzeug.security

from .db import get_session
from .entities.auth import Auth, AuthSchema


blueprint = flask.Blueprint('auth', __name__)


class AuthError(Exception):
    def __init__(self, error, status_code):
        super().__init__()
        self.error = error
        self.status_code = status_code


@blueprint.route('/register', methods=['POST'])
def register():
    print(f'registering... {flask.request.get_json()}')
    posted_auth = AuthSchema(
        only=('login', 'password')).load(flask.request.get_json())
    auth = Auth(
        posted_auth['login'],
        werkzeug.security.generate_password_hash(posted_auth['password']),
        created_by='HTTP post request')

    session = get_session()
    error = None

    if not auth.login:
        error = 'Login is required.'
    elif not auth.password:
        error = 'Password is required.'
    elif session.execute(
            'SELECT id FROM auth WHERE login = :login', {'login': auth.login}
    ).fetchone() is not None:
        error = f'User {auth.login} is already registered.'

    if error is None:
        session.add(auth)
        session.commit()
        session.close()
        return flask.jsonify({'login': auth.login}), 201

    raise AuthError({
        'code': 'registration failed',
        'description': error}, 401)


@blueprint.route('/login', methods=['POST'])
def login():
    posted_auth = AuthSchema(
        only=('login', 'password')).load(flask.request.get_json())
    auth = Auth(**posted_auth, created_by='HTTP post request')

    db = get_session()
    error = None
    user = db.execute(
        'SELECT * FROM auth WHERE login = :login', {'login': auth.login}
    ).fetchone()

    if user is None:
        error = 'Incorrect username.'
    elif not werkzeug.security.check_password_hash(
            user['password'], auth.password):
        error = 'Incorrect password.'

    if error is None:
        flask.session.clear()
        flask.session['user_id'] = user['id']
        return flask.jsonify({'login': auth.login}), 201

    raise AuthError({
        'code': 'login failed',
        'description': error}, 401)


@blueprint.before_app_request
def load_logged_in_user():
    user_id = flask.session.get('user_id')

    if user_id is None:
        flask.g.user = None
    else:
        flask.g.user = get_session().execute(
            'SELECT * FROM user WHERE id = :login', {'login': user_id}
        ).fetchone()


@blueprint.route('/logout')
def logout():
    flask.session.clear()
    return None, 204


def requires_auth(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if flask.g.user is None:
            return flask.redirect(flask.url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@blueprint.errorhandler(AuthError)
def handle_auth_error(error):
    response = flask.jsonify(error.error)
    response.status_code = error.status_code
    return response

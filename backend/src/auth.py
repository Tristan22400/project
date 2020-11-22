import functools

import flask
import werkzeug.security

from .db import get_session


blueprint = flask.Blueprint('auth', __name__, url_prefix='/auth')


class AuthError(Exception):
    def __init__(self, error, status_code):
        super().__init__()
        self.error = error
        self.status_code = status_code


@blueprint.route('/register', methods=('GET', 'POST'))
def register():
    if flask.request.method == 'POST':
        username = flask.request.form['username']
        password = flask.request.form['password']
        db = get_session()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
                'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, werkzeug.security.generate_password_hash(password))
            )
            db.commit()
            return flask.redirect(flask.url_for('auth.login'))

        raise AuthError({
            'code': 'registration failed',
            'description': error}, 401)

    return flask.render_template('auth/register.html')


@blueprint.route('/login', methods=('GET', 'POST'))
def login():
    if flask.request.method == 'POST':
        username = flask.request.form['username']
        password = flask.request.form['password']
        db = get_session()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not werkzeug.security.check_password_hash(
                user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            flask.session.clear()
            flask.session['user_id'] = user['id']
            return flask.redirect(flask.url_for('index'))

        raise AuthError({
            'code': 'login failed',
            'description': error}, 401)

    return flask.render_template('auth/login.html')


@blueprint.before_app_request
def load_logged_in_user():
    user_id = flask.session.get('user_id')

    if user_id is None:
        flask.g.user = None
    else:
        flask.g.user = get_session().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@blueprint.route('/logout')
def logout():
    flask.session.clear()
    return flask.redirect(flask.url_for('index'))


def login_required(view):
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

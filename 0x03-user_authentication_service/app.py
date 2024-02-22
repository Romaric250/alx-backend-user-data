#!/usr/bin/env python3
""" simple flask app
"""


from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index() -> str:
    """ simple index route
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """
    login in to sessions
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not (AUTH.valid_login(email, password)):
        abort(401)
    else:
        session_id = AUTH.create_session(email)
        resp = jsonify({"email": email, "message": "logged in"})
        resp.set_cookie('session_id', session_id)

    return resp


@app.route('/users', methods=['POST'])
def users() -> str:
    """ get users from the db
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        the_user = AUTH.register_user(email, password)
        return jsonify({"email": the_user.email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """_
    get user profile
    """
    session_id = request.cookies.get('session_id')
    the_user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": the_user.email}), 200
    else:
        abort(403)


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """ sessions logout
    """
    session_id = request.cookies.get('session_id')
    the_user = AUTH.get_user_from_session_id(session_id)
    if not the_user:
        abort(403)
    AUTH.destroy_session(the_user.id)
    return redirect('/')


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> str:
    """
    reset password token
    """
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except Exception:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password() -> str:
    """update password
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

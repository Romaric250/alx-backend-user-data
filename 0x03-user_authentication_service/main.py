#!/usr/bin/env python3
""" user model script
"""

import requests

def register_user(email: str, password: str) -> None:
    response = requests.post('http://localhost/register', data={'email': email, 'password': password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}

def log_in_wrong_password(email: str, password: str) -> None:
    response = requests.post('http://localhost/sessions', data={'email': email, 'password': password})
    assert response.status_code == 401

def log_in(email: str, password: str) -> str:
    response = requests.post('http://localhost/sessions', data={'email': email, 'password': password})
    assert response.status_code == 200
    return response.cookies['session_id']

def profile_unlogged() -> None:
    response = requests.get('http://localhost/profile')
    assert response.status_code == 403

def profile_logged(session_id: str) -> None:
    response = requests.get('http://localhost/profile', cookies={'session_id': session_id})
    assert response.status_code == 200
    assert 'email' in response.json()

def log_out(session_id: str) -> None:
    response = requests.delete('http://localhost/sessions', cookies={'session_id': session_id})
    assert response.status_code == 200

def reset_password_token(email: str) -> str:
    response = requests.post('http://localhost/reset_password', data={'email': email})
    assert response.status_code == 200
    return response.json()['reset_token']

def update_password(email: str, reset_token: str, new_password: str) -> None:
    response = requests.put('http://localhost/reset_password', data={'email': email, 'reset_token': reset_token, 'new_password': new_password})
    assert response.status_code == 200
    
    
MAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
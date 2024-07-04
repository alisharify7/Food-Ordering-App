from flask import session, request

def login_user(user_object):
    session['username'] = user_object.username
    session['account-id'] = user_object.id
    session['password-hash'] = user_object.password
    session['login'] = True
    session['role'] = 'user'

def logout_user():
    session.pop('username')
    session.pop('account-id')
    session.pop('password-hash')
    session.pop('login')
    session.pop('role')

def login_admin():
    ...

def logout_admin():
    ...


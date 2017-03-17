#!/usr/bin/env python
#encoding=UTF-8

from functools import wraps
from flask import request
from flask import session
from flask import url_for
from flask import redirect


# Check if login
def requireLogin(func):
    @wraps(func)
    def decoratedFunction(*args, **kwargs):
        if 'userName' not in session:
            session['redirectUrl'] = request.url
            return redirect(url_for('account.login'))
        return func(*args, **kwargs)
    return decoratedFunction

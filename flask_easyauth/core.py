#!/usr/bin/env python

"""
Provides Base Model
"""

from __future__ import absolute_import

import uuid

from flask import session, current_app
from werkzeug.local import LocalProxy

# pylint: disable=no-name-in-module
from flask.ext.login import (
    login_user,
    logout_user)
# pylint: enable=no-name-in-module

from .token_redis_session import TokenRedisSessionInterface
from .login_manager import AuthLoginManager


# pylint: disable=invalid-name
_auth = LocalProxy(lambda: current_app.extensions['easyauth'])
# pylint: enable=invalid-name


class Auth(object):
    """
    The Auth app
    """

    app = None
    db = None
    login_manager = None
    user_cls = None
    token_cls = None

    def __init__(self, app=None, db=None, user_cls=None, token_cls=None):
        """
        Constructor
        """
        self.app = app
        self.db = db
        self.user_cls = user_cls
        self.token_cls = token_cls
        if (
            (app is not None) and
            (db is not None) and
            (user_cls is not None) and
            (token_cls is not None)
        ):
            self.init_app(app, db, user_cls, token_cls)
        return None

    def init_app(self, app, db, user_cls, token_cls):
        """
        Initiate this application
        """
        ## Initialize app
        self.app = app
        self.app.session_interface = TokenRedisSessionInterface(self.app)
        ## Initialize db
        self.db = db
        ## Setup models
        self.user_cls = user_cls
        self.token_cls = token_cls
        ## Setup login manager
        self.login_manager = \
            AuthLoginManager(self.app, self.db, self.user_cls, self.token_cls)
        ## Add to extensions
        self.app.extensions['easyauth'] = self
        return True

    def login(self, user, **kwargs):
        """
        Logs a user in
        """
        ## Create token
        token = self.create_token()
        ## Add to DB
        auth_token = self.token_cls()
        auth_token.user_id = user.id
        auth_token.token = token
        for key, val in kwargs.iteritems():
            setattr(auth_token, key, val)
        self.db.session.add(auth_token)
        self.db.session.commit()
        ## Set session vars
        session['is_authenticated'] = True
        session['auth_token'] = token
        ## Log user in
        login_user(user, remember=False)
        ## Return token
        return auth_token

    def logout(self):
        """
        Logs out current user
        """
        if ('auth_token' in session) and (session['auth_token'] is not None):
            ## Get token
            token = session['auth_token']
            ## Remove token from DB
            auth_token = self.token_cls.query.filter_by(token=token).first()
            self.db.session.delete(auth_token)
            self.db.session.commit()
        ## Clear session stuff
        session.clear()
        session['is_authenticated'] = False
        session['auth_token'] = None
        ## Logout the user
        logout_user()
        return True

    def create_token(self):
        """
        Created a token
        """
        return uuid.uuid4().get_hex()

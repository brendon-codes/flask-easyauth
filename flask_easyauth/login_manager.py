#!/usr/bin/env python

"""
Provides Base Model
"""

from __future__ import absolute_import

from flask import session, json, Response

# pylint: disable=no-name-in-module
from flask.ext.login import LoginManager
# pylint: enable=no-name-in-module

from .constants import REQ_TOKEN_HEADER


class AuthLoginManager(object):
    """
    Auth login manager
    """

    manager = None
    app = None
    user_cls = None
    token_cls = None
    db = None

    def __init__(self, app, db, user_cls, token_cls):
        """
        Constructor
        """
        self.db = db
        self.user_cls = user_cls
        self.token_cls = token_cls
        self.app = app
        self.manager = LoginManager()
        self.manager.request_loader(self._load_user_from_request)
        self.manager.user_loader(self._load_user)
        self.manager.token_loader(self._user_from_token)
        self.manager.unauthorized_handler(self.unauthorized)
        self.manager.init_app(self.app)
        return None

    def get_manager(self):
        """
        Get login manager
        """
        return self.manager

    def _load_user_from_request(self, request):
        """
        Callback to load a user from a Flask request object

        See:
            https://flask-login.readthedocs.org
            /en/latest/#custom-login-using-request-loader
        """
        req_token = request.headers.get(REQ_TOKEN_HEADER, None)
        if req_token is None:
            return None
        auth_token = self.token_cls.query.filter_by(token=req_token).first()
        if auth_token is None:
            return None
        session['is_authenticated'] = True
        session['auth_token'] = auth_token.token
        return auth_token.user

    def _load_user(self, user_id):
        """
        Load a user from a user id
        """
        return self.user_cls.get(user_id)

    def _user_from_token(self, token):
        """
        Gets a user from a token
        """
        auth_token = self.token_cls.query.filter_by(token=token).first()
        if auth_token is None:
            return None
        return auth_token.user

    def unauthorized(self):
        """
        Unauthorized handler
        """
        headers = {}
        headers['Content-Type'] = "application/json"
        payload = {
            'msg': "Not authorized",
            'code': 'not_authorized'
        }
        return Response(json.dumps(payload), 401, headers)

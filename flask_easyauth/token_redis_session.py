#!/usr/bin/env python

"""
Provides Redis session support.

This was originally copied/inspired from:
http://flask.pocoo.org/snippets/75/

Original Author: Armin Ronacher
"""

from __future__ import absolute_import

import pickle
import uuid
from datetime import timedelta

from redis import Redis

from flask.sessions import SessionInterface, SessionMixin
from werkzeug.datastructures import CallbackDict

from .constants import REQ_TOK_TYPES
from . import request_helpers


class TokenRedisSession(CallbackDict, SessionMixin):
    """
    A Redis Session Class
    """

    def __init__(self, initial=None, sid=None, new=False):
        """
        Constructor
        """

        def on_update(self):
            """
            On Update Callback
            """
            self.modified = True
            return None

        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        self.new = new
        self.modified = False
        return None


class TokenRedisSessionInterface(SessionInterface):
    """
    A Redis Session Interface
    """
    serializer = pickle
    session_class = TokenRedisSession
    req_tok_type = None

    def __init__(self, app, redis=None, prefix='session:'):
        """
        Constructor
        """
        redis_host = app.config.get('SESSION_REDIS_HOST', '127.0.0.1')
        redis_port = app.config.get('SESSION_REDIS_PORT', 6379)
        redis_pass = app.config.get('SESSION_REDIS_PASS', None)
        redis_db = app.config.get('SESSION_REDIS_DB', 0)
        if redis is None:
            redis = \
                Redis(
                    host=redis_host,
                    port=redis_port,
                    db=redis_db,
                    password=redis_pass)
        self.redis = redis
        self.prefix = prefix
        self.req_tok_type = (
            app.config.get(
                'AUTH_TOKEN_TYPE',
                REQ_TOK_TYPES['header']
            )
        )
        return None

    def generate_sid(self):
        """
        Generate a session ID
        """
        return uuid.uuid4().get_hex()

    def get_redis_expiration_time(self, app, sess):
        """
        Get expiration time
        """
        if sess.permanent:
            return app.permanent_session_lifetime
        return timedelta(days=1)

    def open_session(self, app, request):
        """
        Open Session
        """
        sid = (
            request_helpers
            .get_request_token(
                self.req_tok_type,
                request
            )
        )
        if sid is None:
            sid = self.generate_sid()
            return self.session_class(sid=sid, new=True)
        val = self.redis.get(self.prefix + sid)
        if val is not None:
            data = self.serializer.loads(val)
            return self.session_class(data, sid=sid)
        return self.session_class(sid=sid, new=True)

    def save_session(self, app, sess, response):
        """
        Save Session
        """
        if not sess:
            self.redis.delete(self.prefix + sess.sid)
            return None
        redis_exp = self.get_redis_expiration_time(app, sess)
        #cookie_exp = self.get_expiration_time(app, sess)
        val = self.serializer.dumps(dict(sess))
        self.redis.setex(
            self.prefix + sess.sid,
            val,
            int(redis_exp.total_seconds())
        )
        return None

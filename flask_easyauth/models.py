#!/usr/bin/env python

"""
Provides Base Model
"""

from __future__ import absolute_import

from flask import session, current_app
from werkzeug.local import LocalProxy

from passlib.apps import custom_app_context as pwd_context

# pylint: disable=invalid-name
_auth = LocalProxy(lambda: current_app.extensions['easyauth'])
# pylint: enable=invalid-name


class AuthTokenMixin(object):
    """
    An Authentication token.
    The following should be defined:

        user_id = \
            db.Column(db.CHAR(32), db.ForeignKey('user.id'), nullable=False)
        user = \
            db.relationship(
                'User',
                backref=db.backref('auth_tokens', lazy='dynamic'))
        token = db.Column(db.CHAR(32), nullable=False, index=True, unique=True)
    """
    pass


class AuthUserMixin(object):
    """
    User Model.
    The following should be defined

        email = \
            db.Column(db.String(255), nullable=False, index=True, unique=True)
        password = db.Column(db.String(255), nullable=False, index=True)
        active = \
            db.Column(db.Boolean(), nullable=False, index=True, default=True)
        type = db.Column(db.String(10), index=True)

    You will probably want to add this too:

        ## See: http://docs.sqlalchemy.org/en/rel_0_9/orm/inheritance.html
        __mapper_args__ = {
            'polymorphic_identity': 'user',
            'polymorphic_on': type
        }
    """

    email = None
    password = None
    active = None
    type = None

    def is_authenticated(self):
        """
        Is Authenticated
        """
        return (
            ('is_authenticated' in session) and
            session['is_authenticated']
        )

    def is_active(self):
        """
        Is Active
        """
        return self.active

    def is_anonymous(self):
        """
        Is Anonymous
        """
        return (not self.is_authenticated())

    def get_id(self):
        """
        Get ID
        """
        return unicode(self.id)

    def verify_password(self, password):
        """
        Verify a password

        See:
            http://pythonhosted.org/passlib/lib
            /passlib.apps.html#predefined-context-example
        """
        return pwd_context.verify(password, self.password)

    def get_auth_token(self):
        """
        Return the auth token
        """
        if 'auth_token' not in session:
            return None
        return session['auth_token']

    def login(self, **kwargs):
        """
        Wrapper to log a user in
        """
        _auth.login(self, **kwargs)
        return True

    def set_security_attrs(self, email, password=None, encrypted_password=None):
        """
        Creates a user and commits to db
        """
        if (password is None) and (encrypted_password is None):
            raise Exception("Must supply either password or encrypted password")
        elif (password is not None) and (encrypted_password is not None):
            raise \
                Exception(
                    "Can only supply either password or encrypted password")
        elif password is not None:
            self.password = self.encrypt_password(password)
        elif encrypted_password is not None:
            self.password = encrypted_password
        self.email = email
        return True

    @classmethod
    def get_by_email(cls, email):
        """
        Get a user by email
        """
        user = cls.query.filter_by(email=email).first()
        if user is None:
            return None
        return user

    @classmethod
    def encrypt_password(cls, password):
        """
        Encrypt a password

        See:
            http://pythonhosted.org/passlib/lib
            /passlib.apps.html#predefined-context-example
        """
        return pwd_context.encrypt(password)

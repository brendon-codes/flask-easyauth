#!/usr/bin/env python

"""
Decorators for auth-rest
"""

from __future__ import absolute_import

from functools import wraps

from flask import current_app
from werkzeug.local import LocalProxy
# pylint: disable=no-name-in-module
from flask.ext.login import current_user
# pylint: enable=no-name-in-module

# pylint: disable=invalid-name
_auth = LocalProxy(lambda: current_app.extensions['easyauth'])
# pylint: enable=invalid-name


def user_types_required(*types):
    """
    Ensures that user is of a certain type
    """
    def wrapper(func):
        """
        Wrapper
        """
        @wraps(func)
        def decorated_view(*args, **kwargs):
            """
            Decorated class view
            """
            ## No Good
            if (
                (not current_user.is_authenticated()) or
                (current_user.type not in types)
            ):
                return _auth.login_manager.unauthorized()
            ## Return success
            return func(*args, **kwargs)
        return decorated_view
    return wrapper

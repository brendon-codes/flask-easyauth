#!/usr/bin/env python

"""
Flask Easy Auth
"""

from __future__ import absolute_import

# pylint: disable=no-name-in-module
from flask.ext.login import current_user
# pylint: enable=no-name-in-module

from .core import Auth
from .models import AuthTokenMixin, AuthUserMixin

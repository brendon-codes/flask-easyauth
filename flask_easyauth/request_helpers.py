#!/usr/bin/env python

"""
Various request helpers
"""

from __future__ import absolute_import

from .constants import (
    REQ_TOK_TYPES,
    REQ_TOKEN_HEADER,
    REQ_TOKEN_COOKIE
)


def get_request_token(req_tok_type, request):
    """
    Get the request token
    """
    if req_tok_type == REQ_TOK_TYPES['header']:
        req_token = request.headers.get(REQ_TOKEN_HEADER, None)
    elif req_tok_type == REQ_TOK_TYPES['cookie']:
        req_token = request.cookies.get(REQ_TOKEN_COOKIE, None)
    else:
        raise Exception("Invalid token type")
    return req_token

#!/usr/bin/env python

"""
Flask-Easy-Auth
==============

Flask-Easy-Auth adds easy token authentication to your applications
"""

from __future__ import absolute_import

from setuptools import setup


setup(
    name='Flask-EasyAuth',
    version='0.1.0',
    url='https://github.com/brendoncrawford/flask-easyauth',
    license='MIT',
    author='Brendon Crawford',
    author_email='brendon@aphex.io',
    description='Easy token authentication for Flask apps',
    long_description=__doc__,
    packages=[
        'flask_easyauth'
    ],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask>=0.10.1',
        'Flask-Login>=0.2.9',
        'passlib>=1.6.2',
        'Flask-SQLAlchemy>=1.0',
        'redis>=2.9.1',
        'pep8>=1.5.6',
        'pylint>=1.2.0'
    ]
)

#!/usr/bin/env python

"""
Runs Pylint and PEP8 Checks
"""

from __future__ import absolute_import

import os
import sys

ROOT = \
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '../'))
os.chdir(ROOT)
sys.path.append(ROOT)

from pylint.lint import Run as pylint_run
import pep8


PYLINT_RCFILE = os.path.join(ROOT, 'etc', 'pylintrc')
PEP8_RCFILE = os.path.join(ROOT, 'etc', 'pep8rc')

CHECK_FILES = [
    'flask_easyauth/',
    'bin/'
]

PYLINT_DISABLES = [
    'import-error',
    'locally-disabled',
    'file-ignored',
    'no-self-use',
    'no-init',
    'superfluous-parens',
    'duplicate-code',
    'too-many-public-methods',
    'interface-not-implemented',
    'star-args'
]


def pep8_run(paths=None, config_file=None):
    """
    Parse options and run checks on Python source.

    See: pep8._main
    """
    if config_file is None:
        config_file = True
    pep8style = \
        pep8.StyleGuide(
            parse_argv=False,
            config_file=config_file,
            paths=paths)
    options = pep8style.options
    if options.doctest or options.testsuite:
        from testsuite.support import run_tests
        report = run_tests(pep8style)
    else:
        report = pep8style.check_files()
    if options.statistics:
        report.print_statistics()
    if options.benchmark:
        report.print_benchmark()
    if options.testsuite and not options.quiet:
        report.print_results()
    if report.total_errors:
        if options.count:
            sys.stderr.write(str(report.total_errors) + '\n')
        sys.exit(1)
    return True


def build_pylint_opt(key, val):
    """
    Build a pylint option
    """
    return "=".join(["--%s" % key, val])


def build_pylint_disable(val):
    """
    Build a pylint disable
    """
    return build_pylint_opt('disable', val)


def build_pylint_options():
    """
    Build Pylint Options
    """
    pylint_opts = []
    pylint_opts.append(__file__)
    pylint_opts.append(build_pylint_opt('rcfile', PYLINT_RCFILE))
    pylint_opts += map(build_pylint_disable, PYLINT_DISABLES)
    pylint_opts += CHECK_FILES
    return pylint_opts


def start_pep8():
    """
    Wrapper to start pep8
    """
    pep8_run(paths=CHECK_FILES, config_file=PEP8_RCFILE)
    return True


def start_pylint():
    """
    Wrapper to start pylint
    """
    pylint_run(build_pylint_options())
    return True


if __name__ == '__main__':
    ## First run PEP8
    start_pep8()
    ## Then run pylint
    start_pylint()
    ## If the above scripts did not already exit
    ## Then exit with success
    sys.exit(0)

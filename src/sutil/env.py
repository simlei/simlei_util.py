from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import os
import sys
import attr
import funcy

def getEnvFile(name, predicates=[os.path.isfile, os.path.exists], failIfNot=True):
    return getEnv(name, predicates=predicates, failIfNot=failIfNot)

def getEnvDir(name, predicates=[os.path.isdir], failIfNot=True):
    return getEnv(name, predicates=predicates, failIfNot=failIfNot)

def getEnv(name, predicates=[], failIfNot=True):
    """gets an env variable, applying some optional unary predicates. by default [os.path.exists] for a file argument

    :param String name: the environment variable
    :rtype: String or None

    """
    val = os.environ.get(name)
    if val is None:
        if failIfNot:
            raise RuntimeError("environment variable %s is not present. Its predicates are %s." % (str(name), str(predicates)))
        else:
            return None
    for pred in predicates:
        if not pred(val):
            if failIfNot:
                raise RuntimeError("predicate %s not met for env variable %s with value %s" % (str(pred), name, val))
            else:
                return None

    return val

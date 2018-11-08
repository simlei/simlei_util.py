from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import typing

import os
from pathlib2 import Path
import sys
import attr


class _Singleton(type):
    """ A metaclass that creates a Singleton base class when called, python 2 and 3 compatible. """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Singleton(_Singleton('SingletonMeta', (object,), {})):
    """ Extend this for a singleton class that yields the same instance every call
    """
    pass

def _raise(ex):
    """ raise an exception from a lambda
    """
    raise ex

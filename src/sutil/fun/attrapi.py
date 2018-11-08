from __future__ import absolute_import
import os
import attr
import funcy
from fn.func import curried
from functional import seq
from functional.pipeline import Sequence
import inspect
import sys

from sutil.fun import (Option, Some, Empty)


class Attrobject(object):
    """ Base class for attr.s objects with ADT-style methods
    """

    def evolved(self, **kwargs):
        res = attr.evolve(self, **kwargs)
        attr.validate(res)
        return res


def optionized(arg):
    if arg is None:
        return Empty
    return Some(arg)

def typeAdapt(clazz, mayBeNone=True):
    """ 
    This is just for legacy reasons: converters are dirty. Checks the class, by default lets None (which only isinstance of object anyway)
    """

    if not isinstance(mayBeNone, bool):
        raise TypeError('typeAdapt: mayBeNone must be bool')
        
    def _adapter(subj):
        if subj is None and not mayBeNone:
            raise TypeError('passed None for required type {}'.format(clazz))
            
        if not isinstance( subj, clazz ):
            raise TypeError('passed {} for required type {}'.format(subj, clazz))

        return subj

    return _adapter

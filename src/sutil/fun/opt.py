from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import typing

import os
from pathlib2 import Path
import sys
import attr

from .util import Singleton
from . import (fn, funcy, functional, iters, X, F, curried, methodcaller)

class EmptySingleton(Singleton):
    pass
__NOTHING__ = EmptySingleton()

@attr.s(frozen=True)
class Option(object):

    @staticmethod
    def some(val):
        # type: object -> Option
        if val is None:
            raise ValueError('Option value may not be None')
            
        return Option(val)

    @staticmethod
    def noneable(val):
        # type: object -> Option
        """
        converts None to Empty, as the default constructor does
        """
        if val is None:
            return Empty
        else:
            return Some(val)


    # The constructor accepts None and converts it
    _val = attr.ib(converter=(lambda v: __NOTHING__ if v is None else v))  # type: object
    isEmpty = attr.ib(init=False)  # type: bool
    isSome = attr.ib(init=False)  # type: bool

    @isEmpty.default
    def _isEmpty_default(self):
        return self._val is __NOTHING__

    @isSome.default
    def _isSome_default(self):
        return not self.isEmpty
    

    @_val.validator
    def __val_validator(instance, attribute, value):
        if value is None:
            raise ValueError('Option value is None')


    def map(self, fun):
        if self.isEmpty:
            return self
        else:
            return Option(fun(self.get()))

    def flatmap(self, fun):
        if self.isEmpty:
            return self
        else:
            funval = fun(self.get())
            if not isinstance(funval, Option):
                raise TypeError('flatmap lambda returned no Option, but ' + str(funval))
            return funval
    
    def filter(self, fun):
        return self.flatMap(lambda val: self if fun(val) else Empty)

    def get(self):
        if self.isSome:
            return self._val
        else:
            raise ValueError('Called get() on empty Option')

    def getOrElse(self, alternative):
        if self.isEmpty:
            return alternative
        else:
            return self.get()


Empty = Option(__NOTHING__)
def Some(val):
    # type: (...) -> Option
    return Option.some(val)

def __option__repr__(obj):
    if obj.isEmpty:
        return 'Empty'
    else:
        return 'Some({})'.format(repr(obj.get()))

def __option__str__(obj):
    if obj.isEmpty:
        return 'Empty'
    else:
        return 'Some({})'.format(str(obj.get()))

Option.__str__ = __option__str__
Option.__repr__ = __option__repr__

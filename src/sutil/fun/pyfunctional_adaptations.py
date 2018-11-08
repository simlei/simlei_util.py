from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import typing

import os
from pathlib2 import Path
import sys
import attr
import functional
from functional.pipeline import Sequence
from . import (fn, funcy, functional, iters, X, F, curried, methodcaller, Option, Some, Empty)



@funcy.monkey(Sequence)
def findOpt(self):
    for element in self:
        if func(element):
            return Some(element)
    return Empty

@funcy.monkey(Sequence)
def lastOpt(self):
    if not self.sequence:
        return Empty
    return Some(self.last())

@funcy.monkey(Sequence)
def headOpt(self):
    if not self.sequence:
        return Empty
    return Some(self.first())

@funcy.monkey(Sequence)
def zipmap(self, mapFun):
    # type: (...) -> Sequence
    return self.map( lambda x: (x, mapFun(x)) )

@funcy.monkey(Sequence)
def zipmap2(self, mapFun):
    # type: (...) -> Sequence
    return self.map( lambda x: (mapFun(x), x) )



def seq(*args):
    # type: (...) -> Sequence
    """
    just wraps the argument list into a functional.Sequence
    """
    if(args == ()):
        return functional.seq([])
    return functional.seq(list(args))

def Seq(listlike):
    # type: (...) -> Sequence
    """
    indirection to the (unconditional) wrapping of a sequence-like python builtin via the functional streams API.
    """
    return Sequence(listlike)

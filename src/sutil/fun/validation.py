from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import typing

import os
from pathlib2 import Path
import sys
import attr
from . import (fn, funcy, functional, iters, X, F, curried, methodcaller, Option, Some, Empty, seq, Seq, Sequence, Stream)



class ValidationDomain(object):

    @attr.s(frozen=True)
    class Invalid(object):
        errors = attr.ib()  # type: List[ValidationDomain.Error]
        #TODO: validate that not empty

    @attr.s(frozen=True)
    class Valid(object):
        subj = attr.ib()  # type: object
        
    
    def fresh(subj):
        return Valid(subj)

    def combine(v1, v2):
        if isinstance(v1, Valid) and isinstance(v2, Valid):
            return v2
        else:
            v1errors = v1.errors if isinstance(v1, Invalid) else []
            v2errors = v2.errors if isinstance(v2, Invalid) else []
            errs = v1.errors + v2.errors
            return Invalid(errs)


@attr.s(frozen=True)
class Validation(object):
    semigroup = None
    


""" useful snippets moving on 
"""
@attr.s(frozen=True)
class ConvError(object):
    """
    https://stackoverflow.com/questions/18188563/how-to-re-raise-an-exception-in-nested-try-except-blocks
    """
    converter = attr.ib()  # type: Conv
    input = attr.ib()  # type: ConvInput
    exception = attr.ib()  # type: Exception
    sysInfo = attr.ib(repr=False)  # 3-tuple sys-info, can be reraised using self.reraise

    def reraise(self):
        raise self.sysInfo[0], self.sysInfo[1], self.sysInfo[2]

    def msg(self):
        return '{0}({1}): {2}'.format(str(self.exception), value, excReason)
    


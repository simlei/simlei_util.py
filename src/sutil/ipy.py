from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import typing

import os
from pathlib2 import Path
import sys
import attr
import sutil
from sutil.fun import (fn, funcy, functional, iters, seq, Seq, Sequence, Stream, Option, Some, Empty, X, F, curried, methodcaller)

import sutil

import IPython
from IPython.core.interactiveshell import InteractiveShell
from IPython import get_ipython
ipython = get_ipython()  # type: InteractiveShell

def hist(negpatterns=None, buffersize=100, **kwargs):
    # type: (...) -> Sequence
    negpatterns = negpatterns or seq(r"sutil\.ipy", r"^%", r"\?$")

    patternfilters = negpatterns.map(lambda pat: (lambda x: not funcy.re_test(pat, x)))  # type: Seq
    filterF = patternfilters.fold_left(lambda x: True, lambda f1, f2: lambda val: f1(val) and f2(val))

    return Seq(ipython.history_manager.get_tail(n=buffersize, **kwargs))\
        .map(X[2])\
        .zipmap(filterF)\
        .filter(X[1])\
        .map(X[0])

def lastHistCalls(n=1):
    # type: (...) -> str
    rev = hist().reverse()  # type: Seq
    res = rev.take(n).reverse()  # type: Seq
    return res.make_string("\n") + "\n"
    # return hist(n).lastOpt(z).getOrElse("'no non-hist entries'")

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import typing

from abc import (ABCMeta, abstractmethod)
import os
from pathlib2 import Path
import sys
import attr
import sutil
import sutil.fun as f
from sutil.fun import (fn, funcy, functional, iters, X, F, curried, methodcaller, Option, Some, Empty, seq, Seq, Sequence, Stream)

from sutil import ros
from sutil import ycm
from sutil import dictmerge as merge
from sutil.dictmerge import mergers

ros.catkin.getRosSyspathAugmentation()

s1 = merge.Contrib(merge.mergers.atomic(True), dict(
    val1='s1v1',
    val2='s1v2'
))
s2 = merge.Contrib(merge.mergers.atomic(True), dict(
    val1='s2v1',
    val3='s2v3'
))
s3 = merge.Contrib(merge.mergers.atomic(True), dict(
    val2='s3v2',
    val3='s3v3'
))
s4 = merge.Contrib(merge.mergers.precedence(True), dict(
    flags=['-b', '-c'],
    flags2=['-2c', '-2x'],
    setting1='s1no'
))
s5 = merge.Contrib(merge.mergers.precedence(True), dict(
    flags=['-a', '-d'],
    flags2=['-2c', '-2y']
))


contribs = seq(s1, s2, s3, s4, s5)  # type: Seq
merge.mergeContribs(contribs)
contribs.for_each(print)

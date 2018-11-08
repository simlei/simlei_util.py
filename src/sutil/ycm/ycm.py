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

def mergeContribs(contribs):
    def contribfold(old, new):
        # type: (dict, SettingsContrib) -> dict
        return new.contribute(old)

    # import ipdb; ipdb.set_trace()
    return Seq(contribs).fold_left(dict(), contribfold)

@attr.s(frozen=True)
class SettingsContrib(sutil.fun.attrapi.Attrobject):
    """
    This class holds a dictionary and an entry-wise merger method to specify how it changes
    an existing YCM settings dictionary.

    This class holds predefined merger factories, named merger_xyz, which 
    """

    merger = attr.ib()  # type: SettingsMerger
    dict = attr.ib()  # type: dict

    def contribute(self, old):
        # type: (dict) -> dict
        result = old.copy()
        result.update({k: self.merger.merge(k, old.get(k), v) for k, v in self.dict.iteritems()})
        return result


@attr.s
class SettingsMerger(sutil.fun.attrapi.Attrobject):
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def merge(self, key, existingValue, newValue):
        raise NotImplementedError('SettingsMerger itself is abstract')


@attr.s
class SettingMergeAtomic(SettingsMerger):
    overwrite = attr.ib(default=True, converter=bool)
    
    def merge(self, key, existingValue, newValue):
        # type: (object, object) -> object
        ex = Option(existingValue)
        new = Option(newValue)

        if self.overwrite:
            return new.getOrElse(ex.getOrElse(None))
        else:
            return ex.getOrElse(new.getOrElse(None))

@attr.s(frozen=True)
class SettingsMergePrecedenceList(SettingsMerger):
    """
    precedence is understood as "elements that come first override conflicting ones that come later."
    merges such list-valued entries.
    """
    override = attr.ib()  # type: bool

    @override.default
    def _override_default(self):
        return True

    def merge(self, key, existingValue, newValue):
        try:
            ex = Option(existingValue).map( lambda x: Seq(x) )
            new = Option(newValue).map( lambda x: Seq(x) )
        except Exception:
            raise ValueError('This merge method only takes sequence-valued input')

        if self.override:
            return new.getOrElse(seq()) + ex.getOrElse(seq())
        else:
            return ex.getOrElse(seq()) + new.getOrElse(seq())




class mergers(object):
    pass
    
    atomic = SettingMergeAtomic
    precedence = SettingsMergePrecedenceList

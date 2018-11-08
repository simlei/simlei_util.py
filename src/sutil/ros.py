from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import typing

import re
import os
from pathlib2 import Path
import sys
import attr
import sutil
import sutil.fun as f
from sutil.fun import (fn, funcy, functional, iters, X, F, curried, methodcaller, Option, Some, Empty, seq, Seq, Sequence, Stream)


class C(object):
    def fname(self, x, y):
        return "2"

@attr.s
class D(sutil.fun.attrapi.Attrobject):
    abc = attr.ib()  # type: C

@attr.s
class Catkin(sutil.fun.attrapi.Attrobject):

    catkin_ws = attr.ib(converter=Path)  # type: Path
    catkin_src = attr.ib(init=False)  # type: Path
    catkin_devel = attr.ib(init=False)  # type: Path
    
    @catkin_src.default
    def _catkin_src_default(self):
        return self.catkin_ws / 'src'

    @catkin_devel.default
    def _catkin_devel_default(self):
        return self.catkin_ws / 'devel'

    def abc(self):
        return 1

    def getRosSyspathAugmentation(self):
        dists = self.getRospyDistsFromSyspath()
        return funcy.flatten([dist.getExtendedPaths() for dist in dists])

    def getRospyDistsFromSyspath(self):
        return [RosPyDistPackage(self, expandable_path)
                for libpath in self.develLibsFilter([Path(p) for p in sys.path])
                for expandable_path in self.identifyExpandablePaths(libpath)
                ]

    @funcy.collecting
    def develLibsFilter(self, paths):
        for p in paths:
            if self.catkin_devel in p.parents:
                yield p

    def identifyExpandablePaths(self, path):
        return funcy.filter(self.expandablesFilter, funcy.map(lambda p: p.parent, path.glob('*/__init__.py')))

    def expandablesFilter(self, p):
        if p.name == 'test':
            return False
        return True


@attr.s(frozen=True)
class RosPyDistPackage(sutil.fun.attrapi.Attrobject):
    ws = attr.ib(validator=attr.validators.instance_of(Catkin))
    dir = attr.ib(converter=lambda p: Path(p).resolve())
    
    @dir.validator
    def _dir_validator(instance, attribute, value):
        if not value.is_dir():
            raise ValueError('not a directory')
        if instance.ws.catkin_devel not in value.parents:
            raise ValueError('not a child of ' + str(instance.ws.catkin_devel))
        if not (value / '__init__.py').exists():
            raise ValueError("no __init__.py in %(value)s" % locals())

    @funcy.collecting
    def getExtendedPaths(self):
        if not self.dir.name == 'test':
            initpy = self.dir / '__init__.py'  # type: Path
            with initpy.open() as file:
                for line in file.readlines():
                    match = re.search(r"__extended_path = \"(.*)\".split", line)
                    if match is not None:
                        for sp in match.group(1).split(";"):
                            if not sp.strip() == "":
                                yield sp.strip().rstrip('/')



def catkin_from_env():
    # type: (...) -> Catkin
    return Option(sutil.getEnvDir('ROS_WORKSPACE', failIfNot=False)).map(Catkin)

catkin = catkin_from_env().getOrElse(None)  # type: Catkin

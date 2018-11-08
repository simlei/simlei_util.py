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





""" Legacy code from converter based validation which was a bad idea 
"""

# from fn.monad import Option as ExtOption

#     def _single_adapter(specCallable):

#         def _impl(subj):
#             if not hasattr(specCallable, '__call__'):
#                 raise TypeError('type converter adapter must be callable')
           
#             # # only case in which None is acceptable is through that one method
#             # if subj is None and specCallable is not acceptNone:
#             #     raise ValueError('None cannot be converted except with sutil.model.acceptNone')

#             # isinstance(None, object) == True, therefore we had to gate it. otherwise, if the type fits, pass.
#             if inspect.isclass(specCallable) and isinstance(subj, specCallable):
#                 return subj

#                 # original conversion implementation
#             else:
#                 return specCallable(subj)

#         return _impl

#     def _impl(subj):
#         adapters = seq(vargs)
#         errors = []
#         result = adapters.map(errorAccumulatingConvGen(errors)).fold_left(
#             ExtOption(None), 
#             lambda acc, conv: ExtOption.from_call(acc.get_or_call, conv, subj)
#         ).get_or_call(_raise, ValueError('no adapter of ' + str(adapters) + ' worked for ' + '`' + str(subj) + '`; errors: ' + str(errors)))
#         return result

#     return _impl

# def boolvalid(boolfunc):
#     return lambda instance, attribute, value: True if boolfunc(value) else _raise(RuntimeError("invalid argument to %(attribute)s: %(value)s" % locals()))

    

# @attr.s(frozen=True)
# class ConvRegular(sutil.fun.attrapi.Attrobject):
#     convCallable = attr.ib()
    
#     @convCallable.validator
#     def _convCallable_validator(instance, attribute, value):
#         if not hasattr(value, '__call__'):
#             raise TypeError('type converter adapter must be callable')

#     def adapt(subj, ):

#         # isinstance(None, object) == True, therefore we had to gate it. otherwise, if the type fits, pass.
#         if inspect.isclass(specCallable) and isinstance(subj, specCallable):
#             return subj

#         result = self.convCallable(subj)
#         if result = None
       
#         if 
#         #     raise ValueError('None cannot be converted except with sutil.model.acceptNone')

#             # original conversion implementation
#         else:
#             return specCallable(subj)

    
# def errorAccumulatingConvGen(errorAcc):

#     def _new_converter(fun):
#         name = fun.__name__

#         def _convert(value):
#             try:
#                 return fun(value)
#             except Exception as e:
#                 einfo = sys.exc_info()
#                 excReason = str(e)
#                 msg = '{0}({1}): {2}'.format(name, value, excReason)
#                 # msg = "%(name)s(%(value)s): %(excReason)s" % locals()
#                 error = ConvError(msg, einfo)
#                 errorAcc.append(error)
#                 error.reraise()

#         return _convert

#     return _new_converter

            

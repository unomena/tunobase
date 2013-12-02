'''
Created on 08 Nov 2013

@author: michael
'''
from functools import wraps

from django.utils.decorators import decorator_from_middleware

from tunobase.age_gate.middleware import AgeGateMiddleware

age_gated = decorator_from_middleware(AgeGateMiddleware)
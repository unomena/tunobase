"""
This module provides decorator functionality to the rest of the app
for ensuring that the user is of the correct age to access the site.

Classes:
    n/a

Functions:
    n/a

Created on 08 Nov 2013

@author: michael

"""
from django.utils.decorators import decorator_from_middleware

from tunobase.age_gate.middleware import AgeGateMiddleware

age_gated = decorator_from_middleware(AgeGateMiddleware)

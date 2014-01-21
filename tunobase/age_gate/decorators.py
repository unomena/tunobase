"""
Age Gate App

This module provides decorator functionality to the rest of the app
for ensuring that the user is of the correct age to access the site.

"""
from django.utils.decorators import decorator_from_middleware

from tunobase.age_gate.middleware import AgeGateMiddleware

age_gated = decorator_from_middleware(AgeGateMiddleware)

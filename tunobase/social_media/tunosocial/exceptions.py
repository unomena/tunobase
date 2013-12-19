"""
TUNOSOCIAL APP

This module provides a series of exceptions that can be raised
when interacting with the tunosocial app.

Classes:
    RapidLikingError
    UnauthorizedLikingError

Functions:
    n/a

Created on 31 Oct 2013

@author: michael

"""
class RapidLikingError(Exception):
    """Prevent spam posts."""

    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class UnauthorizedLikingError(Exception):
    """Prevent unauthorized posts."""

    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

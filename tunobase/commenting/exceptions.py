"""
Commenting App

This module provides an exception to be used when comments are
posted too quickly, seemingly looking like spam.

"""


class RapidCommentingError(Exception):
    """Disallow comments posted too quickly."""

    def __init__(self, value):
        """Initialise variables."""

        self.value = value

    def __str__(self):
        """Return string representation."""

        return repr(self.value)

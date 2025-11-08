"""
config package initializer.

Exports settings for easy import: from config import settings
"""
from .settings import *  # noqa: F401,F403

# Optionally, make `settings` available as a namespace
from . import settings as settings  # noqa: F401

__all__ = ["settings"] + [k for k in globals().keys() if k.isupper()]

"""Production settings."""
import os

from .base import *

SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = environ['ALLOWED_HOSTS'].split(',')

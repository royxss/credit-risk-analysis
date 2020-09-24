from .base import *
from decouple import Config, RepositoryEnv
DOTENV_FILE = './.env'
env_config = Config(RepositoryEnv(DOTENV_FILE))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# CORS_ORIGIN_WHITELIST = ['http://localhost:8000', 'http://localhost:3000']

# Prints email in the console
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
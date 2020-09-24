from .base import *
from decouple import Config, RepositoryEnv
DOTENV_FILE = './.env'
env_config = Config(RepositoryEnv(DOTENV_FILE))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# ALLOWED_HOSTS = ["titanrecruit.net"]

ALLOWED_HOSTS = [env_config.get('SERVER_NAME')]

# Email Server Setting
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Other security settings

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_BROWSER_XSS_FILTER = True

SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# X_FRAME_OPTIONS = "DENY"

CSRF_COOKIE_SECURE = True # Change it to true after installing SSL
import os


class BaseConfig(object):
    """Base configuration."""

    # main config
    SECRET_KEY = os.environ.get('SECRET_KEY', 'adljk;adlfgjk')
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT', 'adlkjasdf246')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 7
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    weather_key = os.environ.get('weather_key')
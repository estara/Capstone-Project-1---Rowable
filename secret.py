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

    # mail settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    # gmail authentication
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # mail accounts
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

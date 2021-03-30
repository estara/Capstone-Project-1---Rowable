class BaseConfig(object):
    """Base configuration."""

    # main config
    SECRET_KEY = 'IsItRowable'
    SECURITY_PASSWORD_SALT = 'IWantToRowToday'
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 7
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    weather_key = '279fd9dca315057953de0350c4863100'

    # mail settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    # gmail authentication
    MAIL_USERNAME = 'safetorow@gmail.com'
    MAIL_PASSWORD = 'Rowable2@'

    # mail accounts
    MAIL_DEFAULT_SENDER = 'safetorow@gmail.com'

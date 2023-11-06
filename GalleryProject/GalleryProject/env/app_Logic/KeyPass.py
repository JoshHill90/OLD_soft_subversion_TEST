from decouple import config

class SETTINGS_KEYS:

    DJANGO_KEY = config('DJANGO_KEY')
    DEBUG_STATE = config('DEBUG_STATE')
    DB_NAME = config('DB_NAME')
    DB_USER = config('DEV_DB_USER')
    DB_PASSWORD = config('DEV_DB_PASSWORD')
    DB_HOST = config('DB_HOST')
    DB_PORT = config('DB_PORT')
    MYSQL_ATTR_SSL_CA = config('MYSQL_ATTR_SSL_CA')
    dbstt = config('DEBUG_STATE', bool)
    EMAIL_HOSTING = config('EMAIL_HOSTING')
    EMAIL_USER = config('EMAIL_USER')
    EMAIL_PASSWORD = config('EMAIL_PASSWORD')
    EMAIL_BACKEND_SMTP = config('EMAIL_BACKEND_SMTP')
    EMAIL_PORT = config('EMAIL_PORT')
    

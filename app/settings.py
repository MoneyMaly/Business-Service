import configparser
import os

config = configparser.ConfigParser()
config.read(os.getenv('CONFIG_FILE', '/configs/businessconfig.ini'))

try:
    db_section = config['db_section']
    DATABASE_SERVER = os.getenv('DATABASE_SERVER', db_section['database_server'])
    DATABASE_PORT = os.getenv('DATABASE_PORT', int(db_section['database_port']))
    DATABASE_NAME = os.getenv('DATABASE_NAME', db_section['database_name'])
    DATABASE_USER = os.getenv('DATABASE_USER', db_section['database_user'])
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', db_section['database_password'])

    auth_section = config['auth_section']
    APP_SECRET_KEY = os.getenv('APP_SECRET_KEY', auth_section['app_secret_key'])
    ALGORITHM = os.getenv('ALGORITHM', auth_section['algorithm'])
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES',int(auth_section['access_token_expire_minutes']))

    service_section = config['service_section']
    BANK_API_URL = os.getenv('BANK_API_URL', service_section['bank_api_url'])

except KeyError:
    DATABASE_SERVER = os.getenv('DATABASE_SERVER')
    DATABASE_PORT = os.getenv('DATABASE_PORT')
    DATABASE_NAME = os.getenv('DATABASE_NAME')
    DATABASE_USER = os.getenv('DATABASE_USER')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')

    APP_SECRET_KEY = os.getenv('APP_SECRET_KEY')
    ALGORITHM = os.getenv('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
    BANK_API_URL = os.getenv('BANK_API_URL')
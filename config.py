from os import getenv, path, makedirs
import logging
from dotenv import load_dotenv

load_dotenv()


class Config:
    ENV = getenv('ENV', 'dev')

    DEBUG = not ENV not in ['dev', 'test']
    TESTING = not ENV not in ['dev', 'test']

    # Database
    DB_DIALECT = getenv('DB_DIALECT', 'postgresql')
    DB_HOST = getenv('DB_HOST', '127.0.0.1')
    DB_PORT = getenv('DB_PORT', '5432')
    DB_USERNAME = getenv('DB_USERNAME', 'postgres')
    DB_PASSWORD = getenv('DB_PASSWORD', '')
    DB_NAME = getenv('DB_NAME', 'blank')
    SQLALCHEMY_DATABASE_URI = f'{DB_DIALECT}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}' if \
        ENV != 'test' else f'{getenv("DATABASE_URI")}'

    # Secret Key
    SECRET_KEY = getenv('SECRET_KEY', None)

    # Logging
    log_path = './logs/'
    log_file_path = f'{log_path}app.log'
    if not path.exists(log_path):
        makedirs(log_path)
    if not path.exists(log_file_path):
        with open(log_file_path, 'w'):
            pass

    logging.basicConfig(
        level=getenv('LOGLEVEL', 'DEBUG'),
        handlers=[logging.FileHandler(log_file_path), logging.StreamHandler()]
    )

    # Swagger
    SWAGGER_TITLE = getenv('SWAGGER_TITLE', 'Blank API')
    SWAGGER_VERSION = getenv('SWAGGER_VERSION', '1.0')
    SWAGGER_DESCRIPTION = getenv('SWAGGER_DESCRIPTION', 'Blank API')

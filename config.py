import os
import logging
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    DEBUG = False
    TESTING = False

    POSTGRES_URL = os.getenv("POSTGRES_URL")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB")

    # SQLAlchemy
    uri_template = "postgresql+psycopg2://{user}:{pw}@{url}/{db}"
    SQLALCHEMY_DATABASE_URI = uri_template.format(
        user=POSTGRES_USER, pw=POSTGRES_PASSWORD, url=POSTGRES_URL, db=POSTGRES_DB
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret Key
    SECRET_KEY = "BAD_SECRET_KEY"

    # API settings
    API_PAGINATION_PER_PAGE = 10

    # --------- Logging ---------
    if not os.path.exists("./logs/"):
        os.makedirs("./logs/")
    if not os.path.exists("./logs/trace.log"):
        open("./logs/trace.log", "x")

    logging.basicConfig(
        level=os.getenv("LOGLEVEL", "DEBUG"),
        handlers=[logging.FileHandler("./logs/trace.log"), logging.StreamHandler()],
    )


class DevelopmentConfig(Config):
    DEBUG = True


class TestConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    # production config
    pass

import os
from decouple import config
from datetime import timedelta


class Config:
    DEBUG = True
    basedir = os.path.abspath(os.path.dirname(__file__))

    SECRET_KEY = config('SECRET_KEY', default='')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TRAP_HTTP_EXCEPTIONS = True

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_ACCESS_LIFESPAN = timedelta(days=1)
    JWT_REFRESH_LIFESPAN = timedelta(days=2)


class ProductionConfig(Config):
    DEBUG = False

    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        config('DB_ENGINE', default=''),
        config('DB_USERNAME', default=''),
        config('DB_PASSWORD', default=''),
        config('DB_HOST', default=''),
        config('DB_PORT', default=''),
        config('DB_NAME', default='')
    )


class DevelopmentConfig(Config):
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=100)
    JWT_ACCESS_LIFESPAN = timedelta(days=100)
    JWT_REFRESH_LIFESPAN = timedelta(days=100)

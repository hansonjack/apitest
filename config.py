import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_secret_key')
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@192.168.152.100:13306/api'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@192.168.50.95:13306/api'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    # SQLALCHEMY_ECHO=True  ##打印sql
    REDIS_HOST = '192.168.50.95'
    REDIS_PORT = '6379'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY

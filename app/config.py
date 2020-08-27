import os


class Config:
    SITE_NAME = u'PPCMS'

    # Consider SQLALCHEMY_COMMIT_ON_TEARDOWN harmful
    # SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    SQLALCHEMY_POOL_RECYCLE = 10
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # to get a string like this run:
    # openssl rand -hex 32
    SECRET_KEY = "bfpsT2JuBMjhEvc4xeKy9Xy73VihKP"
    ALGORITHM = "HS256"

    # SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_ECHO = False

    MYSQL_USER = 'root'
    MYSQL_PASS = 'root'
    MYSQL_HOST = '127.0.0.1'
    MYSQL_PORT = '3306'
    MYSQL_DB = 'fastapitest'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s:%s/%s' % (MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DB)


class ProductionConfig(Config):
    DEBUG = True

    # mysql configuration
    MYSQL_USER = ''
    MYSQL_PASS = ''
    MYSQL_HOST = ''
    MYSQL_PORT = '3306'
    MYSQL_DB = ''

    if (len(MYSQL_USER) > 0 and len(MYSQL_PASS) > 0 and len(MYSQL_HOST) > 0 and len(MYSQL_PORT) > 0 and len(MYSQL_DB) > 0):
        SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s:%s/%s' % (MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DB)


config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}


def get_config():
    config_name = os.getenv('FASTAPI_ENV') or 'default'
    return config[config_name]
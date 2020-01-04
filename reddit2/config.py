import secrets

class Config(object):
    DEBUG = False
    TESTING = False

    db_username = ''
    db_password = ''
    db_host = ''
    db_db = ''

    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}/{}'.format(db_username, db_password, db_host, db_db)
    SECRET_KEY = secrets.token_hex(16)

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

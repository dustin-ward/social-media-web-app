import secrets

class Config(object):
    DEBUG = False
    TESTING = False

    db_username = 'bf4b93f804c0be'
    db_password = 'a6125a3a'
    db_host = 'us-cdbr-iron-east-05.cleardb.net'
    db_db = 'heroku_7174b26bd198011'

    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}/{}'.format(db_username, db_password, db_host, db_db)
    SECRET_KEY = secrets.token_hex(16)

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

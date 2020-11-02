import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'
    SITE_ADMIN = 'admin@test.my'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'dev.sqlite')

class ProductionConfig(Config):
    ENV = 'production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'prod.sqlite')

class TestingConfig(Config):
    ENV = 'testing'
    TESTING = True

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}


if __name__ == "__main__":
    print(config)
    print(config['development'])

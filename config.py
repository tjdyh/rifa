import os
basedir = os.path.abspath(os.path.dirname(__file__))

print(basedir)


class Config:
    # FLASK_CONFIG = 'default'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.163.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '465'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'False').lower() in \
        ['true', 'on', '1']
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'True')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME','zhb_zabbix@163.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD','DPCWOJUWEQSIEMUM')
    FLASKY_MAIL_SUBJECT_PREFIX = '[RIFA]'
    FLASKY_MAIL_SENDER = 'zhb_zabbix@163.com'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # print(FLASK_CONFIG)
    # print(FLASKY_ADMIN)

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    # SQLALCHEMY_POOL_SIZE = 50
    SQLALCHEMY_BINDS = {
        # 'instanc_name': 'oracle://user/password@ip:port/instance',
       ,
    }


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # wtform depend on Secret key to perform
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'salt key'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_MAIL_SUBJECT_PREFIX = '[FLASKY]'
    FLASK_MAIL_SENDER = 'FLASKY ADMIN <FLASKY@MAIL.COM>'
    FLASK_ADMIN = os.environ.get('FLAKSY_ADMIN')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://cc_user:AmzRedGsvcAdminAcc@127.0.0.1:3306/gsvcdatabase"

    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'chenyongle'
    MAIL_PASSWORD = 'testpass'
    

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = ""

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
    'default': DevelopmentConfig
}
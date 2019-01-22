import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = '1234567890123456789012345678901234567890'
    UPLOADS_DEFAULT_DEST = basedir + '/app/static'
    FLASKY_ADMIN = '13167288970'
    SERVER_NAME = '192.168.0.147:5000'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:19920720@127.0.0.1/smart'
    DEBUG = True
    if not os.path.exists(UPLOADS_DEFAULT_DEST):
        os.mkdir(UPLOADS_DEFAULT_DEST)

    @staticmethod
    def init_app(app):
        pass


class Release:
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = '\xc3m\x0e\xae\x1c\xcbs\x06pF\xa8\xe1\x84o\xaf\xe90\x00R=j\xce\x93&'
    UPLOADS_DEFAULT_DEST = basedir + '/app/static'
    FLASKY_ADMIN = '13167288970'
    SERVER_NAME = 'www.smart.com'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:lYp926233@127.0.0.1/share'
    DEBUG = False
    TESTING = False
    if not os.path.exists(UPLOADS_DEFAULT_DEST):
        os.mkdir(UPLOADS_DEFAULT_DEST)

    @staticmethod
    def init_app(app):
        pass

config = {
    'default': Config,
    'release': Release
}

#for sqllite
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = '23adflj24'
    #for sqllight
    """ SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db') """
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://app:MYapp123@localhost:3306/pm'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #Email Issues
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['loewecreations@gmail.com']
    TASKS_PER_PAGE = 4
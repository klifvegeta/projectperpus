import os
from flask_login import LoginManager
class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get ('OPENSHIFT_POSTGRESQL_DB_URL') if os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL') else 'postgresql://localhost:5432/perpustakaan'
    CSRF_ENABLED = True
    SECRET_KEY = 'terlalu'
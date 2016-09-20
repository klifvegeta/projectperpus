import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get ('OPENSHIFT_POSTGRESQL_DB_URL') if os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL') else 'postgresql://localhost:5432/perpustakaan'
    WTF_CSRF_ENABLE = True
    SECRET_KEY = "mantan-terindah"
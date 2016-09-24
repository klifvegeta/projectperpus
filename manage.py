from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5432/perpustakaan'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True)
    firstname = db.Column(db.String(20))
    lastname = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(54))

    time_registered = db.Column(db.DateTime)
    active = db.Column(db.Boolean)

    def __init__(self, username = None, email = None, firstname = None, lastname = None, active = None, password = None):
        self.username = username
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.active = active
        self.password = password
    @property
    def is_authenticated(self):
        return True
    @property
    def is_active(self):
        return True
    @property
    def is_anonymous(self):
        return False
    def get_id(self):
        try:
            return unicode(self.uid)
        except NameError:
            return str(self.uid)
    def __repr__(self):
        return '<User %r>' %(self.name)


class Buku(db.Model):
    ___tablename__ = 'buku'
    idbuku = db.Column(db.Integer, primary_key=True)
    judul_buku = db.Column(db.String(100))
    penulis_buku = db.Column(db.String(50))

    def __init__(self, judul_buku = None, penulis_buku = None):
        self.judul_buku = judul_buku
        self.penulis_buku = penulis_buku

class Transaksi(db.Model):
    __tablename__ = 'transaksi'
    idtransaksi = db.Column(db.Integer, primary_key=True)
    iduser = db.Column(db.Integer)
    idbuku = db.Column(db.Integer)
    tglpinjam = db.Column(db.DateTime)
    durasi = db.Column(db.Integer)

    def __ini__(self, iduser = None, idbuku = None, tglpinjam = None, durasi = None):
        self.iduser = iduser
        self.idbuku = idbuku
        self.tglpinjam = tglpinjam
        self.durasi = durasi

if __name__ == '__main__':
    manager.run()
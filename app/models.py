from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Users(UserMixin, db.Model):
    uid = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    nama = db.Column(db.String(200), nullable=False)
    notlp = db.Column(db.String(200), nullable=False)
    alamat = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    last_active = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return {'name': self.name}

    def getRole(self):
        return self.role

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Pjasa(db.Model):
    pid = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    toko = db.Column(db.String(200))
    email = db.Column(db.String(200), nullable=False)
    mobile = db.Column(db.String(200), nullable=False)
    alamat = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return {'name': self.name}

    def getRole(self):
        return self.role

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Orders(db.Model):
    oid = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    nama = db.Column(db.String(200), nullable=False)
    warna = db.Column(db.String(200), nullable=False)
    kertas = db.Column(db.String(200), nullable=False)
    catatan = db.Column(db.String(200), nullable=False)
    file = db.Column(db.String(200), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Product(db.Model):
    idp         = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    toko        = db.Column(db.String(200), nullable=False)
    unit        = db.Column(db.String(200), nullable=False)
    bw          = db.Column(db.String(200), nullable=False)
    berwarna    = db.Column(db.String(200), nullable=False)
    kertas      = db.Column(db.String(200), nullable=False)
    deskripsi   = db.Column(db.String(200), nullable=False)
    alamat      = db.Column(db.String(200))
    jam         = db.Column(db.String(200), nullable=False)

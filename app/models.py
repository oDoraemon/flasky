from . import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    id_role = db.Column(db.Integer, db.ForeignKey('roles.id'))
    email = db.Column(db.String(128), unique=True, index=True)
    password_hash = db.Column(db.String(256))
    confirmed = db.Column(db.Integer)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.String(64))

    def __repr__(self):
        return '<User %r>' % self.username

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

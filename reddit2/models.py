from datetime import datetime
from reddit2 import db, loginManager
from flask_login import UserMixin

@loginManager.user_loader
def loadUser(userID):
    return User.query.get(int(userID))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    profilePicture = db.Column(db.String(20), nullable=False, default='default.jpg')
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.dateCreated}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.String(240), nullable=False)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    edited = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.dateCreated}', '{self.body}')"

from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    __table_args__ = {
        # ‘mysql_engine‘: ‘InnoDB‘,   # 指定表的引擎
        'mysql_charset': 'utf8'  # 指定表的编码格式
    }
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<用户名:{}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1548673579046&di=65b7bc266fbe70313ac8e1dbba4b7b31&imgtype=0&src=http%3A%2F%2Fpic154.nipic.com%2Ffile%2F20180127%2F14015775_103417035658_2.jpg'.format(digest, size)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

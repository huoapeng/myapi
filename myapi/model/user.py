import datetime
from myapi import db

class UserModel(db.Model):
    # __tablename__ = 'todos'
    id = db.Column('user_id', db.Integer, primary_key=True)
    nickname = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(50))
    regist_date = db.Column(db.DateTime)
    projects = db.relationship('ProjectModel',
        backref=db.backref('owner', lazy='joined'), lazy='dynamic')

    def __init__(self, email, password):
        self.nickname = email[:email.find(r'@')]
        self.email = email
        self.password = password
        self.regist_date = datetime.datetime.now()

    def __repr__(self):
        return '<User %r>' % (self.nickname)

# tags = db.Table('tags',
#     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
#     db.Column('page_id', db.Integer, db.ForeignKey('page.id'))
# )

# class Page(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     tags = db.relationship('Tag', secondary=tags,
#         backref=db.backref('pages', lazy='dynamic'))

# class Tag(db.Model):
#     id = db.Column(db.Integer, primary_key=True)


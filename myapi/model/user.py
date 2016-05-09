import datetime
from myapi import db
from enum import user_status
from tag import tags

class UserModel(db.Model):
    # __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    area = db.Column(db.String(50))
    image = db.Column(db.String(50))
    description = db.Column(db.String(500))
    status = db.Column(db.Integer)
    regist_date = db.Column(db.DateTime)

    published_projects = db.relationship('ProjectModel',
        backref=db.backref('owner', lazy='joined'), lazy='dynamic')

    participate_tasks = db.relationship('TaskModel',
        backref=db.backref('successful_bidder', lazy='joined'), lazy='dynamic')

    tags = db.relationship('TagModel', secondary=tags,
        backref=db.backref('users', lazy='dynamic'))

    versions = db.relationship('VersionModel',
        backref=db.backref('owner', lazy='joined'), lazy='dynamic')

    notes = db.relationship('NoteModel',
        backref=db.backref('owner', lazy='joined'), lazy='dynamic')

    def __init__(self, email, password):
        self.nickname = email[:email.find(r'@')]
        self.email = email
        self.password = password
        self.regist_date = datetime.datetime.now()
        self.status = user_status.normal

    def __repr__(self):
        return '<User %r>' % (self.nickname)

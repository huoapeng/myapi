import datetime
from myapi import db
from enum import user_status
from tag import user_tags
from note import NoteModel
from message import NoteMessageModel

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    area = db.Column(db.String(50))
    image = db.Column(db.String(50))
    description = db.Column(db.String(4096))
    status = db.Column(db.Integer)
    regist_date = db.Column(db.DateTime)

    published_projects = db.relationship('ProjectModel',
        backref=db.backref('owner', lazy='joined'), lazy='dynamic')

    # won_tasks = db.relationship('TaskModel', foreign_keys='TaskModel.winner_id',
    #     backref=db.backref('owner', lazy='joined'), lazy='joined')

    tags = db.relationship('TagModel', secondary=user_tags,
        backref=db.backref('users', lazy='dynamic'))

    versions = db.relationship('VersionModel',
        backref=db.backref('owner', lazy='joined'), lazy='joined')
    # versionmessages = db.relationship('VersionMessageModel',
    #     backref=db.backref('owner', lazy='joined'), lazy='joined')

    notes = db.relationship('NoteModel',
        backref=db.backref('owner', lazy='joined'), lazy='joined')
    notemessages = db.relationship('NoteMessageModel',
        backref=db.backref('owner', lazy='joined'), lazy='joined')

    def __init__(self, email, password):
        self.nickname = email[:email.find(r'@')]
        self.email = email
        self.password = password
        self.regist_date = datetime.datetime.now()
        self.status = user_status.normal

    def __repr__(self):
        return '<User %r>' % (self.nickname)

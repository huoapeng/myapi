import datetime
from myapi import db
from enum import user_status, authorised_status
from tag import user_tags

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(200))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    area = db.Column(db.String(200))
    image = db.Column(db.String(500))
    description = db.Column(db.Text)
    status = db.Column(db.Integer)
    authorisedStatus = db.Column(db.Integer)
    registDate = db.Column(db.DateTime)

    published_projects = db.relationship('ProjectModel',
        backref=db.backref('owner', lazy='joined'), lazy='dynamic')
    
    tags = db.relationship('TagModel', secondary=user_tags,
        backref=db.backref('users', lazy='dynamic'))

    versions = db.relationship('VersionModel',
        backref=db.backref('owner', lazy='joined'), lazy='joined')

    notes = db.relationship('NoteModel',
        backref=db.backref('owner', lazy='joined'), lazy='joined')
    notemessages = db.relationship('NoteMessageModel',
        backref=db.backref('owner', lazy='joined'), lazy='joined')

    privateAuthority = db.relationship('PrivateAuthorisedModel', uselist=False,
        backref=db.backref('owner', lazy='joined'), lazy='joined')
    companyAuthority = db.relationship('CompanyAuthorisedModel', uselist=False,
        backref=db.backref('owner', lazy='joined'), lazy='joined')

    bidTasks = db.relationship('BidModel', backref='user')

    def __init__(self, email, password):
        self.nickname = email[:email.find(r'@')]
        self.email = email
        self.password = password
        self.registDate = datetime.datetime.now()
        self.status = user_status.normal
        self.authorisedStatus = authorised_status.none

    def __repr__(self):
        return '<User %r>' % (self.nickname)

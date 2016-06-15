import datetime
from flask import url_for
from myapi import db
from enum import user_status, authorised_status
from tag import user_tags

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(200))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    location = db.Column(db.String(200))
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
        backref=db.backref('owner', lazy='joined'), lazy='dynamic')

    notes = db.relationship('NoteModel',
        backref=db.backref('owner', lazy='joined'), lazy='dynamic')
    notemessages = db.relationship('NoteMessageModel',
        backref=db.backref('owner', lazy='joined'), lazy='dynamic')

    privateAuthority = db.relationship('PrivateAuthorisedModel', uselist=False,
        backref=db.backref('owner', lazy='joined'), lazy='joined')
    companyAuthority = db.relationship('CompanyAuthorisedModel', uselist=False,
        backref=db.backref('owner', lazy='joined'), lazy='joined')

    wonTasks = db.relationship('TaskModel',
        backref=db.backref('winner', lazy='joined'), lazy='dynamic')
    bidTasks = db.relationship('BidModel', lazy='dynamic')

    works = db.relationship('WorkModel',
        backref=db.backref('owner', lazy='joined'), lazy='dynamic')

    def __init__(self, email, password):
        self.nickname = email[:email.find(r'@')]
        self.email = email
        self.password = password
        self.registDate = datetime.datetime.now()
        self.status = user_status.normal
        self.authorisedStatus = authorised_status.none

    def __repr__(self):
        return '<User %r>' % (self.nickname)

    def serialize(self):
        return {
            'id': self.id,
            'nickname': self.nickname,
            'email': self.email,
            'phone': self.phone,
            'location': self.location,
            'image': url_for('.imageep', _external=True, userid=self.id, imagetype=1, filename=self.image) \
                if self.image else self.image,
            'description': self.description,
            'status': self.status,
            'authorisedStatus': self.authorisedStatus,
            'registDate': self.registDate.isoformat(),
            'tags': url_for('.userTags', _external=True, userid=self.id),
            'works': url_for('.userWorks', _external=True, userid=self.id, page=1),
            'publishedProjects': url_for('.publishedProjects', _external=True, userid=self.id, page=1),
            'wonProjects': url_for('.wonProjects', _external=True, userid=self.id, page=1)
        }


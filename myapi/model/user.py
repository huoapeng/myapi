import datetime, random
from flask import url_for
from myapi import db, app
from enum import user_status, file_type, authentication_type
from tag import user_tags
from myapi.common.image import getUploadFileUrl, getDefaultImageUrl

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(200))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    location = db.Column(db.String(200))
    imageLarge = db.Column(db.String(200))
    imageMedium = db.Column(db.String(200))
    imageSmall = db.Column(db.String(200))
    defaultImage = db.Column(db.String(200))
    description = db.Column(db.Text)
    status = db.Column(db.Integer)
    authenticationType = db.Column(db.Integer)
    registDate = db.Column(db.DateTime)

    publishedProjects = db.relationship('ProjectModel', backref=db.backref('owner', lazy='joined'), lazy='dynamic')
    tags = db.relationship('UserTagModel', secondary=user_tags, backref=db.backref('users', lazy='dynamic'))
    versions = db.relationship('VersionModel', backref=db.backref('owner', lazy='joined'), lazy='dynamic')
    notes = db.relationship('NoteModel', backref=db.backref('owner', lazy='joined'), lazy='dynamic')
    notemessages = db.relationship('NoteMessageModel', backref=db.backref('owner', lazy='joined'), lazy='dynamic')
    wonTasks = db.relationship('TaskModel', backref=db.backref('winner', lazy='joined'), lazy='dynamic')
    bidTasks = db.relationship('BidModel', lazy='dynamic')
    works = db.relationship('WorkModel', backref=db.backref('owner', lazy='joined'), lazy='dynamic')
    authentications = db.relationship('ApprovalModel', backref=db.backref('owner', lazy='joined'), lazy='dynamic')
    privateAuthenHistory = db.relationship('PrivateAuthenticateModel', 
        backref=db.backref('owner', lazy='joined'), lazy='dynamic')
    companyAuthenHistory = db.relationship('CompanyAuthenticateModel',
        backref=db.backref('owner', lazy='joined'), lazy='dynamic')
    bankAuthenHistory = db.relationship('BankModel',
        backref=db.backref('owner', lazy='joined'), lazy='dynamic')

    def __init__(self, email, password, nickname=None, phone=None, location=None, description=None):
        if nickname:
            self.nickname = nickname
        else:
            self.nickname = email[:email.find(r'@')]
        self.defaultImage = '{}.jpg'.format(random.randint(1, app.config['DEFAULT_IMAGE_COUNT']))
        self.email = email
        self.password = password
        self.phone = phone
        self.location = location
        self.description = description
        self.registDate = datetime.datetime.now()
        self.status = user_status.disable
        self.authenticationType = authentication_type.none

    def __repr__(self):
        return '<User %r>' % (self.nickname)

    def serialize(self):
        return {
            'id': self.id,
            'nickname': self.nickname,
            'email': self.email,
            'phone': self.phone,
            'location': self.location,
            'imageLarge': self.getImage(file_type.profileLarge),
            'imageMedium': self.getImage(file_type.profileMedium),
            'imageSmall': self.getImage(file_type.profileSmall),
            'description': self.description,
            'status': self.status,
            'authenticationType': self.authenticationType,
            'registDate': self.registDate.isoformat(),
            'tags': url_for('.userTags', _external=True, userid=self.id),
            'works': url_for('.userWorks', _external=True, userid=self.id, page=1),
            'publishedProjects': url_for('.userPublishedProjects', _external=True, userid=self.id, page=1),
            'wonProjects': url_for('.userWonProjects', _external=True, userid=self.id, page=1)
        }

    def getImage(self, imageType=file_type.profileSmall):
        if self.imageLarge and imageType == file_type.profileLarge:
            return getUploadFileUrl(imageType, self.id, self.imageLarge)
        elif self.imageMedium and imageType == file_type.profileMedium:
            return getUploadFileUrl(imageType, self.id, self.imageMedium)
        elif self.imageSmall and imageType == file_type.profileSmall:
            return getUploadFileUrl(imageType, self.id, self.imageSmall)
        else:
            return getDefaultImageUrl(self.defaultImage)



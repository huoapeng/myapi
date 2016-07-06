import datetime
from flask import url_for
from myapi import db
from enum import verify_type, authentication_type
from myapi.common.image import getUploadFileUrl
from myapi.model.enum import file_type

class ApprovalModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    authenticationType = db.Column(db.Integer)
    approvalStatus = db.Column(db.Integer)
    approvalDate = db.Column(db.DateTime)
    userid = db.Column(db.Integer, db.ForeignKey('user_model.id'))
    adminid = db.Column(db.Integer)

    privateAuthenticate = db.relationship('PrivateAuthenticateModel',
        backref=db.backref('approval', lazy='joined'), lazy='dynamic')

    companyAuthenticate = db.relationship('CompanyAuthenticateModel',
        backref=db.backref('approval', lazy='joined'), lazy='dynamic')

    bankAuthenticate = db.relationship('BankModel',
        backref=db.backref('approval', lazy='joined'), lazy='dynamic')

    def __init__(self, approvalStatus, userid, adminid):
        self.approvalStatus = approvalStatus
        self.approvalDate = datetime.datetime.now()
        self.userid = userid
        self.adminid = adminid

    def serialize(self):
        return {
            'id': self.id,
            'approvalStatus': self.approvalStatus,
            'approvalDate': self.approvalDate,
            'userid': self.userid,
            'user': url_for('.userep', _external=True, userid=self.userid),
            'adminid': self.adminid,
            'admin': url_for('.userep', _external=True, userid=self.adminid)
        }

class PrivateAuthenticateModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100))
    authenticateDate = db.Column(db.DateTime)
    identityID = db.Column(db.String(50), nullable=False)
    identityFrontImage = db.Column(db.String(100), nullable=False)
    identityBackImage = db.Column(db.String(100), nullable=False)

    approvalid = db.Column(db.Integer, db.ForeignKey('approval_model.id'))

    def __init__(self, name, identityID, identityFrontImage, identityBackImage):
        self.name = name
        self.authenticateDate = datetime.datetime.now()
        self.identityID = identityID
        self.identityFrontImage = identityFrontImage
        self.identityBackImage = identityBackImage

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'authenticateDate': self.authenticateDate,
            'identityID': self.identityID,
            'identityFrontImage': getUploadFileUrl(file_type.privateFront, self.owner_id,  self.identityFrontImage),
            'identityBackImage': getUploadFileUrl(file_type.privateBack, self.owner_id, self.identityBackImage),
        }

class CompanyAuthenticateModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100))
    authenticateDate = db.Column(db.DateTime)
    businessScope = db.Column(db.Text)
    licenseID = db.Column(db.String(500))
    licenseImage = db.Column(db.String(500))
    contactImage = db.Column(db.String(500))
    verifyType = db.Column(db.Integer)

    approvalid = db.Column(db.Integer, db.ForeignKey('approval_model.id'))

    def __init__(self, name, businessScope, licenseID, licenseImage, contactImage, verifyType):
        self.name = name
        self.authorisedDate = datetime.datetime.now()
        self.businessScope = businessScope
        self.licenseID = licenseID
        self.licenseImage = licenseImage
        self.contactImage = contactImage
        self.verifyType = verifyType

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'authorisedDate': self.authorisedDate,
            'businessScope': self.businessScope,
            'licenseID':self.licenseID,
            'licenseImage': getUploadFileUrl(file_type.companyLience, self.owner_id, self.licenseImage),
            'contactImage': getUploadFileUrl(file_type.companyContactCard, self.owner_id, self.contactImage),
            'verifyType': self.verifyType
        }

class BankModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    authenticateDate = db.Column(db.DateTime)
    bankAccount = db.Column(db.String(100))
    bankName = db.Column(db.String(500))
    bankLocation = db.Column(db.String(200))

    approvalid = db.Column(db.Integer, db.ForeignKey('approval_model.id'))

    def __init__(self, bankAccount, bankName, bankLocation):
        self.authenticateDate = datetime.datetime.now()
        self.bankAccount = bankAccount
        self.bankName = bankName
        self.bankLocation = bankLocation

    def serialize(self):
        return {
            'id': self.id,
            'authenticateDate': self.authenticateDate,
            'bankAccount': self.bankAccount,
            'bankName': bankName,
            'bankLocation': bankLocation
        }
        
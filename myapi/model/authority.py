import datetime
from flask import url_for
from myapi import db
from enum import verifyType, approvalStatus, approvalResult

class PrivateAuthorisedModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    identityID = db.Column(db.Integer)
    identityFrontImage = db.Column(db.String(500))
    identityBackImage = db.Column(db.String(500))
    authorisedDate = db.Column(db.DateTime)

    approvalStatus = db.Column(db.Integer)
    approvalResult = db.Column(db.Integer)
    approvalDate = db.Column(db.DateTime)

    owner_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))

    def __init__(self, name, identityID):
        self.name = name
        self.identityID = identityID
        self.authorisedDate = datetime.datetime.now()
        self.approvalStatus = approvalStatus.start

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'identityID': self.identityID,
            'identityFrontImage': url_for('.userep', _external=True, userid=self.identityFrontImage),
            'identityBackImage': url_for('.userep', _external=True, userid=self.identityBackImage),
            'authorisedDate': self.authorisedDate,
            'approvalStatus': self.approvalStatus,
            'approvalResult': self.approvalResult,
            'approvalDate': self.approvalDate,
        }

class CompanyAuthorisedModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    businessScope = db.Column(db.String(4096))
    businessLicenseID = db.Column(db.String(500))
    businessLicenseImage = db.Column(db.String(500))
    contactImage = db.Column(db.String(500))
    verifyType = db.Column(db.Integer)
    bankAccount = db.Column(db.String(500))
    bankName = db.Column(db.String(500))
    bankLocation = db.Column(db.String(500))
    authorisedDate = db.Column(db.DateTime)

    approvalStatus = db.Column(db.Integer)
    approvalResult = db.Column(db.Integer)
    approvalDate = db.Column(db.DateTime)

    owner_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))

    def __init__(self, name, businessScope, businessLicenseID, verifyType, bankAccount, bankName, bankLocation):
        self.name = name
        self.businessScope = businessScope
        self.businessLicenseID = businessLicenseID
        self.verifyType = verifyType
        self.bankAccount = bankAccount
        self.bankName = bankName
        self.bankLocation = bankLocation
        self.authorisedDate = datetime.datetime.now()


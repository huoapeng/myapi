import datetime
from myapi import db
from enum import task_status
from kind import task_kinds

class TaskModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    timespan = db.Column(db.String(200))
    requirements = db.Column(db.Text)
    bonus = db.Column(db.Integer)
    description = db.Column(db.Text)
    publishDate = db.Column(db.DateTime)
    bidderQualifiRequire = db.Column(db.String(100))
    bidderLocationRequire = db.Column(db.String(100))
    status = db.Column(db.Integer)
    receipt = db.Column(db.Boolean)
    receiptDes = db.Column(db.String(500))

    winnerid = db.Column(db.Integer, db.ForeignKey('user_model.id'))
    projectid = db.Column(db.Integer, db.ForeignKey('project_model.id'))

    kinds = db.relationship('KindModel', secondary=task_kinds, backref=db.backref('tasks', lazy='dynamic'))
    versions = db.relationship('VersionModel', backref=db.backref('task', lazy='joined'), lazy='dynamic')
    notes = db.relationship('NoteModel', backref=db.backref('task', lazy='joined'), lazy='dynamic')
    bidders = db.relationship('BidModel', lazy='dynamic')

    def __init__(self, name, timespan=None, requirements=None, bonus=0, description=None, 
        bidderQualifiRequire=None, bidderLocationRequire=None, receipt=False, receiptDes=None):
        self.name = name
        self.timespan = timespan
        self.requirements = requirements
        self.bonus = bonus
        self.description = description
        self.publishDate = datetime.datetime.now()
        self.bidderQualifiRequire = bidderQualifiRequire
        self.bidderLocationRequire = bidderLocationRequire
        self.status = task_status.disable
        self.receipt = receipt
        self.receiptDes = receiptDes

    def __repr__(self):
        return '<User %r>' % (self.name)
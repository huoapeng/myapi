import datetime
from myapi import db
from enum import task_status
from kind import task_kinds

class TaskModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    timespan = db.Column(db.String(200))
    requirements = db.Column(db.Text)
    bonus = db.Column(db.String(200))
    description = db.Column(db.Text)
    publishDate = db.Column(db.DateTime)
    bidder_qualification_requirement = db.Column(db.String(100))
    bidder_location_requirement = db.Column(db.String(100))
    receipt = db.Column(db.Boolean)
    receiptDescription = db.Column(db.String(200))
    status = db.Column(db.Integer)

    project_id = db.Column(db.Integer, db.ForeignKey('project_model.id'))

    kinds = db.relationship('KindModel', secondary=task_kinds,
        backref=db.backref('tasks', lazy='dynamic'))

    versions = db.relationship('VersionModel',
        backref=db.backref('task', lazy='joined'), lazy='dynamic')

    notes = db.relationship('NoteModel',
        backref=db.backref('task', lazy='joined'), lazy='dynamic')

    winner_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))
    bidders = db.relationship('BidModel', lazy='dynamic')

    def __init__(self, name, timespan=None, requirements=None, bonus=None, description=None, 
        bidder_qualification_requirement=None, bidder_location_requirement=None, receipt=False, receiptDes=None):
        self.name = name
        self.timespan = timespan
        self.requirements = requirements
        self.bonus = bonus
        self.description = description
        self.publishDate = datetime.datetime.now()
        self.bidder_qualification_requirement = bidder_qualification_requirement
        self.bidder_location_requirement = bidder_location_requirement
        self.receipt = receipt
        self.receiptDescription = receiptDes
        self.status = task_status.bidding

    def __repr__(self):
        return '<User %r>' % (self.name)
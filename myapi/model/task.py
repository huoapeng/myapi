import datetime
from myapi import db
from enum import task_status
from kind import task_kinds, KindModel
from bid import bid
from user import UserModel
from version import VersionModel
from note import NoteModel

class TaskModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    timespan = db.Column(db.Integer)
    requirements = db.Column(db.String(100))
    bonus = db.Column(db.Integer)
    description = db.Column(db.String(5000))
    publishDate = db.Column(db.DateTime)
    bidder_qualification_requirement = db.Column(db.String(100))
    bidder_area_requirement = db.Column(db.String(100))
    status = db.Column(db.Integer)

    winner_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))

    project_id = db.Column(db.Integer, db.ForeignKey('project_model.id'))

    kinds = db.relationship('KindModel', secondary=task_kinds,
        backref=db.backref('tasks', lazy='dynamic'))

    bidders = db.relationship('UserModel', secondary=bid,
        backref=db.backref('participate_tasks', lazy='dynamic'))

    versions = db.relationship('VersionModel',
        backref=db.backref('task', lazy='joined'), lazy='joined')

    notes = db.relationship('NoteModel',
        backref=db.backref('task', lazy='joined'), lazy='joined')

    def __init__(self, name, timespan=None, requirements=None, bonus=None, description=None, 
        bidder_qualification_requirement=None, bidder_area_requirement=None):
        self.name = name
        self.timespan = timespan
        self.requirements = requirements
        self.bonus = bonus
        self.description = description
        self.publishDate = datetime.datetime.now()
        self.bidder_qualification_requirement = bidder_qualification_requirement
        self.bidder_area_requirement = bidder_area_requirement
        self.status = task_status.normal

    def __repr__(self):
        return '<User %r>' % (self.name)
from myapi import db
from enum import task_status
from types import task_types

class TaskModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer)
    name = db.Column(db.String(100))
    timespan = db.Column(db.Integer)
    requirements = db.Column(db.String(100))
    reward = db.Column(db.Integer)
    description = db.Column(db.String(5000))
    publishDate = db.Column(db.DateTime)
    bidder_qualification_requirement = db.Column(db.String(100))
    bidder_area_requirement = db.Column(db.String(100))

    types = db.relationship('TypeModel', secondary=task_types,
        backref=db.backref('tasks', lazy='dynamic'))

    project_id = db.Column(db.Integer, db.ForeignKey('project_model.id'))
    # owner_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))
    bidder_successful = db.Column(db.Integer, db.ForeignKey('user_model.id'))

    # user = relationship('User', foreign_keys='Friend.user_id')
    # friend = relationship('User', foreign_keys='Friend.friend_id')

    versions = db.relationship('VersionModel',
        backref=db.backref('task', lazy='joined'), lazy='dynamic')

    notes = db.relationship('NoteModel',
        backref=db.backref('task', lazy='joined'), lazy='dynamic')

    bidders = db.relationship('UserModel',
        backref=db.backref('bidde_tasks', lazy='joined'), lazy='joined')

    def __init__(self, taskName):
        self.name = taskName
        self.status = task_status.normal

    def __repr__(self):
        return '<User %r>' % (self.name)
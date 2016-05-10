from myapi import db
from enum import project_status
from types import project_types

class ProjectModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(5000))
    status = db.Column(db.Integer)
    type_id = db.Column(db.Integer)

    types = db.relationship('TypeModel', secondary=project_types,
        backref=db.backref('projects', lazy='dynamic'))

    owner_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))

    tasks = db.relationship('TaskModel',
        backref=db.backref('project', lazy='joined'), lazy='dynamic')

    def __init__(self, projectName):
        self.name = projectName
        self.status = project_status.normal

    def __repr__(self):
        return '<User %r>' % (self.name)
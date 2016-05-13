from myapi import db
from enum import project_status
from types import project_types

class ProjectModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(5000))
    status = db.Column(db.Integer)
    type_id = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))

    types = db.relationship('TypeModel', secondary=project_types,
        backref=db.backref('projects', lazy='dynamic'))

    tasks = db.relationship('TaskModel',
        backref=db.backref('project', lazy='joined'), lazy='dynamic')

    def __init__(self, projectName, description=None, type_id=None, owner_id=None):
        self.name = projectName
        self.description = description
        self.status = project_status.normal
        self.type_id = type_id
        self.owner_id = owner_id

    def __repr__(self):
        return '<User %r>' % (self.name)
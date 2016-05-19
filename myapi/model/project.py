import datetime
from myapi import db
from enum import project_status
from kind import project_kinds

class ProjectModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    status = db.Column(db.Integer)
    description = db.Column(db.String(4096))
    publish_date = db.Column(db.DateTime)

    owner_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))
    # owner = db.relationship('UserModel',
    #      backref=db.backref('published_projects', lazy='dynamic'))

    # kind_id = db.Column(db.Integer)
    kinds = db.relationship('KindModel', secondary=project_kinds,
        backref=db.backref('projects', lazy='dynamic'))

    # tasks = db.relationship('TaskModel',
    #     backref=db.backref('project', lazy='joined'), lazy='dynamic')

    def __init__(self, projectName, description=None):
        self.name = projectName
        self.status = project_status.normal
        self.description = description
        self.publish_date = datetime.datetime.now()

    def __repr__(self):
        return '<User %r>' % (self.name)
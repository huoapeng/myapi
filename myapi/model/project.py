import datetime
from flask import url_for
from myapi import db
from enum import project_status

class ProjectModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    status = db.Column(db.Integer)
    description = db.Column(db.Text)
    publish_date = db.Column(db.DateTime)

    ownerid = db.Column(db.Integer, db.ForeignKey('user_model.id'))

    tasks = db.relationship('TaskModel',
        backref=db.backref('project', lazy='joined'), lazy='dynamic')

    def __init__(self, projectName, description=None):
        self.name = projectName
        self.status = project_status.disable
        self.description = description
        self.publish_date = datetime.datetime.now()

    def __repr__(self):
        return '<User %r>' % (self.name)

    def serialize(self):
        return {
            'ownerid': self.ownerid,
            'projectId': self.id,
            'projectName': self.name,
            'description': self.description,
            'publish_date': self.publish_date.isoformat(),
            'tasks_url':url_for('.getTasksByProjectID', _external=True, projectid=self.id),
            'owner':url_for('.userep', _external=True, userid=self.ownerid)
        }
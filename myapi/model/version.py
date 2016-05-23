import datetime
from myapi import db
from enum import version_status

class VersionModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(500))
    image = db.Column(db.String(500))
    title = db.Column(db.String(500))
    publish_date = db.Column(db.DateTime)
    status = db.Column(db.Integer)

    task_id = db.Column(db.Integer, db.ForeignKey('task_model.id'))
    
    def __init__(self, title):
        self.title = title
        self.publish_date = datetime.datetime.now()
        self.status = version_status.normal

    def __repr__(self):
        return '<User %r>' % (self.title)

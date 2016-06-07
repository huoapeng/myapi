import datetime
from flask import url_for
from myapi import db
from enum import version_status

class VersionModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(500))
    image = db.Column(db.String(500))
    title = db.Column(db.String(500))
    description = db.Column(db.Text)
    publish_date = db.Column(db.DateTime)
    status = db.Column(db.Integer)

    task_id = db.Column(db.Integer, db.ForeignKey('task_model.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))

    def __init__(self, title, description, image):
        self.title = title
        self.description = description
        self.image = image
        self.publish_date = datetime.datetime.now()
        self.status = version_status.normal

    def __repr__(self):
        return '<User %r>' % (self.title)

    def serialize(self):
        return {
            'id': self.id,
            'image': url_for('.imageep', _external=True, userid=self.user_id, imagetype=1, filename=self.image)\
                if self.image else self.image,
            'title': self.title,
            'description': self.description,
            'publish_date': self.publish_date,
            'status': self.status,
            'user_id': self.user_id,
            'task_id': self.task_id
        }
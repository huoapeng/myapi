import datetime
from flask import url_for
from myapi import db
from myapi.model.enum import work_status

class WorkModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    image = db.Column(db.String(500))
    description = db.Column(db.Text)
    status = db.Column(db.Integer)
    publish_date = db.Column(db.DateTime)

    owner_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))

    # messages = db.relationship('NoteMessageModel', order_by="NoteMessageModel.publish_date",
    #     backref=db.backref('work', lazy='joined'), lazy='dynamic')

    def __init__(self, title=None, image=None, description=None):
        self.title = title
        self.image = image
        self.description = description
        self.status = work_status.normal
        self.publish_date = datetime.datetime.now()

    def __repr__(self):
        return '<User %r>' % (self.title)

    def serialize(self):
        return {
            'userid': self.owner_id,
            'workid': self.id,
            'title': self.title,
            'image': getImageUrl(userid=self.owner_id, imageType=7, imageName=self.image) \
                if self.image else self.image,
            'description': self.description,
            'status': self.status,
            'publish_date': self.publish_date.isoformat(),
            'owner':url_for('.userep', _external=True, userid=self.owner_id)
        }
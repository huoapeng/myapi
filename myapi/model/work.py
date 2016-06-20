import datetime
from flask import url_for
from myapi import db
from myapi.model.tag import work_tags
from myapi.model.enum import work_status
from myapi.common.image import getImageUrl

class WorkModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))
    file = db.Column(db.String(200))
    description = db.Column(db.Text)
    copyright = db.Column(db.Integer)
    status = db.Column(db.Integer)
    publish_date = db.Column(db.DateTime)

    owner_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))

    tags = db.relationship('WorkTagModel', secondary=work_tags,
        backref=db.backref('works', lazy='dynamic'))

    # messages = db.relationship('NoteMessageModel', order_by="NoteMessageModel.publish_date",
    #     backref=db.backref('work', lazy='joined'), lazy='dynamic')

    def __init__(self, title=None, image=None, file=None, description=None, copyright=None):
        self.title = title
        self.image = image
        self.file = file
        self.description = description
        self.copyright = copyright
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
            'file': '',
            'description': self.description,
            'copyright': self.copyright,
            'status': self.status,
            'publish_date': self.publish_date.isoformat(),
            'owner':url_for('.userep', _external=True, userid=self.owner_id)
        }
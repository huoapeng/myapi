import datetime
from myapi import db
from enum import note_status

class NoteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    publish_date = db.Column(db.DateTime)
    status = db.Column(db.Integer)

    task_id = db.Column(db.Integer, db.ForeignKey('task_model.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))

    messages = db.relationship('NoteMessageModel', order_by="NoteMessageModel.publish_date",
        backref=db.backref('note', lazy='joined'), lazy='joined')

    def __init__(self, title):
        self.title = title
        self.publish_date = datetime.datetime.now()
        self.status = note_status.normal

    def __repr__(self):
        return '<User %r>' % (self.title)

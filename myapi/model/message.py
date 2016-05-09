from myapi import db
from enum import project_status

class MessageModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(1000))
    publish_date = db.Column(db.DateTime)

    types = db.Column(db.Integer)
	belong_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))

    def __init__(self, message, types):
        self.message = message
        self.publish_date = datetime.datetime.now()
        self.types = types

    def __repr__(self):
        return '<User %r>' % (self.message)
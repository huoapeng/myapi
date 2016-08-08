import datetime
from myapi import db

# class VersionMessageModel(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     message = db.Column(db.String(1000))
#     publish_date = db.Column(db.DateTime)

#     version_id = db.Column(db.Integer, db.ForeignKey('version_model.id'))
#     user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))

#     def __init__(self, message):
#         self.message = message
#         self.publish_date = datetime.datetime.now()

#     def __repr__(self):
#         return '<User %r>' % (self.message)


class NoteMessageModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    publishDate = db.Column(db.DateTime)

    note_id = db.Column(db.Integer, db.ForeignKey('note_model.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))

    def __init__(self, message):
        self.message = message
        self.publish_date = datetime.datetime.now()

    def __repr__(self):
        return '<User %r>' % (self.message)

    def serialize(self):
        return {
            'userid': self.owner.id,
            'userName': self.owner.nickname,
            'userImage': self.owner.getImage(),
            'message': self.message,
            'publishDate': self.publish_date
        }
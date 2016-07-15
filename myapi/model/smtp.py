import datetime
from myapi import db

class EmailModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    params = db.Column(db.Text)
    sendDate = db.Column(db.DateTime)
    expires = db.Column(db.DateTime)

    to_user = db.Column(db.String(200))

    def __init__(self, to_user=None, params=None, expires=None):
        self.to_user = to_user
        self.params = params
        self.sendDate = datetime.datetime.now()
        self.expires = expires

    def serialize(self):
        return {
            # 'noteid': self.id,
            # 'userid': self.owner.id,
            # 'userName': self.owner.nickname,
            # 'userImage': self.owner.getImage(),
            # 'title': self.title,
            # 'publishDate': self.publish_date.isoformat()
        }
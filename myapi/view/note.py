from flask import url_for
from myapi.common.image import getUserImage

class NoteView():

    def __init__(self, note_id, owner_id, owner_name, owner_image, title, publish_date):
        self.note_id = note_id
        self.owner_id = owner_id
        self.owner_name = owner_name
        self.owner_image = owner_image
        self.title = title
        self.publish_date = publish_date

    def serialize(self):
        return {
            'noteid': self.note_id,
            'userid': self.owner_id,
            'userName': self.owner_name,
            'userImage': getUserImage(self.owner_id, self.owner_image),
            'title': self.title,
            'publishDate': self.publish_date.isoformat()
        }

from flask import url_for
from myapi.common.image import getUserImage

class NoteMessageView():

    def __init__(self, owner_id, owner_name, owner_image, message, publish_date):
        self.owner_id = owner_id
        self.owner_name = owner_name
        self.owner_image = owner_image
        self.message = message
        self.publish_date = publish_date

    def serialize(self):
        return {
            'userid': self.owner_id,
            'userName': self.owner_name,
            'userImage': getUserImage(self.owner_id, self.owner_image),
            'message': self.message,
            'publishDate': self.publish_date
        }

from flask import url_for
from myapi.common.image import getFileUrl

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
            'userImage': getFileUrl(self.owner_id, 1, self.owner_image) if self.owner_image else self.owner_image,
            'message': self.message,
            'publishDate': self.publish_date
        }

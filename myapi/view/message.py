from flask import url_for

class NoteMessageView():

    def __init__(self, user_id, user_name, user_image, message, publish_date):
        self.user_id = user_id
        self.user_name = user_name
        self.user_image = user_image
        self.message = message
        self.publish_date = publish_date

    def __repr__(self):
        return '<User %r>' % (self.message)

    def serialize(self):
        return {
            'userid': self.user_id,
            'userName': self.user_name,
            'userImage': getImageUrl(userid=self.user_id, imageType=1, imageName=self.user_image) \
                if self.user_image else self.user_image,
            'message': self.message,
            'publishDate': self.publish_date
        }

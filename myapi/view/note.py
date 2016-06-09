from flask import url_for

class NoteView():

    def __init__(self, note_id, user_id, user_name, user_image, title, publish_date):
        self.note_id = note_id
        self.user_id = user_id
        self.user_name = user_name
        self.user_image = user_image
        self.title = title
        self.publish_date = publish_date

    def serialize(self):
        return {
            'noteid': self.note_id,
            'userid': self.user_id,
            'userName': self.user_name,
            'userImage': url_for('.imageep', userid=self.user_id, imagetype=0, filename=self.user_image, \
                _external=True) if self.user_image else self.user_image,
            'title': self.title,
            'publishDate': self.publish_date
        }

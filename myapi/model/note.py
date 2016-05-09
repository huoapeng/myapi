import datetime
from myapi import db

class NoteModel(db.Model):
    # __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    publish_date = db.Column(db.DateTime)

    task_id = db.Column(db.Integer, db.ForeignKey('task_model.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))
    
    def __init__(self, file, title, description):
        self.file = file
        self.title = title
        self.regist_date = datetime.datetime.now()

    def __repr__(self):
        return '<User %r>' % (self.title)

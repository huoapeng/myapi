from myapi import db

user_tags = db.Table('user_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag_model.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user_model.id'))
)

class TagModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name
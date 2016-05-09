from myapi import db

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag_model.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user_model.id'))
)


class TagModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
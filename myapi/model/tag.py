from myapi import db

user_tags = db.Table('user_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('user_tag_model.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user_model.id'))
)

work_tags = db.Table('work_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('work_tag_model.id')),
    db.Column('work_id', db.Integer, db.ForeignKey('work_model.id'))
)

class UserTagModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

class WorkTagModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

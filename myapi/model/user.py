from myapi import db

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(50))
    email = db.Column(db.String(120))
    password = db.Column(db.String(50))

    def __init__(self, email, password):
        self.nickname = email
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.nickname)
# , unique=True

# class Person(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))
#     addresses = db.relationship('Address', backref='person',
#                                 lazy='dynamic')

# class Address(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(50))
#     person_id = db.Column(db.Integer, db.ForeignKey('person.id'))

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))
#     addresses = db.relationship('Address',
#         backref=db.backref('person', lazy='joined'), lazy='dynamic')

# tags = db.Table('tags',
#     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
#     db.Column('page_id', db.Integer, db.ForeignKey('page.id'))
# )

# class Page(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     tags = db.relationship('Tag', secondary=tags,
#         backref=db.backref('pages', lazy='dynamic'))

# class Tag(db.Model):
#     id = db.Column(db.Integer, primary_key=True)


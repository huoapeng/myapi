from myapi import db
from enum import kind_status

# project_kinds = db.Table('project_kinds',
#     db.Column('kind_id', db.Integer, db.ForeignKey('kind_model.id'), primary_key=True),
#     db.Column('project_id', db.Integer, db.ForeignKey('project_model.id'), primary_key=True)
# )

task_kinds = db.Table('task_kinds',
    db.Column('kind_id', db.Integer, db.ForeignKey('kind_model.id'), primary_key=True),
    db.Column('task_id', db.Integer, db.ForeignKey('task_model.id'), primary_key=True)
)

class KindModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    status = db.Column(db.Integer)

    parent_id = db.Column(db.Integer, db.ForeignKey('kind_model.id'))

    parent = db.relationship('KindModel', remote_side=[id], 
        backref=db.backref('kids', lazy='dynamic'), lazy='joined')

    def __init__(self, name):
    	self.name = name
        self.status = kind_status.normal
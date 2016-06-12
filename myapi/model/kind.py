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
    parent_id = db.Column(db.Integer)
    status = db.Column(db.Integer)

    def __init__(self, name, parent_id=None):
    	self.name = name
    	self.parent_id = parent_id
        self.status = kind_status.normal
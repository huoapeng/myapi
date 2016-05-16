from myapi import db

project_types = db.Table('project_types',
    db.Column('type_id', db.Integer, db.ForeignKey('type_model.id')),
    db.Column('project_id', db.Integer, db.ForeignKey('project_model.id'))
)

task_types = db.Table('task_types',
    db.Column('type_id', db.Integer, db.ForeignKey('type_model.id')),
    db.Column('task_id', db.Integer, db.ForeignKey('task_model.id'))
)

class TypeModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    parent_id = db.Column(db.Integer)

    def __init__(self, name, parent_id):
    	self.name = name
    	self.parent_id = parent_id

    
from myapi import db

class ProjectModel(db.Model):
    id = db.Column('project_id', db.Integer, primary_key=True)
    project_name = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.user_id'))

    def __init__(self, projectName):
        self.project_name = projectName

    def __repr__(self):
        return '<User %r>' % (self.nickname)
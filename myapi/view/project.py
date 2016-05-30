

from flask import url_for

class UserPublishedProjectsView(object):

    def __init__(self, projectid, projectname, kind_str_list):
        self.projectid = projectid
        self.projectname = projectname
        self.kind_str_list = kind_str_list

    def serialize(self):
        return {
            'projectId': self.projectid,
            'projectName': self.projectname,
            'projectKinds': ','.join(self.kind_str_list),
            'tasks_url':url_for('.getTasksByProjectID', _external=True, projectid=self.projectid),
        }
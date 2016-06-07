

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

class UserBidProjectsView(object):

    def __init__(self, userid, projectid, projectname, kind_str_list):
        self.userid = userid
        self.projectid = projectid
        self.projectname = projectname
        self.kind_str_list = kind_str_list

    def serialize(self):
        return {
            'userid': self.userid,
            'projectId': self.projectid,
            'projectName': self.projectname,
            'projectKinds': ','.join(self.kind_str_list),
            'tasks_url':url_for('.GetTaskListByBidderID', _external=True, projectid=self.projectid,\
                 bidderid=self.userid),
        }
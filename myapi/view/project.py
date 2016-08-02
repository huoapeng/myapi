

from flask import url_for, request

class UserBidProjectsView(object):

    def __init__(self, userid, projectid, projectname):
        self.userid = userid
        self.projectid = projectid
        self.projectname = projectname

    def serialize(self):
        return {
            'userid': self.userid,
            'projectId': self.projectid,
            'projectName': self.projectname,
            'tasks_url':url_for('.getTasksByProjectID', _external=True, projectid=self.projectid,
                bidderid=self.userid)
                # bidderid=request.args.get('bidderid'))
        }
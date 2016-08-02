
from flask import url_for

class TaskDetailView(object):

    def __init__(self, 
            task,
            projectid,
            projectName,
            userid,
            userName,
            userLocation,
            kind_str_list,
        ):
        self.task
        self.projectid = projectid
        self.projectName = projectName
        self.userid = userid
        self.userName = userName
        self.userLocation = userLocation
        self.kind_str_list = kind_str_list

    def serialize(self):
        return {
            'task': self.task.serialize(),
            'projectid': self.projectid,
            'projectName': self.projectName,
            'projectURI': url_for('.projectep', projectid=self.projectid, _external=True),
            'userid': self.userid,
            'userName': self.userName,
            'userLocation': self.userLocation,
            'userURI': url_for('.userep', userid=self.userid, _external=True),
            'taskKinds': ','.join(self.kind_str_list)
        }


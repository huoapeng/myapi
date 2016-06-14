
from flask import url_for

class TaskDetailView(object):

    def __init__(self, 
            taskid,
            taskName,
            projectid,
            projectName,
            userid,
            userName,
            userLocation,
            timespan,
            requirements,
            bonus,
            description,
            publishDate,
            bidder_qualification_requirement,
            bidder_location_requirement,
            status,
            kind_str_list,
        ):
        self.taskid = taskid
        self.taskName = taskName
        self.projectid = projectid
        self.projectName = projectName
        self.userid = userid
        self.userName = userName
        self.userLocation = userLocation
        self.timespan = timespan
        self.requirements = requirements
        self.bonus = bonus
        self.description = description
        self.publishDate = publishDate
        self.bidder_qualification_requirement = bidder_qualification_requirement
        self.bidder_location_requirement = bidder_location_requirement
        self.status = status
        self.kind_str_list = kind_str_list

    def serialize(self):
        return {
            'taskid': self.taskid,
            'taskName': self.taskName,
            'projectid': self.projectid,
            'projectName': self.projectName,
            'projectURI': url_for('.projectep', projectid=self.projectid, _external=True),
            'userid': self.userid,
            'userName': self.userName,
            'userLocation': self.userLocation,
            'userURI': url_for('.userep', userid=self.userid, _external=True),
            'timespan': self.timespan,
            'requirements': self.requirements,
            'bonus': self.bonus,
            'description': self.description,
            'publishDate': self.publishDate,
            'bidder_qualification_requirement': self.bidder_qualification_requirement,
            'bidder_location_requirement': self.bidder_location_requirement,
            'status': self.status,
            'taskKinds': ','.join(self.kind_str_list)
        }



class TaskOfMovieMarketView(object):

    def __init__(self, 
            taskid,
            taskName,
            projectid,
            projectName,
            userid,
            userName,
            publishDate,
            bonus,
            area,
            bidder_area_requirement,
            bidder_qualification_requirement,
            kind_str_list,
        ):
        self.taskid = taskid
        self.taskName = taskName
        self.projectid = projectid
        self.projectName = projectName
        self.userid = userid
        self.userName = userName
        self.publishDate = publishDate
        self.bonus = bonus
        self.area = area
        self.bidder_area_requirement = bidder_area_requirement
        self.bidder_qualification_requirement = bidder_qualification_requirement
        self.kind_str_list = kind_str_list
        
        # self.bidder_area_requirement = bidder_area_requirement
        # self.bidder_qualification_requirement = bidder_qualification_requirement
        # self.timespan = timespan

        # self.requirements = requirements
        # self.description = description

    def serialize(self):
        return {
            'taskid': self.taskid,
            'taskName': self.taskName,
            'projectid': self.projectid,
            'projectName': self.projectName,
            'userid': self.userid,
            'userName': self.userName,
            'publishDate': self.publishDate,
            'bonus': self.bonus,
            'area': self.area,
            'bidder_area_requirement': self.bidder_area_requirement,
            'bidder_qualification_requirement': self.bidder_qualification_requirement,
            'taskKinds': ','.join(self.kind_str_list)
        }


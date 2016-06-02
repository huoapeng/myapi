from flask import url_for

class UserMarketView(object):

    def __init__(self, 
            userid,
            userImage,
            userName,
            authorisedStatus,
            # authorisedId,
            area,
            wonTaskCount,
            # goodReputationPercent,
            profileIntegrityPercent,
            phone,
            email,
            tag_str_list
        ):
        self.userid = userid
        self.userImage = userImage
        self.userName = userName
        self.authorisedStatus = authorisedStatus
        # self.authorisedId = authorisedId
        self.area = area
        self.wonTaskCount = wonTaskCount
        # self.goodReputationPercent = goodReputationPercent
        self.profileIntegrityPercent = profileIntegrityPercent
        self.phone = phone
        self.email = email
        self.tag_str_list = tag_str_list

    def serialize(self):
        return {
            'userid': self.userid,
            'user_image_url':'',
            'userName': self.userName,
            'authorisedStatus': self.authorisedStatus,
            # 'authorisedId': self.authorisedId,
            'area': self.area,
            'wonTaskCount': self.wonTaskCount,
            'profileIntegrityPercent': self.profileIntegrityPercent,
            'phone': self.phone,
            'email': self.email,
            'tags': ','.join(self.tag_str_list)
        }


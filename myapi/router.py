
from flask import Blueprint
from flask.ext.restful import Api

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

from myapi.resources.profile import Profile
api.add_resource(Profile, '/profile')

from myapi.resources.general import general
api.add_resource(general, '/general/<string:method>')

from myapi.resources.file import UploadFile
api.add_resource(UploadFile, '/uploadfile')

from myapi.resources.user import User, ChangePassword, ChangeUserStatus, GetUserList, GetUserMarketList
api.add_resource(User, '/user', '/user/<int:userid>',  endpoint='userep')
api.add_resource(ChangePassword, '/changepwd')
api.add_resource(ChangeUserStatus, '/changeuserstatus')
api.add_resource(GetUserList, '/userlist/<int:page>')
api.add_resource(GetUserMarketList, '/usermarketlist/<int:page>')

from myapi.resources.tag import UserTag, UserTags, UserTagList, SearchUserTagsByName, \
	WorkTag, WorkTags, SearchWorkTagsByName
api.add_resource(UserTag, '/usertag', '/usertag/<int:tagid>')
api.add_resource(UserTags, '/<int:userid>/usertags', endpoint='userTags')
api.add_resource(UserTagList, '/usertaglist/<int:page>')
api.add_resource(SearchUserTagsByName, '/search/usertaglist/<string:keyword>')
api.add_resource(WorkTag, '/worktag', '/worktag/<int:tagid>')
api.add_resource(WorkTags, '/<int:workid>/worktags', endpoint='workTags')
api.add_resource(SearchWorkTagsByName, '/search/worktaglist/<string:keyword>')

from myapi.resources.project import Project, GetProjectDetail, GetProjectList, \
	UserPublishedProjects, UserParticipateProjects
api.add_resource(Project, '/project', '/project/<int:projectid>', endpoint='projectep')
api.add_resource(GetProjectDetail, '/projectdetail/<int:projectid>', endpoint='projectdetailep')
api.add_resource(GetProjectList, '/projectlist/<int:page>', endpoint='projectlistep')
api.add_resource(UserPublishedProjects, '/userPublishedProjects/<int:page>', endpoint='userPublishedProjects')
api.add_resource(UserParticipateProjects, '/userParticipateProjects/<int:page>', endpoint='userParticipateProjects')

from myapi.resources.bid import Bid, BidList
api.add_resource(Bid, '/bid', '/<int:userid>/bid/<int:projectid>')
api.add_resource(BidList, '/<int:projectid>/bidlist')

from myapi.resources.version import Version, TaskVersions
api.add_resource(Version, '/version', '/version/<int:versionid>')
api.add_resource(TaskVersions, '/<int:projectid>/projectversions')

from myapi.resources.note import Note, TaskNotes
api.add_resource(Note, '/note', '/note/<int:noteid>')
api.add_resource(TaskNotes, '/<int:projectid>/projectnotes')

from myapi.resources.authentication import AuthenticationList, Approval, \
    PrivateAuthenticate, CompanyAuthenticate, BankAuthenticate, UserAuthentication
api.add_resource(AuthenticationList, '/authenticationlist')
api.add_resource(UserAuthentication, '/userauthen', endpoint='userAuthen')
api.add_resource(Approval, '/approval')
api.add_resource(PrivateAuthenticate, '/privateauthen')
api.add_resource(CompanyAuthenticate, '/companyauthen')
api.add_resource(BankAuthenticate, '/bankauthen')

from myapi.resources.category import Category, CategoryList, SearchCategorysByName
api.add_resource(Category, '/category', '/category/<int:cid>')
api.add_resource(CategoryList, '/categorylist')
api.add_resource(SearchCategorysByName, '/search/categorylist/<string:keyword>')

from myapi.resources.message import NoteMessage, NoteMessageList
api.add_resource(NoteMessage, '/notemessage')
api.add_resource(NoteMessageList, '/<int:noteid>/notemessagelist')

from myapi.resources.work import Work, UserWorks
api.add_resource(Work, '/work', '/work/<int:workid>')
api.add_resource(UserWorks, '/<int:userid>/userworks/<int:page>', endpoint='userWorks')

from myapi.resources.smtp import sendEmail
api.add_resource(sendEmail, '/sendemail')

from myapi.resources.recommend import RecommendType, RecommendTypeList, RecommendItem, RecommendItemList
api.add_resource(RecommendType, '/recommendtype', '/recommendtype/<int:id>')
api.add_resource(RecommendTypeList, '/recommendtypelist')
api.add_resource(RecommendItem, '/recommenditem', '/recommenditem/<int:id>')
api.add_resource(RecommendItemList, '/<int:typeid>/recommenditemlist', endpoint='recommenditemep')


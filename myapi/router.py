
from flask import Blueprint
from flask.ext.restful import Api
from myapi.resources.general import general, image
from myapi.resources.user import User, ChangePassword, GetUserList, GetuserDetailList
from myapi.resources.tag import Tag, UserTags, SearchTagsByName, TagList
from myapi.resources.project import Project, UserPublishedProjects, UserWonProjects
from myapi.resources.task import Task, GetTaskListByProjectID, GetTaskListByBidderID, \
	GetTaskList, GetVRTaskList, GetMoiveTaskList, GetTaskDetail
from myapi.resources.version import Version, TaskVersions
from myapi.resources.note import Note, TaskNotes
from myapi.resources.kind import Kind, KindList, SearchKindsByName
from myapi.resources.message import NoteMessage, NoteMessageList
from myapi.resources.profile import Profile
from myapi.resources.authorityPrivate import AuthorityPrivate, AuthorityPrivateList
from myapi.resources.authorityCompany import AuthorityCompany, AuthorityCompanyList
from myapi.resources.bid import Bid, BidList
from myapi.resources.work import Work, UserWorks

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(general, '/general/<string:method>')
api.add_resource(image, '/image')
api.add_resource(ChangePassword, '/changepwd')

api.add_resource(User, '/user', '/user/<int:userid>',  endpoint='userep')
api.add_resource(GetUserList, '/userlist/<int:page>')
api.add_resource(GetuserDetailList, '/userdetaillist/<int:page>')
api.add_resource(Tag, '/tag', '/tag/<int:tagid>')
api.add_resource(TagList, '/taglist/<int:limit>')
api.add_resource(UserTags, '/<int:userid>/usertags', endpoint='userTags')
api.add_resource(UserWorks, '/<int:userid>/userworks/<int:page>', endpoint='userWorks')
api.add_resource(SearchTagsByName, '/search/taglist/<string:keyword>')
api.add_resource(UserPublishedProjects, '/<int:userid>/userpublishedprojects/<int:page>', \
	endpoint='publishedProjects')
api.add_resource(UserWonProjects, '/<int:userid>/userwonprojects/<int:page>', endpoint='wonProjects')

api.add_resource(AuthorityPrivate, '/private', '/private/<int:id>')
api.add_resource(AuthorityPrivateList, '/privatelist')
api.add_resource(AuthorityCompany, '/company', '/company/<int:id>')
api.add_resource(AuthorityCompanyList, '/companylist')

api.add_resource(Bid, '/bid', '/<int:userid>/bid/<int:taskid>')
api.add_resource(BidList, '/<int:taskid>/bidlist')

api.add_resource(Project, '/project', '/project/<int:projectid>', endpoint='projectep')

api.add_resource(Task, '/task', '/task/<int:taskid>', endpoint='taskep')
api.add_resource(TaskNotes, '/<int:taskid>/tasknotes')
api.add_resource(TaskVersions, '/<int:taskid>/taskversions')

api.add_resource(GetVRTaskList, '/vrtasklist')
api.add_resource(GetMoiveTaskList, '/movietasklist')
api.add_resource(GetTaskDetail, '/taskdetail/<int:taskid>', endpoint='taskdetailep')
api.add_resource(GetTaskList, '/<int:kindid>/tasklist/<int:page>', endpoint='tasklistep')
api.add_resource(GetTaskListByProjectID, '/<int:projectid>/GetTaskListByProjectID', \
    endpoint='getTasksByProjectID')
api.add_resource(GetTaskListByBidderID, '/<int:projectid>/<int:bidderid>/GetTaskListByBidderID', \
    endpoint='GetTaskListByBidderID')

api.add_resource(Version, '/version', '/version/<int:versionid>')

api.add_resource(Note, '/note', '/note/<int:noteid>')
api.add_resource(NoteMessage, '/notemessage')
api.add_resource(NoteMessageList, '/<int:noteid>/notemessagelist')

api.add_resource(Work, '/work', '/work/<int:workid>')

api.add_resource(Kind, '/kind', '/kind/<int:kindid>')
api.add_resource(KindList, '/kindlist')
api.add_resource(SearchKindsByName, '/search/kindlist/<string:keyword>')

api.add_resource(Profile, '/profile')
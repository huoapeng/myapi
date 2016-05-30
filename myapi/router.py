
from flask import Blueprint
from flask.ext.restful import Api
from myapi.resources.general import general
from myapi.resources.user import User, ChangePassword
from myapi.resources.tag import Tag, UserTags
from myapi.resources.project import Project, UserPublishedProjects
from myapi.resources.task import Task, GetTaskListByProjectID, GetTaskList
from myapi.resources.version import Version, TaskVersions
from myapi.resources.note import Note, TaskNotes
from myapi.resources.kind import Kind, KindList, SearchKindsByName
from myapi.resources.message import NoteMessage, NoteMessageList
from myapi.resources.profile import Profile

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(general, '/', '/general/<string:method>')
api.add_resource(ChangePassword, '/changepwd')

api.add_resource(User, '/user', '/user/<int:userid>',  endpoint='userep')
api.add_resource(Tag, '/tag', '/tag/<int:tagid>')
api.add_resource(UserTags, '/<int:userid>/usertags')
api.add_resource(UserPublishedProjects, '/<int:userid>/userpublishedprojects')

api.add_resource(Project, '/project', '/project/<int:projectid>')

api.add_resource(Task, '/task', '/task/<int:taskid>')
api.add_resource(TaskNotes, '/<int:taskid>/tasknotes')
api.add_resource(TaskVersions, '/<int:taskid>/taskversions')

api.add_resource(GetTaskList, '/tasklist/<int:page>')
api.add_resource(GetTaskListByProjectID, '/<int:projectid>/GetTaskListByProjectID', endpoint='getTasksByProjectID')

api.add_resource(Version, '/version', '/version/<int:versionid>')

api.add_resource(Note, '/note', '/note/<int:noteid>')
api.add_resource(NoteMessage, '/notemessage')
api.add_resource(NoteMessageList, '/<int:noteid>/notemessagelist')

api.add_resource(Kind, '/kind', '/kind/<int:kindid>')
api.add_resource(KindList, '/kindlist')
api.add_resource(SearchKindsByName, '/search/kindlist/<string:kindname>')

# api.add_resource(UserWonTasks, '/<int:userid>/userwontasks')

api.add_resource(Profile, '/profile')
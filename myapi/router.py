from flask.ext.restful import Api
from myapi.resources.general import general
from myapi.resources.user import User
from myapi.resources.project import Project
from myapi.resources.task import Task
from myapi.resources.version import Version
from myapi.resources.note import Note

api = Api()
api.add_resource(general, '/', '/general/<string:method>')
api.add_resource(User, '/user', '/user/<int:userid>', endpoint='userep')
api.add_resource(Project, '/project', '/project/<int:projectid>')
api.add_resource(Task, '/task', '/task/<int:taskid>')
api.add_resource(Version, '/version', '/version/<int:versionid>')
api.add_resource(Note, '/note', '/note/<int:noteid>')

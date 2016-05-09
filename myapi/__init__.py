from flask import Flask
from flask.ext import restful
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_name)
    app.config.from_pyfile('config.py')
    #app.config.from_envvar('APP_CONFIG_FILE')

    db.init_app(app)

    from myapi.resources.general import general
    from myapi.resources.user import User
    from myapi.resources.project import Project
    from myapi.resources.task import Task
    from myapi.resources.version import Version
    from myapi.resources.note import Note

    api = restful.Api(app)
    api.add_resource(general, '/general/<string:method>')
    api.add_resource(User, '/user', '/user/<int:userid>')
    api.add_resource(Project, '/project', '/project/<int:projectid>')
    api.add_resource(Task, '/task', '/task/<int:taskid>')
    api.add_resource(Version, '/version', '/version/<int:versionid>')
    api.add_resource(Note, '/note', '/note/<int:noteid>')

    return app
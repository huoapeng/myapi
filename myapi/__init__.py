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

	from myapi.resources.user import User
	from myapi.resources.general import general
	api = restful.Api(app)
	api.add_resource(User, '/user', '/user/<int:userid>')
	api.add_resource(general, '/general/<string:method>')

	return app


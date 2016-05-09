from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

def create_app(config_name):
    app.config.from_object(config_name)
    #app.config.from_envvar('APP_CONFIG_FILE')

    db.init_app(app)
    
    from router import api
    api.init_app(app)

    return app
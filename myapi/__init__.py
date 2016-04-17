from flask import Flask
from flask.ext import restful
from flask.ext.sqlalchemy import SQLAlchemy
from myapi.resources.user import User

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.dev')
app.config.from_pyfile('config.py')
#app.config.from_envvar('APP_CONFIG_FILE')
api = restful.Api(app)


api.add_resource(User, '/user', '/user/<int:userid>')

# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     db_session.remove()

# @app.errorhandler(404)
# def not_found(error):
#     return render_template('404.html'), 404

# @app.before_request
# def load_current_user():
#     g.user = User.query.filter_by(openid=session['openid']).first() \
#         if 'openid' in session else None

# from myapi.database import db_session

# @app.teardown_request
# def remove_db_session(exception):
#     db_session.remove()


# @app.context_processor
# def current_year():
#     return {'current_year': datetime.utcnow().year}

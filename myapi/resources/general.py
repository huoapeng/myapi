from flask import Blueprint
from myweb.database import init_db, db_session
from myweb.model.user import User

mod = Blueprint('general', __name__)

@mod.route('/', methods=['GET', 'POST'])
def index():
	return 'this is index'

@mod.route('/init_db')
def initdb():
	init_db()
	return 'init database'


@mod.route('/adduser')
def adduser():
	u = User('admin','admin@test.com')
	db_session.add(u)
	db_session.commit()
	return 'success add user' 


@mod.route('/searchalluser')
def searchalluser():
	return User.query.all()[0].name


@mod.route('/searchuser')
def searchuser():
	return User.query.filter(User.name == 'admin').first()

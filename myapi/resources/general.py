from flask.ext.restful import Resource
from myapi import db

class general(Resource):
	def get(self):
		# if method == 1:
		# 	db.create_all()
		# elif method == 'drop_all':
		# 	db.drop_all()
		# else:
		# pass
		db.create_all()
		return {'result':'true'}

	def get(self):
		pass

	def post(self):
		pass
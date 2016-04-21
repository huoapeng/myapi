from flask.ext.restful import Resource
from myapi import db

class general(Resource):
	def get(self, method):
		if method == 'create_all':
			db.create_all()
		elif method == 'drop_all':
			db.drop_all()
		else:
			pass
		return {'result':'true'}

	def put(self):
		pass

	def post(self):
		pass
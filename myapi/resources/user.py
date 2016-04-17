from flask.ext.restful import Resource
from myapi.model.user import User

class User(Resource):
    def get(self, userid= None):
    	
    	return {'result':'true'}
    	# else
     #    	return {'result': User.query.all()}

    def get(self):
    	    u = User('admin','admin@test.com')
			db_session.add(u)
			db_session.commit()

    def post(self):
    	pass



# class HelloWorld(restful.Resource):
#     def get(self):
#         return {'hello': 'world'}

# class todo(restful.Resource):
# 	def get(self, todo_id):
# 		return {'hello' : todo_id }

# api.add_resource(HelloWorld, '/')
# api.add_resource(todo, '/user/<string:todo_id>')
from flask.ext.restful import Resource
from flask.ext.restful import fields, marshal_with, reqparse
from myapi import db
from myapi.model.project import ProjectModel

post_parser = reqparse.RequestParser()
post_parser.add_argument(
    'email', dest='email',
    type=str, location='form',
    required=True, help='The user\'s email'
)
post_parser.add_argument(
    'password', dest='password',
    type=str, 
    required=True, help='The user\'s password'
)
post_parser.add_argument(
    'type', dest='type',
    type=int, 
    required=True,
    choices=range(2)
)
# post_parser.add_argument(
#     'user_priority', dest='user_priority',
#     type=int, location='form',
#     default=1, choices=range(5), help='The user\'s priority',
# )

project_fields = {
    'id': fields.Integer,
    'username': fields.String(default='Anonymous User'),
    'email': fields.String,
    'ema111il': fields.String,
    'password': fields.String
    # 'user_priority': fields.Integer,
    # 'custom_greeting': fields.FormattedString('Hey there {username}!'),
    # 'date_created': fields.DateTime,
    # 'date_updated': fields.DateTime,
    # 'links': fields.Nested({
    #     'friends': fields.Url('/Users/{id}/Friends'),
    #     'posts': fields.Url('Users/{id}/Posts'),
    # }),
}


class Project(Resource):
    @marshal_with(project_fields)
    def get(self, projectid):
        return ProjectModel.query.get(projectid)
        #return ProjectModel.query.filter_by(id=projectid).first()
        #todos=Todo.query.order_by(Todo.pub_date.desc()).all()

    def post(self):
        args = post_parser.parse_args()
        if not valid_email(args.email,):
            return {'status':'False','message':'pls check email'}
        else:
            if args.type == 0:
                user = ProjectModel.query.filter_by(email=args.email).first()
                if user is None:
                    u = ProjectModel(args.email, args.password)
                    db.session.add(u)
                    db.session.commit()
                    return {'status':'True','message':'regist successfully'}
                else:
                    return {'status':'False','message':'account is already exist'}
            else:
                user = ProjectModel.query.filter_by(email=args.email).filter_by(password=args.password).first()
                if user is None:
                    return {'status':'False','message':'account is not exist'}
                else:
                    return {'status':'True','message':'account is logon'}

    def put(self):
        #     for todo in Todo.query.all():
        #         todo.done = ('done.%d' % todo.id) in request.form
        #     flash('Updated status')
        #     db.session.commit()
        pass

    def delete(self):
        pass


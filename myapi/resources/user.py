from flask.ext.restful import Resource
from flask.ext.restful import fields, marshal_with, reqparse
# from flask import request, jsonify
from myapi import db
from myapi.model.user import UserModel
from myapi.common.util import valid_email, md5

post_parser = reqparse.RequestParser()
post_parser.add_argument(
    'email', type=str, location='json', required=True
)
post_parser.add_argument(
    'password', type=str, location='json', required=True
)
post_parser.add_argument(
    'type', type=int, location='json', required=True,
    choices=range(2)#, default=1
)

user_fields = {
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


class User(Resource):
    @marshal_with(user_fields)
    def get(self, userid):
        return UserModel.query.get(userid)
        #return UserModel.query.filter_by(id=userid).first()
        #todos=Todo.query.order_by(Todo.pub_date.desc()).all()

    def post(self):
        args = post_parser.parse_args()
        # json_data = request.get_json(force=True)
        # un = json_data['email']
        if not valid_email(args.email,):
            return {'status':'False','message':'pls check email'}
        else:
            if args.type == 0:
                user = UserModel.query.filter_by(email=args.email).first()
                if user is None:
                    u = UserModel(args.email, md5(args.password))
                    db.session.add(u)
                    db.session.commit()
                    return {'status':'True','message':'regist successfully'}
                else:
                    return {'status':'False','message':'account is already exist'}
            else:
                user = UserModel.query.filter_by(email=args.email).filter_by(password=md5(args.password)).first()
                if user is None:
                    return {'status':'False','message':'account is not exist'}
                else:
                    return {'status':'True','message':'account is logon'}

    def put(self):
        pass

    def delete(self):
        pass

#     for todo in Todo.query.all():
#         todo.done = ('done.%d' % todo.id) in request.form
#     flash('Updated status')
#     db.session.commit()
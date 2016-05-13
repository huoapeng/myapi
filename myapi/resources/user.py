#coding=utf-8
from flask.ext.restful import Resource, fields, marshal_with, reqparse, abort
from myapi import db
from myapi.model.user import UserModel
from myapi.model.enum import user_actions
from myapi.common.util import valid_email, md5

post_parser = reqparse.RequestParser()
post_parser.add_argument('email', type=str, location='json', required=True)
post_parser.add_argument('password', type=str, location='json', required=True)
post_parser.add_argument('type', type=int, location='json', required=True, choices=range(2), default=1)

user_fields = {
    'id': fields.Integer,
    'nickname': fields.FormattedString('nihao 111111, {nickname}!'),
    'email': fields.String,
    # 'password': fields.String(default='mima is security'),
    'phone': fields.String,
    'area': fields.String,
    'description':fields.String,
    'status':fields.Integer,
    'regist_date': fields.DateTime
}

# 发布的项目s
# 参与的任务s
# 标签s
# 发布的versions
# 发布的意见s
class User(Resource):
    @marshal_with(user_fields)
    def get(self, userid):
        # abort(404, message="Todo {} doesn't exist".format('userid'))
        return UserModel.query.get(userid)
        #return UserModel.query.filter_by(id=userid).first()
        #todos=Todo.query.order_by(Todo.pub_date.desc()).all()
    
    # @marshal_with(user_fields)
    def post(self):
        # from flask import request, jsonify
        # print request.get_json(force=True)
        # json_data = request.get_json(force=True)
        # un = json_data['email']
        # return {'hello world':un}
        args = post_parser.parse_args()
        if not valid_email(args.email,):
            return {'status':'False','message':'pls check email'}
        
        if args.type == user_actions.regist:
            user = UserModel.query.filter_by(email=args.email).first()
            if user is None:
                u = UserModel(args.email, md5(args.password))
                db.session.add(u)
                db.session.commit()
                # return {'status':'True','message':'regist successfully'}
                # return marshal_with(UserModel.query.filter_by(email=args.email).first(), user_fields),200
                return marshal_with(u, user_fields), 200
            else:
                return {'status':'False','message':'account is already exist'}
        else:
            user = UserModel.query.filter_by(email=args.email).filter_by(password=md5(args.password)).first()
            if user is None:
                return {'status':'False','message':'account is not exist'}
            else:
                return marshal_with(user, user_fields), 200

    def put(self):
        args = post_parser.parse_args()
        if not valid_email(args.email,):
            return {'status':'False','message':'pls check email'}
        
        user = UserModel.query.filter_by(email=args.email).first()
        if user is None:
            return {'status':'False','message':'account is not exist'}
        else:
            user.password = args.password
            db.session.commit()
            # return {'status':'True','message':'regist successfully'}
            # return marshal_with(UserModel.query.filter_by(email=args.email).first(), user_fields),200
            return marshal_with(u, user_fields), 200

    def delete(self):
        args = post_parser.parse_args()
        if not valid_email(args.email,):
            return {'status':'False','message':'pls check email'}
        
        user = UserModel.query.filter_by(email=args.email).first()
        if user is None:
            return {'status':'False','message':'account is not exist'}
        else:
            user.status = user_status.delete
            db.session.commit()
            # return {'status':'True','message':'regist successfully'}
            # return marshal_with(UserModel.query.filter_by(email=args.email).first(), user_fields),200
            return marshal_with(u, user_fields), 200

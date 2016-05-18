import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask.ext.restful import Resource, fields, marshal_with, marshal, reqparse
from myapi import db
from myapi.model.user import UserModel
from myapi.model.enum import user_status
from myapi.common.util import valid_email, md5, itemStatus
from myapi.common.decorator import jsonp

post_parser = reqparse.RequestParser()
post_parser.add_argument('email', type=valid_email, location='json', required=True)
post_parser.add_argument('nickname', type=str, location='json')
post_parser.add_argument('password', type=str, location='json')
post_parser.add_argument('phone', type=str, location='json')
post_parser.add_argument('area', type=str, location='json')
post_parser.add_argument('description', type=str, location='json')
# post_parser.add_argument('type', type=int, location='json', required=True, choices=range(2), default=1)

user_fields = {
    'id': fields.Integer,
    # 'nickname': fields.FormattedString('nihao , {nickname}!'),
    'nickname': fields.String,
    'email': fields.String,
    'phone': fields.String,
    'area': fields.String,
    'description': fields.String,
    'status': itemStatus(attribute='status'),
    'regist_date': fields.DateTime,
}

class User(Resource):
    @jsonp
    @marshal_with(user_fields)
    def get(self, userid):
        user = UserModel.query.get(userid)
        return user if user else UserModel('','')
        # return jsonify({
        #     'id':u.id, 
        #     'url':url_for('.userep', _external=True, userid=u.id),
        #     })
        # todos=Todo.query.order_by(Todo.pub_date.desc()).all()
    
    @jsonp
    @marshal_with(user_fields)
    def post(self):
        # from flask import request, jsonify
        # print request.get_json(force=True)
        # json_data = request.get_json(force=True)
        # un = json_data['email']
        # return {'hello world':un}
        args = post_parser.parse_args()

        user = UserModel.query.filter_by(email=args.email).first()
        if user is None:
            u = UserModel(args.email, md5(args.password))
            db.session.add(u)
            db.session.commit()

        return UserModel.query.filter_by(email=args.email).filter_by(password=md5(args.password)).one()

    @jsonp
    @marshal_with(user_fields)
    def put(self):
        args = post_parser.parse_args()
        user = UserModel.query.filter_by(email=args.email).one()
        if user :
            user.nickname = args.nickname
            user.password = args.password
            user.phone = args.phone
            user.area = args.area
            user.description = args.description
            db.session.commit()
            return user
        else:
            return UserModel('','')

    @jsonp
    @marshal_with(user_fields)
    def delete(self):
        args = post_parser.parse_args()
        user = UserModel.query.filter_by(email=args.email).one()
        if user:
            user.status = user_status.delete
            db.session.commit()
            return user
        else:
            return UserModel('','')
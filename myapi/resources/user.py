import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import jsonify
from flask.ext.restful import Resource, fields, marshal_with, marshal, reqparse
from myapi import db, app
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

class ChangePassword(Resource):
    @marshal_with(user_fields)
    def post(self):
        args = post_parser.parse_args()
        user = UserModel.query.filter_by(email=args.email).one()
        if user :
            user.password = md5(args.password)
            db.session.commit()
            return user
        else:
            return UserModel('','')
        
class UserSummary(Resource):
    def get(self, userid):
        # user = UserModel.query.get(userid)
        # return user if user else UserModel('','')
        return jsonify({
            # 'detail':url_for(), 
            'url':url_for('.userep', _external=True, userid=userid),
            })

class GetUserList(Resource):
    def get(self, page):
        tag_str_list = []
        user_obj_list = []
        
        users = UserModel.query.paginate(page, app.config['POSTS_PER_PAGE'], False).items
        for user in users:

            for tag in project.tags:
                tag_str_list.append(tag.name)

            u = UserMarketView(user.id,
                    user.image,
                    user.nickname,
                    user.authorisedStatus,
                    user.authorisedId,
                    user.area,
                    0,#wonTaskCount,
                    0,#profileIntegrityPercent,
                    user.phone,
                    user.email,
                    tag_str_list
                )
            user_obj_list.append(u)

        return jsonify(result=[e.serialize() for e in user_obj_list])
 
        
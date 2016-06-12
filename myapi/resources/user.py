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
from myapi.view.user import UserMarketView

post_parser = reqparse.RequestParser()
post_parser.add_argument('email', type=valid_email, location='json', required=True)
post_parser.add_argument('nickname', type=str, location='json')
post_parser.add_argument('password', type=str, location='json')
post_parser.add_argument('phone', type=str, location='json')
post_parser.add_argument('location', type=str, location='json')
post_parser.add_argument('description', type=str, location='json')

class User(Resource):
    @jsonp
    def get(self, userid):
        user = UserModel.query.get(userid)
        user = user if user else UserModel('','')
        return jsonify(user.serialize())
    
    @jsonp
    def post(self):
        args = post_parser.parse_args()

        user = UserModel.query.filter_by(email=args.email).first()
        if user is None:
            u = UserModel(args.email, md5(args.password))
            db.session.add(u)
            db.session.commit()

        user = UserModel.query.filter_by(email=args.email).filter_by(password=md5(args.password)).one()
        return jsonify(user.serialize())

    @jsonp
    def put(self):
        args = post_parser.parse_args()
        user = UserModel.query.filter_by(email=args.email).one()
        if user :
            user.nickname = args.nickname
            user.phone = args.phone
            user.location = args.location
            user.description = args.description
            db.session.commit()
        else:
            user = UserModel('','')
        return jsonify(user.serialize())

    @jsonp
    def delete(self):
        args = post_parser.parse_args()
        user = UserModel.query.filter_by(email=args.email).one()
        if user:
            user.status = user_status.delete
            db.session.commit()
        else:
            user = UserModel('','')
        return jsonify(user.serialize())

class ChangePassword(Resource):
    def post(self):
        args = post_parser.parse_args()
        user = UserModel.query.filter_by(email=args.email).one()
        if user :
            user.password = md5(args.password)
            db.session.commit()
        else:
            user = UserModel('','')
        return jsonify(user.serialize())

get_parser = reqparse.RequestParser()
get_parser.add_argument('keyword', type=str, location='args')
get_parser.add_argument('tag', type=str, location='args')
get_parser.add_argument('authorised_status', type=int, location='args', choices=range(5), default=0)

class GetUserList(Resource):
    def get(self, page):
        args = get_parser.parse_args()
        user_obj_list = []

        users = UserModel.query

        if args.keyword:
            users = users.filter(UserModel.nickname.contains(args.keyword))
        if args.authorised_status:
            users = users.filter(UserModel.authorisedStatus == args.authorised_status)

        # q = session.query(myClass)
        # for attr, value in web_dict.items():
        # q = q.filter(getattr(myClass, attr).like("%%%s%%" % value))

        users = users.paginate(page, app.config['POSTS_PER_PAGE'], False)
        for user in users.items:
            tag_str_list = []
            for tag in user.tags:
                tag_str_list.append(tag.name)
                
            if args.tag:
                if args.tag not in ','.join(tag_str_list):
                    continue

            u = UserMarketView(user.id,
                    user.image,
                    user.nickname,
                    user.authorisedStatus,
                    user.location,
                    0,#wonTaskCount,
                    0,#profileIntegrityPercent,
                    user.phone,
                    user.email,
                    tag_str_list
                )
            user_obj_list.append(u)

        return jsonify(total = users.total,
            pages = users.pages,
            page = users.page,
            per_page = users.per_page,
            has_next = users.has_next,
            has_prev = users.has_prev,
            next_num = users.next_num,
            prev_num = users.prev_num,
            data=[e.serialize() for e in user_obj_list])
 
        
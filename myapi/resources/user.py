#coding=utf-8
import datetime
from flask import jsonify
from flask.ext.restful import Resource, reqparse
from myapi import db, app
from myapi.model.user import UserModel
from myapi.model.smtp import EmailModel
from myapi.model.tag import UserTagModel
from myapi.model.enum import user_status
from myapi.common.util import valid_email, md5

class User(Resource):
    def get(self, userid):
        user = UserModel.query.get(userid)
        if user:
            return jsonify(user.serialize())
        else:
            return jsonify(result='can`t find user by userid')

    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('email', type=valid_email, location='json', required=True)
        post_parser.add_argument('nickname', type=str, location='json')
        post_parser.add_argument('password', type=str, location='json')
        post_parser.add_argument('phone', type=str, location='json')
        post_parser.add_argument('location', type=str, location='json')
        post_parser.add_argument('description', type=str, location='json')
        args = post_parser.parse_args()

        user = UserModel.query.filter_by(email=args.email).first()
        if user:
            if user.status == user_status.disable:
                return jsonify(result=False, message='此账号已被冻结！')
        else:
            u = UserModel(args.email, md5(args.password), \
                args.nickname, args.phone, args.location, args.description)
            db.session.add(u)
            db.session.commit()
        
        user = UserModel.query.filter_by(email=args.email).filter_by(password=md5(args.password)).first()
        if user:
            return jsonify(result=True, data=user.serialize())
        else:
            return jsonify(result=False, message='用户名或密码错误！')

    def put(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('email', type=valid_email, location='json', required=True)
        args = post_parser.parse_args()
        user = UserModel.query.filter_by(email=args.email).one()
        if user:
            user.nickname = args.nickname
            user.phone = args.phone
            user.location = args.location
            user.description = args.description
            db.session.commit()    
            return jsonify(user.serialize())
        else:
            return jsonify(result='can`t find user by email')

class ChangeUserStatus(Resource):
    def put(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('id', type=int, location='json', required=True)
        post_parser.add_argument('userStatus', type=int, location='json', required=True)
        args = post_parser.parse_args()
        user = UserModel.query.get(args.id)
        if user:
            user.status = args.userStatus
            db.session.commit()
            return jsonify(user.serialize())
        else:
            return jsonify(result='can`t find user by id')

class ChangePassword(Resource):
    def put(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('email', type=valid_email, location='json', required=True)
        post_parser.add_argument('params', type=str, location='json')
        post_parser.add_argument('orignalPassword', type=str, location='json')
        args = post_parser.parse_args()
        if not args.orignalPassword:
            user = UserModel.query.filter_by(email=args.email).one()
            if user:
                e = EmailModel.query.filter_by(toUser=args.email).filter_by(params=args.params).first()
                if not e or e.expires < datetime.datetime.now():
                    return jsonify(result='pls try again')
            else:
                return jsonify(result='can`t find user by email')
        else:
            user = UserModel.query.filter_by(email=args.email).filter_by(password=md5(args.orignalPassword)).one()

        if user:
            user.password = md5(args.password)
            db.session.commit()
            return jsonify(user.serialize())

class ChangeUserDefaultImg(Resource):
    def put(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('userid', type=int, location='json', required=True)
        post_parser.add_argument('imageid', type=int, location='json', required=True)
        args = post_parser.parse_args()
        user = UserModel.query.get(args.userid)
        if user:
            user.defaultImage = '{}.jpg'.format(args.imageid)
            db.session.commit()
            return jsonify(user.serialize())
        else:
            return jsonify(result='can`t find user by id')

class GetUserList(Resource):
    def get(self, page):
        get_parser = reqparse.RequestParser()
        get_parser.add_argument('all', type=int, location='args', choices=range(2), default=0)
        get_parser.add_argument('keyword', type=str, location='args')
        get_parser.add_argument('tag', type=str, location='args')
        get_parser.add_argument('status', type=int, location='args', default=0)
        args = get_parser.parse_args()

        users = UserModel.query
        if not args.all:
            users = users.filter_by(status = user_status.normal)

        if args.tag:
            users = users.filter(UserModel.tags.any(UserTagModel.name == args.tag))

        if args.keyword:
            users = users.filter(UserModel.nickname.contains(args.keyword))

        if args.status:
            users = users.filter(UserModel.authenticationType & args.status == args.status)

        users = users.paginate(page, app.config['POSTS_PER_PAGE'], False)
        return jsonify(total = users.total,
            pages = users.pages,
            page = users.page,
            per_page = users.per_page,
            has_next = users.has_next,
            has_prev = users.has_prev,
            next_num = users.next_num,
            prev_num = users.prev_num,
            data=[e.serialize() for e in users.items])
        
from flask import jsonify
from flask.ext.restful import Resource, fields, marshal_with, marshal, reqparse
from myapi import db, app
from myapi.model.tag import UserTagModel, WorkTagModel
from myapi.model.user import UserModel
from myapi.model.work import WorkModel
from sqlalchemy import func

parser = reqparse.RequestParser()
parser.add_argument('id', type=int, location='json')
parser.add_argument('name', type=str, location='json')
parser.add_argument('user_id', type=int, location='json')
parser.add_argument('work_id', type=int, location='json')

tag_fields = {
    'id': fields.Integer,
    'name': fields.String
}

class UserTag(Resource):
    @marshal_with(tag_fields)
    def get(self, tagid):
        return UserTagModel.query.get(tagid)

    @marshal_with(tag_fields)
    def post(self):
        args = parser.parse_args()
        tag = UserTagModel(args.name)
        db.session.add(tag)

        if args.user_id:
            user = UserModel.query.get(args.user_id)
            user.tags.append(tag)
        db.session.commit()
        return tag

    def put(self):
        pass

    def delete(self):
        args = parser.parse_args()
        tag = UserTagModel.query.get(args.id)
        db.session.delete(tag)
        db.session.commit()
        return {'result':'true'}

class UserTags(Resource):
    @marshal_with(tag_fields)
    def get(self, userid):
        user = UserModel.query.get(userid)
        return user.tags

class UserTagList(Resource):
    def get(self, page):
        # tags = db.session.query(UserTagModel.name, func.count(UserTagModel.name)).\
        #     group_by(UserTagModel.name).order_by(func.count(UserTagModel.name).desc()).limit(limit)
        # return jsonify(data=[e for e in tags])
        tags = UserTagModel.query.paginate(page, app.config['POSTS_PER_PAGE'], False)
        return jsonify(total = tags.total,
            pages = tags.pages,
            page = tags.page,
            per_page = tags.per_page,
            has_next = tags.has_next,
            has_prev = tags.has_prev,
            next_num = tags.next_num,
            prev_num = tags.prev_num,
            data=[e.serialize() for e in tags.items])
 

class SearchUserTagsByName(Resource):
    @marshal_with(tag_fields)
    def get(self, keyword):
        return UserTagModel.query.filter(UserTagModel.name.contains(keyword)).all()

class WorkTag(Resource):
    @marshal_with(tag_fields)
    def get(self, tagid):
        return WorkTagModel.query.get(tagid)

    @marshal_with(tag_fields)
    def post(self):
        args = parser.parse_args()
        tag = WorkTagModel(args.name)
        db.session.add(tag)

        # work = WorkModel.query.get(args.work_id)
        # work.tags.append(tag)
        db.session.commit()
        return tag

    def put(self):
        pass

    def delete(self):
        args = parser.parse_args()
        tag = WorkTagModel.query.get(args.id)
        db.session.delete(tag)
        db.session.commit()
        return {'result':'true'}

class WorkTags(Resource):
    @marshal_with(tag_fields)
    def get(self, workid):
        work = WorkModel.query.get(workid)
        return work.tags

class WorkTagList(Resource):
    def get(self, limit):
        tags = db.session.query(WorkTagModel.name, func.count(WorkTagModel.name)).\
            group_by(WorkTagModel.name).order_by(func.count(WorkTagModel.name).desc()).limit(limit)
        return jsonify(data=[e for e in tags])

class SearchWorkTagsByName(Resource):
    @marshal_with(tag_fields)
    def get(self, keyword):
        return WorkTagModel.query.filter(WorkTagModel.name.contains(keyword)).all()
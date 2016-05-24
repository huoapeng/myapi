import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask.ext.restful import Resource, fields, marshal_with, marshal, reqparse
from myapi import db
from myapi.model.tag import TagModel
from myapi.model.user import UserModel

parser = reqparse.RequestParser()
parser.add_argument('id', type=int, location='json')
parser.add_argument('name', type=str, location='json', required=True)
parser.add_argument('user_id', type=int, location='json', required=True)

tag_fields = {
    'id': fields.Integer,
    'name': fields.String
}

class Tag(Resource):
    @marshal_with(tag_fields)
    def get(self, tagid):
        return TagModel.query.get(tagid)

    @marshal_with(tag_fields)
    def post(self):
        args = parser.parse_args()
        tag = TagModel(args.name)
        db.session.add(tag)

        user = UserModel.query.get(args.user_id)
        user.tags.append(tag)
        db.session.commit()
        return tag

    def put(self):
        pass

    def delete(self):
        args = parser.parse_args()
        tag = TagModel.query.get(args.id)
        db.session.delete(tag)
        db.session.commit()
        return {'result':'true'}

class UserTags(Resource):
    @marshal_with(tag_fields)
    def get(self, userid):
        user = UserModel.query.get(userid)
        return user.tags



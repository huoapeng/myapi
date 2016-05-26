import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask.ext.restful import Resource, fields, marshal_with, marshal, reqparse
from myapi import db
from myapi.model.task import TaskModel
from myapi.model.user import UserModel

parser = reqparse.RequestParser()
parser.add_argument('task_id', type=int, location='json', required=True)
parser.add_argument('user_id', type=int, location='json', required=True)
parser.add_argument('bidding_price', type=int, location='json')
parser.add_argument('bidding_description', type=str, location='json')

    db.Column('user_id', db.Integer, db.ForeignKey('user_model.id'), primary_key=True),
    db.Column('task_id', db.Integer, db.ForeignKey('task_model.id'), primary_key=True),
    db.Column('bidding_price', db.Integer),
    db.Column('bidding_description', db.String(4096)),
    db.Column('bidding_datatime', db.DateTime)

bid_fields = {
    'id': fields.Integer,
    'bidding_price': fields.Integer,
    'bidding_description': fields.String,
    'bidding_datatime': fields.DateTime
}

class Bid(Resource):
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
        pass

class UserTags(Resource):
    @marshal_with(tag_fields)
    def get(self, userid):
        user = UserModel.query.get(userid)
        return user.tags



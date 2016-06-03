import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import jsonify
from flask.ext.restful import Resource, fields, marshal_with, marshal, reqparse
from myapi import db, app
from myapi.model.bid import BidModel
from myapi.model.task import TaskModel
from myapi.model.user import UserModel

parser = reqparse.RequestParser()
parser.add_argument('task_id', type=int, location='json', required=True)
parser.add_argument('user_id', type=int, location='json', required=True)
parser.add_argument('bidding_price', type=str, location='json')
parser.add_argument('bidding_description', type=str, location='json')
# parser.add_argument('bidding_status', type=int, location='json', choices=range(3), default=1)

class Bid(Resource):
    def get(self, userid, taskid):
        e = BidModel.query.filter_by(user_id=userid).filter_by(task_id=taskid).first_or_404()
        return jsonify(data=e.serialize())

    def post(self):
        args = parser.parse_args()
        bid = BidModel(args.bidding_price, args.bidding_description)

        user = UserModel.query.get(args.user_id)
        bid.user = user

        task = TaskModel.query.get(args.task_id)
        task.bidders.append(bid)

        db.session.commit()
        return jsonify(bid.serialize())

    def put(self):
        args = parser.parse_args()
        bid = BidModel.query.filter_by(user_id=userid).filter_by(task_id=taskid).first_or_404()
        bid.status = bid_status.selectBidder

        db.session.commit()

class BidList(Resource):
    def get(self, taskid):
        return jsonify(data=[e.serialize() for e in TaskModel.query.get(taskid).bidders])



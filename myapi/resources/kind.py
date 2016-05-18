#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import jsonify
from flask.ext.restful import Resource, fields, marshal_with, reqparse, marshal
from myapi import db
from myapi.model.kind import KindModel
from myapi.model.enum import kind_status
from myapi.common.decorator import jsonp
from myapi.common.util import itemStatus

parser = reqparse.RequestParser()
parser.add_argument(
    'id', dest='id', type=int, location='json',
)
parser.add_argument(
    'name', dest='name', type=str, location='json'#, required=True
)
parser.add_argument(
    'parent_id', dest='parent_id', type=int, location='json'
)

post_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'parent_id': fields.Integer,
    'status': itemStatus(attribute='status')
}

class Kind(Resource):
    @jsonp
    @marshal_with(post_fields)
    def get(self, kindid):
        return KindModel.query.get(kindid)

    @jsonp
    @marshal_with(post_fields)
    def post(self):
        args = parser.parse_args()
        t = KindModel(args.name, args.parent_id)
        db.session.add(t)
        db.session.commit()
        return t

    @jsonp
    @marshal_with(post_fields)
    def put(self):
        args = parser.parse_args()
        t = KindModel.query.get(args.id)
        t.name = args.name
        t.parent_id = args.parent_id
        db.session.commit()
        return t

    @jsonp
    @marshal_with(post_fields)
    def delete(self):
        args = parser.parse_args()
        t = KindModel.query.get(args.id)
        t.status = kind_status.delete
        db.session.commit()
        return t

class KindList(Resource):
    @jsonp
    @marshal_with(post_fields)
    def get(self):
        return KindModel.query.filter_by(status = kind_status.normal).all()

    @jsonp
    @marshal_with(post_fields)
    def post(self):
        args = parser.parse_args()
        t = KindModel(args.name)
        db.session.add(t)
        db.session.commit()

        t = KindModel.query.filter_by(name=args.name).filter_by(parent_id=None).first()
        t.parent_id = t.id
        db.session.commit()
        return t


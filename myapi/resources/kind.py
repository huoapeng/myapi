import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask.ext.restful import Resource, fields, marshal_with, marshal, reqparse
from myapi import db
from myapi.model.kind import KindModel
from myapi.model.enum import kind_status
from myapi.common.util import itemStatus
from myapi.common.decorator import jsonp

parser = reqparse.RequestParser()
parser.add_argument('id', dest='id', type=int, location='json')
parser.add_argument('name', dest='name', type=str, location='json')#, required=True)
parser.add_argument('parent_id', dest='parent_id', type=int, location='json')

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
        kind = KindModel(args.name, args.parent_id)
        db.session.add(kind)
        db.session.commit()
        return kind

    @jsonp
    @marshal_with(post_fields)
    def put(self):
        args = parser.parse_args()
        kind = KindModel.query.get(args.id)
        kind.name = args.name
        kind.parent_id = args.parent_id
        db.session.commit()
        return kind

    @jsonp
    @marshal_with(post_fields)
    def delete(self):
        args = parser.parse_args()
        kind = KindModel.query.get(args.id)
        kind.status = kind_status.delete
        db.session.commit()
        return kind

class KindList(Resource):
    @jsonp
    @marshal_with(post_fields)
    def get(self):
        return KindModel.query.filter_by(status = kind_status.normal).all()

    @jsonp
    @marshal_with(post_fields)
    def post(self):
        args = parser.parse_args()
        kind = KindModel(args.name)
        db.session.add(kind)
        db.session.commit()

        kind = KindModel.query.filter_by(name=args.name).filter_by(parent_id=None).first()
        kind.parent_id = kind.id
        db.session.commit()
        return kind

class SearchKindsByName(Resource):
    @marshal_with(post_fields)
    def get(self, kindname):
        return KindModel.query.filter_by(status = kind_status.normal)\
            .filter(KindModel.name.contains(kindname)).all()



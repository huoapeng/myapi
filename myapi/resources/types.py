from flask.ext.restful import Resource, fields, marshal_with, reqparse
from myapi import db
from myapi.model.types import TypeModel
from myapi.model.enum import type_status

parser = reqparse.RequestParser()
parser.add_argument(
    'id', dest='id', type=int, location='json',
)
parser.add_argument(
    'name', dest='name', type=str, location='json', required=True
)
parser.add_argument(
    'parent_id', dest='parent_id', type=int, location='json'
)

post_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'parent_id': fields.Integer,
}

class Project(Resource):
    @marshal_with(post_fields)
    def get(self, projectid):
        return TypeModel.query.get(projectid)

    @marshal_with(post_fields)
    def post(self):
        args = parser.parse_args()

        p = TypeModel(args.name, args.description, args.type_id, args.owner_id)
        db.session.add(p)
        db.session.commit()
        return p

    def put(self):
        args = parser.parse_args()
        # user = UserModel.query.filter_by(name=args.email).first()
        p = TypeModel.query.get(args.id)
        p.name = args.name
        p.description = args.description
        p.status = args.status
        p.type_id = args.type_id
        p.owner_id = args.owner_id
        db.session.commit()
        return p

    def delete(self):
        args = parser.parse_args()
        p = TypeModel.query.get(args.id)
        p.status = project_status.delete
        db.session.commit()
        return p


from flask.ext.restful import Resource
from flask.ext.restful import fields, marshal_with, reqparse
from myapi import db
from myapi.model.project import ProjectModel
from myapi.model.enum import project_status

post_parser = reqparse.RequestParser()
post_parser.add_argument(
    'id', dest='id',
    type=int, location='json',
)
post_parser.add_argument(
    'name', dest='name',
    type=str, location='json',
    required=True
)
post_parser.add_argument(
    'description', dest='description',
    type=str, location='json',
)
post_parser.add_argument(
    'status', dest='status',
    type=int, location='json',
)
post_parser.add_argument(
    'type_id', dest='type_id',
    type=int, location='json',
    required=True
)
post_parser.add_argument(
    'owner_id', dest='owner_id',
    type=int, location='json',
    required=True
)

project_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'status': fields.Integer,
    'type_id': fields.Integer,
    'owner_id':fields.Integer
}

class Project(Resource):
    @marshal_with(project_fields)
    def get(self, projectid):
        return ProjectModel.query.get(projectid)

    @marshal_with(project_fields)
    def post(self):
        args = post_parser.parse_args()

        p = ProjectModel(args.name, args.description, args.type_id, args.owner_id)
        db.session.add(p)
        db.session.commit()
        return p

    def put(self):
        args = post_parser.parse_args()
        # user = UserModel.query.filter_by(name=args.email).first()
        print args.id
        p = ProjectModel.query.get(args.id)
        p.name = args.name
        p.description = args.description
        p.status = args.status
        p.type_id = args.type_id
        p.owner_id = args.owner_id
        db.session.commit()
        pass

    def delete(self):
        args = post_parser.parse_args()
        p = ProjectModel.query.get(args.id)
        p.status = project_status.delete
        db.session.commit()
        pass


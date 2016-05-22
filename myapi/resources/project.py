import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask.ext.restful import Resource, fields, marshal_with, marshal, reqparse
from myapi import db
from myapi.model.project import ProjectModel
from myapi.model.user import UserModel
from myapi.model.kind import KindModel
from myapi.model.enum import project_status
from myapi.common.util import itemStatus

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, location='json', required=True)
parser.add_argument('description', type=str, location='json')
parser.add_argument('owner_id', type=int, location='json', required=True)
parser.add_argument('kind_id', type=int, location='json', required=True)

project_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'publish_date': fields.DateTime,
    'status': itemStatus(attribute='status'),
    'owner_id': fields.Integer
}

class Project(Resource):
    @marshal_with(project_fields)
    def get(self, projectid):
        return ProjectModel.query.get(projectid)

    @marshal_with(project_fields)
    def post(self):
        args = parser.parse_args()

        kind = KindModel.query.get(args.kind_id)
        project = ProjectModel(args.name, args.description)
        project.kinds.append(kind)
        db.session.add(project)

        user = UserModel.query.get(args.owner_id)
        user.published_projects.append(project)
        db.session.commit()
        return project

    @marshal_with(project_fields)
    def put(self):
        args = parser.parse_args()
        kind = KindModel.query.get(args.kind_id)
        project = ProjectModel.query.get(args.id)
        project.name = args.name
        project.description = args.description
        project.kind = kind
        db.session.commit()
        return project

    @marshal_with(project_fields)
    def delete(self):
        args = parser.parse_args()
        project = ProjectModel.query.get(args.id)
        project.status = project_status.delete
        db.session.commit()
        return project


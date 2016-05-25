import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask.ext.restful import Resource, fields, marshal_with, marshal, reqparse
from myapi import db
from myapi.model.version import VersionModel
from myapi.model.task import TaskModel
from myapi.model.enum import version_status
from myapi.common.util import itemStatus

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, location='json', required=True)
parser.add_argument('description', type=str, location='json')
parser.add_argument('task_id', type=int, location='json', required=True)

version_fields = {
    'id': fields.Integer,
    'file': fields.String,
    'image': fields.String,
    'title': fields.String,
    'description': fields.String,
    'publish_date': fields.DateTime,
    'status':  itemStatus(attribute='status'),
}

class Version(Resource):
    @marshal_with(version_fields)
    def get(self, versionid):
        return VersionModel.query.get(versionid)

    @marshal_with(version_fields)
    def post(self):
        args = parser.parse_args()
        version = VersionModel(args.title, args.description)
        db.session.add(version)

        task = TaskModel.query.get(args.task_id)
        task.versions.append(version)
        db.session.commit()
        return version

    def put(self):
        
        pass

    @marshal_with(version_fields)
    def delete(self):
        args = parser.parse_args()
        version = VersionModel.query.get(args.id)
        version.status = version_status.delete
        db.session.commit()
        return version

class TaskVersions(Resource):
    @marshal_with(version_fields)
    def get(self, taskid):
        task = TaskModel.query.get(taskid)
        return task.versions
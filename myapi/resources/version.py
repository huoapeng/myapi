import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import jsonify
from flask.ext.restful import Resource, fields, reqparse
from myapi import db
from myapi.model.version import VersionModel
from myapi.model.user import UserModel
from myapi.model.task import TaskModel
from myapi.model.enum import version_status

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, location='json', required=True)
parser.add_argument('description', type=str, location='json')
parser.add_argument('image', type=str, location='json')
parser.add_argument('task_id', type=int, location='json', required=True)
parser.add_argument('user_id', type=int, location='json', required=True)

class Version(Resource):
    def get(self, versionid):
        version = VersionModel.query.get(versionid)
        return jsonify(version.serialize())

    def post(self):
        args = parser.parse_args()
        version = VersionModel(args.title, args.description, args.image)
        db.session.add(version)

        task = TaskModel.query.get(args.task_id)
        task.versions.append(version)

        user = UserModel.query.get(args.user_id)
        user.versions.append(version)
        db.session.commit()
        return jsonify(version.serialize())

    def put(self):      
        pass

    def delete(self):
        args = parser.parse_args()
        version = VersionModel.query.get(args.id)
        version.status = version_status.delete
        db.session.commit()
        return jsonify(version.serialize())

class TaskVersions(Resource):
    def get(self, taskid):
        task = TaskModel.query.get(taskid)
        if task:
            return jsonify(data=[e.serialize() for e in task.versions.order_by(VersionModel.publish_date.desc())])
        else:
            return jsonify(data=[])


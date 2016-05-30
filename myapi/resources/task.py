import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import jsonify
from flask.ext.restful import Resource, fields, marshal_with, marshal, reqparse
from myapi import db
from myapi.model.task import TaskModel
from myapi.model.user import UserModel
from myapi.model.kind import KindModel
from myapi.model.project import ProjectModel
from myapi.model.enum import task_status
from myapi.common.util import itemStatus
from myapi.view.task import TaskOfMovieMarketView

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, location='json', required=True)
parser.add_argument('timespan', type=str, location='json')
parser.add_argument('requirements', type=str, location='json')
parser.add_argument('bonus', type=str, location='json')
parser.add_argument('description', type=str, location='json')
parser.add_argument('bidder_qualification_requirement', type=str, location='json')
parser.add_argument('bidder_area_requirement', type=str, location='json')
parser.add_argument('project_id', type=int, location='json', required=True)
parser.add_argument('kind_id', type=int, location='json', required=True)

task_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'timespan': fields.Integer,
    'requirements': fields.String,
    'bonus': fields.Integer,
    'description': fields.String,
    'publishDate': fields.DateTime,
    'bidder_qualification_requirement': fields.String,
    'bidder_area_requirement': fields.String,
    'status': itemStatus(attribute='status'),
    'project_id': fields.Integer,
    'winner_id': fields.Integer
}

class Task(Resource):
    @marshal_with(task_fields)
    def get(self, taskid):
        return TaskModel.query.get(taskid)

    @marshal_with(task_fields)
    def post(self):
        args = parser.parse_args()

        kind = KindModel.query.get(args.kind_id)
        task = TaskModel(args.name, 
            args.timespan,
            args.requirements,
            args.bonus,
            args.description,
            args.bidder_qualification_requirement,
            args.bidder_area_requirement)
        task.kinds.append(kind)

        # user = UserModel.query.get(1)
        # task.bidders.append(user)
        db.session.add(task)

        project = ProjectModel.query.get(args.project_id)
        project.tasks.append(task)
        db.session.commit()
        return task

    @marshal_with(task_fields)
    def put(self):
        pass

    @marshal_with(task_fields)
    def delete(self):
        args = parser.parse_args()
        task = TaskModel.query.get(args.id)
        task.status = task_status.delete
        db.session.commit()
        return task

class GetTaskListByProjectID(Resource):
    @marshal_with(task_fields)
    def get(self, projectid):
        project = ProjectModel.query.get(projectid)
        return project.tasks

class GetTaskList(Resource):
    def get(self):
        kind_str_list = []
        task_obj_list = []
        
        tasks = TaskModel.query.all()
        for task in tasks:
            project = task.project
            owner = project.owner
            for kind in project.kinds:
                kind_str_list.append(kind.name)

            t = TaskOfMovieMarketView(task.id,
                    task.name,
                    project.id,
                    project.name,
                    owner.id,
                    owner.nickname,
                    task.publishDate,
                    task.bonus,
                    kind_str_list
                )
            task_obj_list.append(t)

        return jsonify(result=[e.serialize() for e in task_obj_list])

class UserWonTasks(Resource):
    @marshal_with(task_fields)
    def get(self, userid):
        user = UserModel.query.get(userid)
        return user.won_tasks

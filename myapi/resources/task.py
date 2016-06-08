import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import jsonify
from flask.ext.restful import Resource, fields, marshal_with, marshal, reqparse
from myapi import db, app
from myapi.model.task import TaskModel
from myapi.model.user import UserModel
from myapi.model.kind import KindModel
from myapi.model.project import ProjectModel
from myapi.model.enum import task_status
from myapi.common.util import itemStatus
from myapi.view.task import TaskOfMovieMarketView

post_parser = reqparse.RequestParser()
post_parser.add_argument('id', type=int, location='json')
post_parser.add_argument('name', type=str, location='json')
post_parser.add_argument('timespan', type=str, location='json')
post_parser.add_argument('requirements', type=str, location='json')
post_parser.add_argument('bonus', type=str, location='json')
post_parser.add_argument('description', type=str, location='json')
post_parser.add_argument('bidder_qualification_requirement', type=str, location='json')
post_parser.add_argument('bidder_area_requirement', type=str, location='json')
post_parser.add_argument('project_id', type=int, location='json')
post_parser.add_argument('kind_id', type=int, location='json')

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
    'status': fields.Integer,
    'project_id': fields.Integer,
    'winner_id': fields.Integer
}

class Task(Resource):
    @marshal_with(task_fields)
    def get(self, taskid):
        return TaskModel.query.get(taskid)

    @marshal_with(task_fields)
    def post(self):
        args = post_parser.parse_args()

        kind = KindModel.query.get(args.kind_id)
        task = TaskModel(args.name, 
            args.timespan,
            args.requirements,
            args.bonus,
            args.description,
            args.bidder_qualification_requirement,
            args.bidder_area_requirement)
        task.kinds.append(kind)

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
        args = post_parser.parse_args()
        task = TaskModel.query.get(args.id)
        task.status = task_status.finish
        db.session.commit()
        return task

parser = reqparse.RequestParser()
parser.add_argument('status', type=int, location='args', choices=range(3), default=0)

class GetTaskListByProjectID(Resource):
    @marshal_with(task_fields)
    def get(self, projectid):
        args = parser.parse_args()
        tasks = ProjectModel.query.get(projectid).tasks
        if args.status:
            tasks = tasks.filter(TaskModel.status == args.status)
        return tasks.all()

class GetTaskListByBidderID(Resource):
    @marshal_with(task_fields)
    def get(self, projectid, bidderid):
        args = parser.parse_args()
        tasks = ProjectModel.query.get(projectid).tasks
        if args.status:
            tasks = tasks.filter(TaskModel.status == args.status)

        result = []
        for task in tasks:
            for bidder in task.bidders:
                if bidderid == bidder.user_id:
                    result.append(task)
        return result

get_parser = reqparse.RequestParser()
get_parser.add_argument('keyword', type=str, location='args')
get_parser.add_argument('kind', type=str, location='args')
get_parser.add_argument('status', type=int, location='args', choices=range(3), default=0)
get_parser.add_argument('orderby', type=int, location='args', choices=range(2), default=0)
get_parser.add_argument('desc', type=int, location='args', choices=range(2), default=0)

class GetTaskList(Resource):
    def get(self, page):
        args = get_parser.parse_args()
        task_obj_list = []
        
        tasks = TaskModel.query
        
        if args.keyword:
            tasks = tasks.filter(TaskModel.name.contains(args.keyword))
        if args.status:
            tasks = tasks.filter(TaskModel.status == args.status)
            
        if args.orderby == 0:
            if args.desc:
                tasks = tasks.order_by(TaskModel.publishDate.desc())
            else:
                tasks = tasks.order_by(TaskModel.publishDate.asc())
        if args.orderby == 1:
            if args.desc:
                tasks = tasks.order_by(TaskModel.bonus.desc())
            else:
                tasks = tasks.order_by(TaskModel.bonus.asc())

        tasks = tasks.paginate(page, app.config['POSTS_PER_PAGE'], False)
        for task in tasks.items:
            project = task.project
            owner = project.owner
            kind_str_list = []
            for kind in project.kinds:
                kind_str_list.append(kind.name)

            if args.kind:
                if args.kind not in ','.join(kind_str_list):
                    continue

            t = TaskOfMovieMarketView(task.id,
                    task.name,
                    project.id,
                    project.name,
                    owner.id,
                    owner.nickname,
                    task.publishDate,
                    task.bonus,
                    owner.area,
                    task.bidder_area_requirement,
                    task.bidder_qualification_requirement,
                    kind_str_list
                )
            task_obj_list.append(t)

        return jsonify(total = tasks.total,
            pages = tasks.pages,
            page = tasks.page,
            per_page = tasks.per_page,
            has_next = tasks.has_next,
            has_prev = tasks.has_prev,
            next_num = tasks.next_num,
            prev_num = tasks.prev_num,
            result=[e.serialize() for e in task_obj_list])


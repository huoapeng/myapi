from flask import jsonify
from flask.ext.restful import Resource, fields, marshal_with, marshal, reqparse
from myapi import db, app
from myapi.model.project import ProjectModel
from myapi.model.user import UserModel
from myapi.model.kind import KindModel
from myapi.model.enum import project_status
from myapi.model.bid import BidModel
from myapi.common.util import itemStatus
from myapi.view.project import UserBidProjectsView

class Project(Resource):
    def get(self, projectid):
        project = ProjectModel.query.get(projectid)
        return project.serialize()

    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('name', type=str, location='json', required=True)
        post_parser.add_argument('description', type=str, location='json')
        post_parser.add_argument('userid', type=int, location='json', required=True)
        args = post_parser.parse_args()

        project = ProjectModel(args.name, args.description)
        db.session.add(project)

        user = UserModel.query.get(args.userid)
        user.publishedProjects.append(project)
        db.session.commit()
        return project.serialize()

    def put(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('id', type=int, location='json', required=True)
        post_parser.add_argument('projectStatus', type=int, location='json', required=True)
        args = post_parser.parse_args()
        project = ProjectModel.query.get(args.id)
        project.status = args.projectStatus
        db.session.commit()
        return project.serialize()

# from sqlalchemy import func
class UserPublishedProjects(Resource):
    def get(self, page):
        get_parser = reqparse.RequestParser()
        get_parser.add_argument('userid', type=int, location='args', required=True)
        get_parser.add_argument('projectStatus', type=int, location='args')
        args = get_parser.parse_args()

        projects = UserModel.query.get(args.userid).publishedProjects
        if args.projectStatus:
            projects = projects.filter_by(status = args.projectStatus)
        projects = projects.paginate(page, app.config['POSTS_PER_PAGE'], False)

        # project_obj_list = []
        # for project in projects.items:
        #     if func.count(project.tasks) == 0:
        #         continue
        #     project_obj_list.append(project)

        return jsonify(total = projects.total,
            pages = projects.pages,
            page = projects.page,
            per_page = projects.per_page,
            has_next = projects.has_next,
            has_prev = projects.has_prev,
            next_num = projects.next_num,
            prev_num = projects.prev_num,
            data=[e.serialize() for e in projects.items])

class UserParticipateProjects(Resource):
    def get(self, page):
        get_parser = reqparse.RequestParser()
        get_parser.add_argument('userid', type=int, location='args', required=True)
        args = get_parser.parse_args()

        bidTasks = UserModel.query.get(args.userid).bidTasks\
            .paginate(page, app.config['POSTS_PER_PAGE'], False)

        project_obj_dict = {}
        for bid in bidTasks.items:
            project = bid.task.project

            if project.id not in project_obj_dict: 
                v = UserBidProjectsView(userid, project.id, project.name)
                project_obj_dict[project.id] = v

        return jsonify(total = bidTasks.total,
            pages = bidTasks.pages,
            page = bidTasks.page,
            per_page = bidTasks.per_page,
            has_next = bidTasks.has_next,
            has_prev = bidTasks.has_prev,
            next_num = bidTasks.next_num,
            prev_num = bidTasks.prev_num,
            data=[e.serialize() for e in project_obj_dict.values()])




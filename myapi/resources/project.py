from flask import jsonify
from flask.ext.restful import Resource, fields, marshal_with, marshal, reqparse
from myapi import db, app
from myapi.model.project import ProjectModel
from myapi.model.user import UserModel
from myapi.model.kind import KindModel
from myapi.model.enum import project_status
from myapi.model.bid import BidModel
from myapi.common.util import itemStatus
from myapi.view.project import UserPublishedProjectsView, UserBidProjectsView


post_parser = reqparse.RequestParser()
post_parser.add_argument('name', type=str, location='json', required=True)
post_parser.add_argument('description', type=str, location='json')
post_parser.add_argument('owner_id', type=int, location='json', required=True)

class Project(Resource):
    def get(self, projectid):
        project = ProjectModel.query.get(projectid)
        return project.serialize()

    def post(self):
        args = post_parser.parse_args()

        project = ProjectModel(args.name, args.description)
        db.session.add(project)

        user = UserModel.query.get(args.owner_id)
        user.publishedProjects.append(project)
        db.session.commit()
        return project.serialize()

    def delete(self):
        args = post_parser.parse_args()
        project = ProjectModel.query.get(args.id)
        project.status = project_status.delete
        db.session.commit()
        return project.serialize()

class UserPublishedProjects(Resource):
    def get(self, userid, page):
        projects = UserModel.query.get(userid).published_projects\
            .paginate(page, app.config['POSTS_PER_PAGE'], False)

        project_obj_list = []
        for project in projects.items:
            v = UserPublishedProjectsView(project.id, project.name)
            project_obj_list.append(v)

        return jsonify(total = projects.total,
            pages = projects.pages,
            page = projects.page,
            per_page = projects.per_page,
            has_next = projects.has_next,
            has_prev = projects.has_prev,
            next_num = projects.next_num,
            prev_num = projects.prev_num,
            data=[e.serialize() for e in project_obj_list])

class UserWonProjects(Resource):
    def get(self, userid, page):
        bidTasks = UserModel.query.get(userid).bidTasks\
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




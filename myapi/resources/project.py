#coding=utf-8
from flask import jsonify
from flask.ext.restful import Resource, reqparse
from myapi import db, app
from myapi.model.category import CategoryModel
from myapi.model.project import ProjectModel
from myapi.model.user import UserModel

class Project(Resource):
    def get(self, taskid):
        return ProjectModel.query.get(taskid).serialize()

    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('name', type=str, location='json', required=True)
        post_parser.add_argument('timespan', type=str, location='json')
        post_parser.add_argument('requirements', type=str, location='json')
        post_parser.add_argument('bonus', type=int, location='json')
        post_parser.add_argument('description', type=str, location='json')
        post_parser.add_argument('bidderQualifiRequire', type=str, location='json')
        post_parser.add_argument('bidderLocationRequire', type=str, location='json')
        post_parser.add_argument('receipt', type=bool , location='json')
        post_parser.add_argument('receiptDescription', type=str, location='json')
        post_parser.add_argument('userid', type=int, location='json', required=True)
        post_parser.add_argument('cids', type=str, location='json', required=True)
        args = post_parser.parse_args()

        project = ProjectModel(args.name, 
            args.timespan,
            args.requirements,
            args.bonus,
            args.description,
            args.bidderQualifiRequire,
            args.bidderLocationRequire,
            args.receipt,
            args.receiptDescription)

        for id in args.cids.split(','):
            category = CategoryModel.query.get(id)
            project.categorys.append(category)

        db.session.add(project)

        user = UserModel.query.get(args.userid)
        user.projects.append(project)
        db.session.commit()
        return project.serialize()

    def put(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('id', type=int, location='json', required=True)
        post_parser.add_argument('status', type=int, location='json', required=True)
        args = post_parser.parse_args()
        project = ProjectModel.query.get(args.id)
        project.status = args.status
        db.session.commit()
        return project

class GetProjectDetail(Resource):
    def get(self, projectid):
        project = ProjectModel.query.get(projectid)
        owner = project.owner
        category_str_list = []
        for category in project.categorys:
            category_str_list.append(category.name)

        taskview = TaskDetailView(project, owner.id, owner.nickname, owner.location, category_str_list)
        return jsonify(taskview.serialize())

class UserPublishedProjects(Resource):
    def get(self, page):
        parser = reqparse.RequestParser()
        parser.add_argument('userid', type=int, location='args', required=True)
        parser.add_argument('status', type=int, location='args', default=0)
        args = parser.parse_args()
        projects = UserModel.query.get(args.userid).publishedProjects

        if args.status:
            projects = projects.filter_by(status = args.status)

        projects = projects.paginate(page, app.config['POSTS_PER_PAGE'], False)
        return jsonify(total = projects.total,
            pages = projects.pages,
            page = projects.page,
            per_page = projects.per_page,
            has_next = projects.has_next,
            has_prev = projects.has_prev,
            next_num = projects.next_num,
            prev_num = projects.prev_num,
            result=[e.serialize() for e in projects.items])

class UserParticipateProjects(Resource):
    def get(self, page):
        parser = reqparse.RequestParser()
        parser.add_argument('userid', type=int, location='args', required=True)
        parser.add_argument('status', type=int, location='args', default=0)
        args = parser.parse_args()
        bids = UserModel.query.get(args.userid).bidProjects

        if args.status:
            bids = bids.project.filter_by(status = args.status)
        
        bids = bids.paginate(page, app.config['POSTS_PER_PAGE'], False)
        return jsonify(total = bids.total,
            pages = bids.pages,
            page = bids.page,
            per_page = bids.per_page,
            has_next = bids.has_next,
            has_prev = bids.has_prev,
            next_num = bids.next_num,
            prev_num = bids.prev_num,
            result=[e.serialize() for e in bids.items])

from sqlalchemy import or_
class GetProjectList(Resource):
    def get(self, page):
        get_parser = reqparse.RequestParser()
        get_parser.add_argument('cid', type=int, location='args', default=0)
        get_parser.add_argument('keyword', type=str, location='args')
        get_parser.add_argument('status', type=int, location='args', choices=range(6), default=0)
        get_parser.add_argument('orderby', type=int, location='args', choices=range(3), default=0)
        get_parser.add_argument('desc', type=int, location='args', choices=range(3), default=0)
        args = get_parser.parse_args()
        project_obj_list = []
        
        projects = ProjectModel.query

        if args.cid:
            projects = projects.filter( \
                or_( \
                    ProjectModel.kinds.any(CategoryModel.id == args.cid), \
                    ProjectModel.kinds.any(CategoryModel.parent_id == args.cid), \
                    ProjectModel.kinds.any(CategoryModel.parent.parent_id == args.cid)
                    ) \
                )

        if args.keyword:
            projects = projects.filter(ProjectModel.name.contains(args.keyword))

        if args.status:
            projects = projects.filter(ProjectModel.status == args.status)
            
        if args.orderby == 1:
            if args.desc == 1:
                projects = projects.order_by(ProjectModel.publishDate.desc())
            else:
                projects = projects.order_by(ProjectModel.publishDate.asc())
        if args.orderby == 2:
            if args.desc == 1:
                projects = projects.order_by(ProjectModel.bonus.desc())
            else:
                projects = projects.order_by(ProjectModel.bonus.asc())

        projects = projects.paginate(page, app.config['POSTS_PER_PAGE'], False)
        for project in projects.items:
            owner = project.owner
            category_str_list = []
            for category in project.categorys:
                category_str_list.append(category.name)

            taskview = TaskDetailView(project, owner.id, owner.nickname, owner.location, category_str_list)
            project_obj_list.append(taskview)

        return jsonify(total = projects.total,
            pages = projects.pages,
            page = projects.page,
            per_page = projects.per_page,
            has_next = projects.has_next,
            has_prev = projects.has_prev,
            next_num = projects.next_num,
            prev_num = projects.prev_num,
            result=[e.serialize() for e in project_obj_list])


from flask.ext.restful import Resource, fields, marshal_with, marshal, reqparse
from myapi import db
from myapi.model.category import CategoryModel
from myapi.model.enum import category_status
from myapi.common.util import itemStatus

parser = reqparse.RequestParser()
parser.add_argument('id', dest='id', type=int, location='json')
parser.add_argument('name', dest='name', type=str, location='json')#, required=True)
parser.add_argument('parentid', dest='parentid', type=int, location='json')
parser.add_argument('isTop', type=int, location='json', default=0)

post_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'parentid': fields.Integer,
    'status': itemStatus(attribute='status')
}

class Category(Resource):
    @marshal_with(post_fields)
    def get(self, cid):
        return CategoryModel.query.get(cid)

    @marshal_with(post_fields)
    def post(self):
        args = parser.parse_args()
        category = CategoryModel(args.name)

        if args.parentid:
            parent = CategoryModel.query.get(args.parentid)
            category.parent = parent

        db.session.add(category)
        db.session.commit()

        if args.isTop:
            category = CategoryModel.query.filter_by(name=args.name).filter_by(parent_id=None).first()
            category.parent_id = category.id
            db.session.commit()
        return category

    @marshal_with(post_fields)
    def put(self):
        args = parser.parse_args()
        category = CategoryModel.query.get(args.id)
        category.name = args.name
        category.parent_id = args.parentid
        db.session.commit()
        return category

    @marshal_with(post_fields)
    def delete(self):
        args = parser.parse_args()
        category = CategoryModel.query.get(args.id)
        category.status = category_status.delete
        db.session.commit()
        return category

class CategoryList(Resource):
    @marshal_with(post_fields)
    def get(self):
        return CategoryModel.query.filter_by(status = category_status.normal).all()

class SearchCategorysByName(Resource):
    @marshal_with(post_fields)
    def get(self, keyword):
        return CategoryModel.query.filter_by(status = category_status.normal)\
            .filter(CategoryModel.name.contains(keyword)).all()



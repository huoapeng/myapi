import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import jsonify
from flask.ext.restful import Resource, reqparse
from myapi import db, app
from myapi.model.recommend import RecommendTypeModel, RecommendItemModel

post_parser = reqparse.RequestParser()
post_parser.add_argument('typeid', type=int, location='json')
post_parser.add_argument('itemid', type=int, location='json')
post_parser.add_argument('targetitemid', type=int, location='json')
post_parser.add_argument('name', type=str, location='json')
post_parser.add_argument('title', type=str, location='json')
post_parser.add_argument('description', type=str, location='json')
post_parser.add_argument('image', type=str, location='json')
post_parser.add_argument('url', type=str, location='json')
post_parser.add_argument('orderid', type=int, location='json')

class RecommendType(Resource):
    def get(self, id):
        kind = RecommendTypeModel.query.get(id)
        return jsonify(data=kind.serialize()) if kind else jsonify(data='')
    
    def post(self):
        args = post_parser.parse_args()

        kind = RecommendTypeModel(args.name)
        db.session.add(kind)
        db.session.commit()

        return jsonify(data=kind.serialize())

    def put(self):
        args = post_parser.parse_args()
        kind = RecommendTypeModel.query.get(args.typeid)
        kind.name = args.name
        db.session.commit()
        return jsonify(data=kind.serialize())

    def delete(self):
        args = post_parser.parse_args()
        kind = RecommendTypeModel.query.get(args.typeid)
        for item in kind.items:
            db.session.delete(item)
        db.session.delete(kind)
        db.session.commit()
        return jsonify(result='true')

class RecommendTypeList(Resource):
    def get(self):
        kinds = RecommendTypeModel.query.all()
        return jsonify(data=[kind.serialize() for kind in kinds])

class RecommendItem(Resource):
    def get(self, id):
        item = RecommendItemModel.query.get(id)
        return jsonify(data=item.serialize()) if item else jsonify(data='')
    
    def post(self):
        args = post_parser.parse_args()
        item = RecommendItemModel(args.title, args.description, args.image, args.url, args.orderid)
        db.session.add(item)

        kind = RecommendTypeModel.query.get(args.typeid)
        kind.items.append(item)
        db.session.commit()
        return jsonify(data=item.serialize())

    def put(self):
        args = post_parser.parse_args()
        item = RecommendItemModel.query.get(args.itemid)
        item.title = args.title
        item.description = args.description
        item.image = args.image
        item.url = args.url
        item.orderid = args.orderid

        # target = RecommendItemModel.query.get(args.targetitemid)
        # item.orderid = target.orderid
        # target.orderid = orderid

        db.session.commit()
        return jsonify(result='true')

    def delete(self):
        args = post_parser.parse_args()
        item = RecommendItemModel.query.get(args.itemid)

        db.session.delete(item)
        db.session.commit()
        return jsonify(result='true')

class RecommendItemList(Resource):
    def get(self, typeid):
        kind = RecommendTypeModel.query.get(typeid)
        if kind and kind.items:
            return jsonify(data=[item.serialize() for item in kind.items])
        else:
            return jsonify(data='')


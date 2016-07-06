#coding=utf-8
# import os
# from flask import request, url_for, jsonify, send_from_directory
from flask.ext.restful import Resource#, reqparse
# # from werkzeug.datastructures import FileStorage
from myapi import db#, app
# from myapi.model.enum import file_type
# from myapi.model.user import UserModel
from myapi.model.kind import KindModel
from myapi.model.recommend import RecommendTypeModel
# from myapi.common.image import resize, allowedFile, getServerPath

class general(Resource):
    def get(self, method = None):
        if method == 'create_all':
            db.create_all()
            
            kind1 = KindModel.query.filter_by(name = '影视大厅').first()
            if not kind1:
                kind1 = KindModel('影视大厅')
                db.session.add(kind1)
                db.session.commit()

            kind11 = RecommendTypeModel.query.filter_by(name = '影视大厅').first()
            if not kind11:
                kind11 = RecommendTypeModel('影视大厅')
                db.session.add(kind11)
                db.session.commit()

            kind2 = KindModel.query.filter_by(name = 'VR/AR大厅').first()
            if not kind2:
                kind2 = KindModel('VR/AR大厅')
                db.session.add(kind2)
                db.session.commit()

            kind22 = RecommendTypeModel.query.filter_by(name = 'VR/AR大厅').first()
            if not kind22:
                kind22 = RecommendTypeModel('VR/AR大厅')
                db.session.add(kind22)
                db.session.commit()

        elif method == 'drop_all':
            db.drop_all()
        else:
            return 'hello world!'
        return {'result':'true'}


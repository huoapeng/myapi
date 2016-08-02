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
        elif method == 'drop_all':
            db.drop_all()
        else:
            return 'hello world!'
        return {'result':'true'}


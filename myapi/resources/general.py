#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
from flask import request, url_for, jsonify, send_from_directory
from flask.ext.restful import Resource, reqparse
# from werkzeug.datastructures import FileStorage
from myapi import db, app
from myapi.model.enum import file_type
from myapi.model.user import UserModel
from myapi.model.kind import KindModel
from myapi.common.image import resize, allowedFile, getServerPath

class image(Resource):
    def get(self, userid, imagetype, filename):
        if filename:
            fpath = os.path.join(app.config['ROOT_PATH'], app.config['UPLOAD_FOLDER'], path[imagetype](userid))
            return send_from_directory(fpath, filename)
        else:
            return ''

    def post(self):
        file = request.files['file']
        get_parser = reqparse.RequestParser()
        get_parser.add_argument('type', type=int, location='args', choices=range(1, 8), required=True)
        get_parser.add_argument('userid', type=int, location='args', required=True)
        get_parser.add_argument('thumbnail', type=int, location='args', default=0)
        args = get_parser.parse_args()

        if file and allowedFile(file.filename, args.type):
            sf = getServerPath(file.filename, args.type, args.userid)

            if args.type == file_type.profile:
                user = UserModel.query.get(args.userid)
                user.image = os.path.basename(sf)
                db.session.commit()
                file = resize(file, 100, 80)

            if args.thumbnail:
                thumbnailfile = resize(file, 223, 99999)
                tsf = getServerPath(file.filename, file_type.workThumbnail, args.userid)
                thumbnailfile.save(tsf)

            file.save(sf)
            return jsonify(image=os.path.basename(sf), thumbnail=os.path.basename(tsf))
        return 'pls check file suffix'

class CompressFile(Resource):
    def post(self):
        file = request.files['file']
        get_parser = reqparse.RequestParser()
        get_parser.add_argument('type', type=int, location='args', choices=range(51, 52), required=True)
        get_parser.add_argument('userid', type=int, location='args', required=True)
        args = get_parser.parse_args()

        if file and allowedFile(file.filename, args.type):
            sf = getServerPath(file.filename, args.type, args.userid)
            file.save(sf)
            return jsonify(data=os.path.basename(sf))
        return 'pls check file suffix'

class general(Resource):
    def get(self, method = None):
        if method == 'create_all':
            db.create_all()
            
            kind1 = KindModel.query.filter_by(name = '影视大厅').first()
            if not kind1:
                kind1 = KindModel('影视大厅')
                db.session.add(kind1)
                db.session.commit()

            kind2 = KindModel.query.filter_by(name = 'VR/AR大厅').first()
            if not kind2:
                kind2 = KindModel('VR/AR大厅')
                db.session.add(kind2)
                db.session.commit()
        elif method == 'drop_all':
            db.drop_all()
        else:
            return 'hello world!'
        return {'result':'true'}


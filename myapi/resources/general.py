#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os, random
from flask import request, url_for, jsonify, send_from_directory
from flask.ext.restful import Resource, reqparse
from werkzeug.utils import secure_filename
# from werkzeug.datastructures import FileStorage
from myapi import db, app
from myapi.model.enum import file_type
from myapi.model.user import UserModel
from myapi.model.kind import KindModel
from myapi.common.image import resize, filePath, allowedFile

class image(Resource):
    def get(self, userid, imagetype, filename):
        if filename:
            fpath = os.path.join(app.config['ROOT_PATH'], app.config['UPLOAD_FOLDER'], path[imagetype](userid))
            return send_from_directory(fpath, filename)
        else:
            return ''

    def post(self):
        file = request.files['file']
        if file and allowedFile(file.filename):
            get_parser = reqparse.RequestParser()
            get_parser.add_argument('type', type=int, location='args', choices=range(8), default=0, required=True)
            get_parser.add_argument('userid', type=int, location='args', required=True)

            args = get_parser.parse_args()
            serverPath = os.path.join(app.config['ROOT_PATH'], \
                app.config['UPLOAD_FOLDER'], filePath[args.type](args.userid))
            if not os.path.exists(serverPath):
                # os.mkdir(serverPath)
                os.makedirs(serverPath)

            fname = secure_filename(file.filename)
            sf = os.path.join(serverPath, fname)
            
            while os.path.exists(sf):
                randomString = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcbaABCDEFGHIJKLMNOPQRSTUVWXYZ',10))
                sf = sf.replace(fname, randomString + fname)

            if args.type == file_type.profile:
                user = UserModel.query.get(args.userid)
                user.image = os.path.basename(sf)
                db.session.commit()

                file = resize(file, 100, 80)

            file.save(sf)
            return jsonify(data=os.path.basename(sf))
        return 'pls check file suffix'

class CompressFile(Resource):
    def post(self):
        file = request.files['file']
        if file and allowedFile(file.filename, 123):
            get_parser = reqparse.RequestParser()
            get_parser.add_argument('type', type=int, location='args', choices=range(8,9), required=True)
            get_parser.add_argument('userid', type=int, location='args', required=True)

            args = get_parser.parse_args()
            serverPath = os.path.join(app.config['ROOT_PATH'], \
                app.config['UPLOAD_FOLDER'], filePath[args.type](args.userid))
            if not os.path.exists(serverPath):
                os.makedirs(serverPath)

            fname = secure_filename(file.filename)
            sf = os.path.join(serverPath, fname)
            
            while os.path.exists(sf):
                randomString = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcbaABCDEFGHIJKLMNOPQRSTUVWXYZ',10))
                sf = sf.replace(fname, randomString + fname)

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


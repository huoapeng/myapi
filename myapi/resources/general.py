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
from myapi.model.enum import image_type
from myapi.model.user import UserModel
from myapi.model.kind import KindModel
from myapi.common.image import resize, imagePath, allowedFile

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
            filepath = os.path.join(app.config['ROOT_PATH'], \
                app.config['UPLOAD_FOLDER'], imagePath[args.type](args.userid))
            if not os.path.exists(filepath):
                # os.mkdir(filepath)
                os.makedirs(filepath)

            fname = secure_filename(file.filename)
            sf = os.path.join(filepath, fname)
            
            while os.path.exists(sf):
                randomString = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcbaABCDEFGHIJKLMNOPQRSTUVWXYZ',10))
                sf = sf.replace(fname, randomString + fname)

            if args.type == image_type.profile:
                user = UserModel.query.get(args.userid)
                user.image = os.path.basename(sf)
                db.session.commit()

                file = resize(file, 100, 80)

            file.save(sf)
            return jsonify(data=os.path.basename(sf))
        return 'pls check file suffix'

class general(Resource):
    def get(self, method = None):
        if method == 'create_all':
            db.create_all()
            
            kind = KindModel('影视大厅')
            db.session.add(kind)
            kind = KindModel('VR/AR大厅')
            db.session.add(kind)
            db.session.commit()
        elif method == 'drop_all':
            db.drop_all()
        else:
            return 'hello world!'
        return {'result':'true'}


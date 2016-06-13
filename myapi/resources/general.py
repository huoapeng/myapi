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

class image(Resource):
    def get(self, userid, imagetype, filename):
        if filename:
            fpath = os.path.join(app.config['UPLOAD_FOLDER'], path[imagetype](userid))
            return send_from_directory(fpath, filename)
        else:
            return ''

    def post(self):
        file = request.files['file']
        if file and allowed_file(file.filename):
            get_parser = reqparse.RequestParser()
            get_parser.add_argument('type', type=int, location='args', choices=range(7), default=0, required=True)
            get_parser.add_argument('userid', type=int, location='args', required=True)

            args = get_parser.parse_args()
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], path[args.type](args.userid))
            if not os.path.exists(filepath):
                # os.mkdir(filepath)
                os.makedirs(filepath)

            fname = secure_filename(file.filename)
            sf = os.path.join(filepath, fname)
            
            while os.path.exists(sf):
                randomString = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcbaABCDEFGHIJKLMNOPQRSTUVWXYZ',10))
                sf = sf.replace(fname, randomString + fname)
            file.save(sf)

            if args.type == image_type.profile:
                user = UserModel.query.get(args.userid)
                user.image = os.path.basename(sf)
                db.session.commit()
            return jsonify(data=os.path.basename(sf))
            # return jsonify(data = url_for('.imageep', 
            #     userid=args.userid, 
            #     imagetype=args.type, 
            #     filename=os.path.basename(sf), 
            #     _external=True)
            # )
        return 'pls check file suffix'

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp'])
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

path = {
    image_type.profile : lambda userid: '{}/profile/'.format(userid),
    image_type.version : lambda userid: '{}/version/'.format(userid),
    image_type.authorityPrivateFront : lambda userid: '{}/authorityPrivateFront/'.format(userid),
    image_type.authorityPrivateBack : lambda userid: '{}/authorityPrivateBack/'.format(userid),
    image_type.companyLience : lambda userid: '{}/companyLience/'.format(userid),
    image_type.companyContactCard : lambda userid: '{}/companyContactCard/'.format(userid),
}

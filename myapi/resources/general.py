#coding=utf-8
from flask.ext.restful import Resource
from myapi import db, app

class general(Resource):
    def get(self, method = None):
        if method == 'create_all':
            db.create_all()
        elif method == 'drop_all':
            db.drop_all()
        else:
            return 'hello world!'
        return {'result':'true'}

    def post(self):
        import os
        from flask import Flask, request, render_template, redirect, url_for
        from werkzeug.utils import secure_filename
        f = request.files['file']
        fname = secure_filename(f.filename) #获取一个安全的文件名，且仅仅支持ascii字符；
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
        return {'result':'true'}
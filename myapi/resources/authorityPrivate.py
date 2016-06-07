import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import datetime
from flask import jsonify
from flask.ext.restful import Resource, fields, marshal_with, marshal, reqparse
from myapi import db, app
from myapi.model.user import UserModel
from myapi.model.authority import PrivateAuthorisedModel
from myapi.model.enum import verify_type, approval_status, authorised_status

post_parser = reqparse.RequestParser()
post_parser.add_argument('user_id', type=int, location='json', required=True)
post_parser.add_argument('name', type=str, location='json')
post_parser.add_argument('identity_id', type=int, location='json')
post_parser.add_argument('identityFrontImage', type=str, location='json')
post_parser.add_argument('identityBackImage', type=str, location='json')
post_parser.add_argument('approval_id', type=int, location='json')
post_parser.add_argument('approval_status', type=int, location='json', choices=range(3), default=1)

class AuthorityPrivate(Resource):
    def get(self, id):
        authority = PrivateAuthorisedModel.query.get(id)
        return jsonify(authority.serialize())

    def post(self):
        args = post_parser.parse_args()

        p = PrivateAuthorisedModel(args.name, args.identity_id, args.identityFrontImage, args.identityBackImage)
        db.session.add(p)

        user = UserModel.query.get(args.user_id)
        user.privateAuthority = p
        user.authorisedStatus = authorised_status.start
        db.session.commit()
        return jsonify(p.serialize())

    def put(self):
        args = post_parser.parse_args()

        p = PrivateAuthorisedModel.query.get(args.approval_id)
        p.approval_status = args.approval_status
        p.approvalDate = datetime.datetime.now()

        user = UserModel.query.get(args.user_id)
        user.privateAuthority = p
        user.authorisedStatus = authorised_status.private
        db.session.commit()
        return jsonify(p.serialize())

    def delete(self):
        pass

class AuthorityPrivateList(Resource):
    def get(self):
        authorityList = PrivateAuthorisedModel.query.filter_by(approval_status=approval_status.start).all()
        return jsonify(data=[e.serialize() for e in authorityList])




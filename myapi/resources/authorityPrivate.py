import datetime
from flask import jsonify
from flask.ext.restful import Resource, fields, marshal_with, marshal, reqparse
from myapi import db, app
from myapi.model.user import UserModel
from myapi.model.authority import PrivateAuthenticateModel
from myapi.model.enum import verify_type, approval_result

post_parser = reqparse.RequestParser()
post_parser.add_argument('user_id', type=int, location='json', required=True)
post_parser.add_argument('name', type=str, location='json')
post_parser.add_argument('identity_id', type=str, location='json')
post_parser.add_argument('identityFrontImage', type=str, location='json')
post_parser.add_argument('identityBackImage', type=str, location='json')
post_parser.add_argument('approval_id', type=int, location='json')
post_parser.add_argument('approval_result', type=int, location='json', choices=range(4), default=0)

class AuthorityPrivate(Resource):
    def get(self, id):
        authority = PrivateAuthenticateModel.query.get(id)
        return jsonify(authority.serialize())

    def post(self):
        args = post_parser.parse_args()

        p = PrivateAuthenticateModel(args.name, args.identity_id, args.identityFrontImage, args.identityBackImage)
        db.session.add(p)

        user = UserModel.query.get(args.user_id)
        user.privateAuthority = p
        # user.authorisedStatus = authenticate_status.start
        db.session.commit()
        return jsonify(p.serialize())

    def put(self):
        args = post_parser.parse_args()

        p = PrivateAuthenticateModel.query.get(args.approval_id)
        p.approval_result = args.approval_result
        p.approvalDate = datetime.datetime.now()

        user = UserModel.query.get(args.user_id)
        user.privateAuthority = p
        # user.authorisedStatus = authenticate_status.none \
        #     if args.approval_result != approval_result.allow else authenticate_status.private
        db.session.commit()
        return jsonify(p.serialize())

    def delete(self):
        pass

class AuthorityPrivateList(Resource):
    def get(self):
        authorityList = PrivateAuthenticateModel.query.filter_by(approval_result=approval_result.start).all()
        return jsonify(data=[e.serialize() for e in authorityList])




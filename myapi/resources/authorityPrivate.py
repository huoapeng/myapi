import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import jsonify
from flask.ext.restful import Resource, fields, marshal_with, marshal, reqparse
from myapi import db, app
from myapi.model.user import UserModel
from myapi.model.authority import PrivateAuthorisedModel
from myapi.model.enum import verifyType, approvalStatus, approvalResult
from myapi.common.util import itemStatus

post_parser = reqparse.RequestParser()
post_parser.add_argument('user_id', type=int, location='json', required=True)
post_parser.add_argument('name', type=str, location='json', required=True)
post_parser.add_argument('identityID', type=int, location='json', required=True)

class AuthorityPrivate(Resource):
    def get(self, id):
        authority = PrivateAuthorisedModel.query.get(id)
        return jsonify(authority.serialize())

    def post(self):
        args = post_parser.parse_args()

        p = PrivateAuthorisedModel(args.name, args.identityID)
        db.session.add(p)

        user = UserModel.query.get(args.user_id)
        user.privateAuthority = p
        db.session.commit()

        return jsonify(p.serialize())

    def put(self):
        pass

    def delete(self):
        pass

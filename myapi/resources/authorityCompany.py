import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import datetime
from flask import jsonify
from flask.ext.restful import Resource, fields, marshal_with, marshal, reqparse
from myapi import db, app
from myapi.model.user import UserModel
from myapi.model.authority import CompanyAuthorisedModel
from myapi.model.enum import verify_type, approval_status, authorised_status

post_parser = reqparse.RequestParser()
post_parser.add_argument('user_id', type=int, location='json', required=True)
post_parser.add_argument('name', type=str, location='json')
post_parser.add_argument('businessScope', type=str, location='json')
post_parser.add_argument('businessLicenseID', type=str, location='json')
post_parser.add_argument('verifyType', type=int, location='json')
post_parser.add_argument('bankAccount', type=str, location='json')
post_parser.add_argument('bankName', type=str, location='json')
post_parser.add_argument('bankLocation', type=str, location='json')
post_parser.add_argument('approval_id', type=int, location='json')
post_parser.add_argument('approval_status', type=int, location='json', choices=range(4), default=1)

class AuthorityCompany(Resource):
    def get(self, id):
        authority = CompanyAuthorisedModel.query.get(id)
        return jsonify(authority.serialize())

    def post(self):
        args = post_parser.parse_args()

        c = CompanyAuthorisedModel(args.name, 
                args.businessScope,
                args.businessLicenseID,
                args.verifyType,
                args.bankAccount,
                args.bankName,
                args.bankLocation
            )
        db.session.add(c)

        user = UserModel.query.get(args.user_id)
        user.companyAuthority = c
        user.authorisedStatus = authorised_status.start
        db.session.commit()

        return jsonify(c.serialize())

    def put(self):
        args = post_parser.parse_args()

        c = CompanyAuthorisedModel.query.get(args.approval_id)
        c.approval_status = args.approval_status
        c.approvalDate = datetime.datetime.now()

        user = UserModel.query.get(args.user_id)
        user.companyAuthority = c
        user.authorisedStatus = authorised_status.company
        db.session.commit()
        return jsonify(c.serialize())

    def delete(self):
        pass

class AuthorityCompanyList(Resource):
    def get(self):
        authorityList = CompanyAuthorisedModel.query.filter_by(approval_status=approval_status.start).all()
        return jsonify(data=[e.serialize() for e in authorityList])





import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask.ext.restful import Resource, fields, marshal_with, marshal, reqparse
from myapi import db
from myapi.model.note import NoteModel
from myapi.model.message import NoteMessageModel
from myapi.model.user import UserModel

parser = reqparse.RequestParser()
parser.add_argument('message', type=str, location='json', required=True)
parser.add_argument('note_id', type=int, location='json', required=True)
parser.add_argument('user_id', type=int, location='json', required=True)

result_field = {
    'id': fields.Integer,
    'message': fields.String,
    'publish_date': fields.DateTime,
    'note_id': fields.Integer,
    'user_id': fields.Integer
}

class NoteMessage(Resource):
    def get(self):
        pass

    @marshal_with(result_field)
    def post(self):
        args = parser.parse_args()
        message = NoteMessageModel(args.message)
        db.session.add(message)

        note = NoteModel.query.get(args.note_id)
        note.messages.append(message)

        user = UserModel.query.get(args.user_id)
        user.notemessages.append(message)
        db.session.commit()
        return message

    def put(self):
        pass

    def delete(self):
        pass

class NoteMessageList(Resource):
    @marshal_with(result_field)
    def get(self, noteid):
        note = NoteModel.query.get(noteid)
        return note.messages

# class VersionMessage(Resource):
#     def get(self):
#         pass

#     @marshal_with(result_field)
#     def post(self):
#         args = parser.parse_args()
#         message = VersionMessageModel(args.message)
#         db.session.add(message)

#         version = VersionModel.query.get(args.belong_id)
#         version.messages.append(message)

#         user = UserModel.query.get(args.user_id)
#         user.versionmessages.append(message)
#         db.session.commit()
#         return message

#     def put(self):
#         pass

#     def delete(self):
#         pass

# class VersionMessageList(Resource):
#     @marshal_with(result_field)
#     def get(self, versionid):
#         version = VersionModel.query.get(versionid)
#         return version.messages

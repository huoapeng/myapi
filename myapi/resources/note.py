import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import jsonify
from flask.ext.restful import Resource, fields, marshal_with, marshal, reqparse
from myapi import db
from myapi.model.note import NoteModel
from myapi.model.user import UserModel
from myapi.model.task import TaskModel
from myapi.model.enum import note_status
from myapi.common.util import itemStatus
from myapi.view.note import NoteView

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, location='json', required=True)
parser.add_argument('task_id', type=int, location='json', required=True)
parser.add_argument('user_id', type=int, location='json', required=True)

note_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'publish_date': fields.DateTime,
    'status':  itemStatus(attribute='status'),
    'user_id': fields.Integer,
    'task_id': fields.Integer
}

class Note(Resource):
    @marshal_with(note_fields)
    def get(self, noteid):
        return NoteModel.query.get(noteid)

    @marshal_with(note_fields)
    def post(self):
        args = parser.parse_args()
        note = NoteModel(args.title)
        db.session.add(note)

        task = TaskModel.query.get(args.task_id)
        task.notes.append(note)

        user = UserModel.query.get(args.user_id)
        user.notes.append(note)
        db.session.commit()
        return note

    def put(self):
        
        pass

    @marshal_with(note_fields)
    def delete(self):
        args = parser.parse_args()
        note = NoteModel.query.get(args.id)
        note.status = version_status.delete
        db.session.commit()
        return note

class TaskNotes(Resource):
    def get(self, taskid):
        notes = NoteModel.query.filter_by(task_id=taskid).all()
        obj_list = []
        for note in notes:
            nv = NoteView(note.id,
                note.owner.id, 
                note.owner.nickname, 
                note.owner.image,
                note.title,
                note.publish_date)
            obj_list.append(nv)
        return jsonify(data=[e.serialize() for e in obj_list])


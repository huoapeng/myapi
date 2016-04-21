from flask.ext.restful import Resource
from flask.ext.restful import fields, marshal_with, reqparse
from myapi import db
from myapi.model.user import UserModel
from myapi.common.util import valid_email

post_parser = reqparse.RequestParser()
post_parser.add_argument(
    'email', dest='email',
    type=str, location='form',
    required=True, help='Missing required parameter in the JSON body ,The user\'s email',
)
post_parser.add_argument(
    'password', dest='password',
    type=str, 
    required=True, help='The user\'s password',
)
# post_parser.add_argument(
#     'user_priority', dest='user_priority',
#     type=int, location='form',
#     default=1, choices=range(5), help='The user\'s priority',
# )

user_fields = {
    'id': fields.Integer,
    'username': fields.String(default='Anonymous User'),
    'email': fields.String,
    'user_priority': fields.Integer,
    'custom_greeting': fields.FormattedString('Hey there {username}!'),
    'date_created': fields.DateTime,
    'date_updated': fields.DateTime,
    'links': fields.Nested({
        'friends': fields.Url('/Users/{id}/Friends'),
        'posts': fields.Url('Users/{id}/Posts'),
    }),
}


class User(Resource):
    def get(self, todo_id= None):
        return {'result':'true'}

    def post(self):
        args = post_parser.parse_args()
        if not valid_email(args.email,):
            return {'status':'False','message':'pls check email'}
        else:
            u = UserModel(args.email, args.password)
            db.session.add(u)
            db.session.commit()
            return {'status':'True','message':'regist successfully'}

    def put(self):
        pass

    def delete(self):
        pass

# @app.route('/')
# def show_all():
#     return render_template('show_all.html',
#         todos=Todo.query.order_by(Todo.pub_date.desc()).all()
#     )


# @app.route('/new', methods=['GET', 'POST'])
# def new():
#     if request.method == 'POST':
#         if not request.form['title']:
#             flash('Title is required', 'error')
#         elif not request.form['text']:
#             flash('Text is required', 'error')
#         else:
#             todo = Todo(request.form['title'], request.form['text'])
#             db.session.add(todo)
#             db.session.commit()
#             flash(u'Todo item was successfully created')
#             return redirect(url_for('show_all'))
#     return render_template('new.html')


# @app.route('/update', methods=['POST'])
# def update_done():
#     for todo in Todo.query.all():
#         todo.done = ('done.%d' % todo.id) in request.form
#     flash('Updated status')
#     db.session.commit()
#     return redirect(url_for('show_all'))


from random import choice
from flask_restx import Resource, Api, fields
from sqlalchemy import and_
from app.api import bp_api
from app.models import StudentModel
from app.main.forms import StudentBaseForm
from app import db, csrf
from app.main.common_funcs import filter_groups_by_size, search_student_query


api = Api(bp_api, version='1.0', title="Students", description='A simple students API', decorators=[csrf.exempt])
ns = api.namespace('students', description='Students operations')

student_model = api.model('Student', {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'group': fields.String,
    'courses': fields.List(fields.String)
})
get_parser = api.parser()
get_parser.add_argument('first_name', type=str)
get_parser.add_argument('last_name', type=str)
get_parser.add_argument(
            'group',
            choices=[choice[0] for choice in StudentBaseForm.all_groups]
)
get_parser.add_argument(
            'course',
            choices=[choice[0] for choice in StudentBaseForm.all_courses]
)

post_parser = api.parser()
post_parser.add_argument('first_name', type=str, required=True, help="First name cannot be blank!")
post_parser.add_argument('last_name', type=str, required=True, help="Last name cannot be blank!")


@ns.route('/')
class StudentList(Resource):
    @ns.expect(get_parser)
    @ns.marshal_list_with(student_model)
    def get(self):
        args = get_parser.parse_args()
        queries = search_student_query(args)
        data = StudentModel.query.filter(and_(*queries)).order_by('id').all()
        return data

    @ns.expect(post_parser)
    @ns.marshal_with(student_model, code=201)
    def post(self):
        data = post_parser.parse_args()
        available_groups = filter_groups_by_size(29, 9)
        group = choice(available_groups)
        new_student = StudentModel(
            first_name=data['first_name'],
            last_name=data['last_name'],
            group_id=group.id)
        db.session.add(new_student)
        db.session.commit()
        return new_student, 201


@ns.route('/<int:student_id>')
@ns.response(404, 'Student not found')
@ns.param('student_id', 'The student identifier')
class Student(Resource):
    @ns.doc('get_student')
    @ns.marshal_with(student_model)
    def get(self, student_id):
        """Show a single by id."""
        student = StudentModel.query.get_or_404(student_id)
        return student

    @ns.doc('delete_student')
    @ns.response(204, 'Student deleted')
    def delete(self, student_id):
        """Delete a student given its identifier."""
        current_student = StudentModel.query.get_or_404(student_id)
        db.session.delete(current_student)
        db.session.commit()
        return '', 204

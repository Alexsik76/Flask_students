from random import choice
from flask_restx import Resource, Api, fields
from sqlalchemy import and_
from app.api import bp_api
from app.models import StudentModel
from app.main.forms import StudentBaseForm
from app import db, csrf
from app.main.common_funcs import filter_groups_by_size, search_student_query


api = Api(bp_api, decorators=[csrf.exempt])
student_model = api.model('StudentModel', {
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

put_parser = api.parser()
put_parser.add_argument('first_name', type=str, required=True, help="First name cannot be blank!")
put_parser.add_argument('last_name', type=str, required=True, help="Last name cannot be blank!")


@api.route('/students')
class AllStudents(Resource):
    @api.expect(get_parser)
    @api.marshal_list_with(student_model)
    def get(self):

        args = get_parser.parse_args()
        queries = search_student_query(args)
        data = StudentModel.query.filter(and_(*queries)).order_by('id').all()
        return data

    @api.expect(put_parser)
    @api.marshal_with(student_model)
    def put(self):
        data = put_parser.parse_args()
        print(put_parser.parse_args())
        available_groups = filter_groups_by_size(29, 9)
        group = choice(available_groups)
        new_student = StudentModel(
            first_name=data['first_name'],
            last_name=data['last_name'],
            group_id=group.id)
        db.session.add(new_student)
        db.session.commit()
        return new_student

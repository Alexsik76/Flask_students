from random import choice
from flask_restx import Resource, Api, fields
from app.api import bp_api
from app.models import StudentModel, CourseModel
from app import db, csrf
from app.main.common_funcs import filter_groups_by_size


api = Api(bp_api, decorators=[csrf.exempt])
student_model = api.model('StudentModel', {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'group': fields.String,
    'courses': fields.List(fields.String)
})
parser = api.parser()
parser.add_argument('first_name', type=str, required=True, help="First name cannot be blank!")
parser.add_argument('last_name', type=str, required=True, help="Last name cannot be blank!")


@api.route('/students')
class AllStudents(Resource):
    @api.marshal_list_with(student_model)
    def get(self):
        return StudentModel.query.all()

    @api.expect(parser)
    @api.marshal_with(student_model)
    def put(self):
        data = parser.parse_args()
        print(parser.parse_args())
        available_groups = filter_groups_by_size(29, 9)
        group = choice(available_groups)
        new_student = StudentModel(
            first_name=data['first_name'],
            last_name=data['last_name'],
            group_id=group.id)
        db.session.add(new_student)
        db.session.commit()
        return new_student

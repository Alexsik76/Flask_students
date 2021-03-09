from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from app.models import GroupModel, CourseModel, StudentModel
from wtforms_alchemy import ModelForm


class StudentForm(FlaskForm):
    first_name = StringField(u'First name')
    last_name = StringField(u'Last name')
    group = StringField(u'Group')
    courses = StringField(u'Courses')
    submit = SubmitField(u'Submit')


def get_list_for_choices(query, field_name):
    items = [(item.name, item.name) for item in query]
    default_choice = f'Choice {field_name}'
    items.append(('', default_choice))
    return items


class SearchStudent(StudentForm):
    all_groups = []
    all_courses = []
    group = SelectField(u'Groups', default='')
    courses = SelectField(u'Courses', default='')

    @classmethod
    def get_choices(cls):
        cls.all_groups = get_list_for_choices(GroupModel.query.all(), 'group')
        cls.all_courses = get_list_for_choices(CourseModel.query.all(), 'courses')

    def __init__(self):
        super().__init__()
        self.group.choices = SearchStudent.all_groups
        self.courses.choices = SearchStudent.all_courses


class SearchGroup(FlaskForm):
    size = IntegerField(u'Group size')
    submit = SubmitField(u'Submit')
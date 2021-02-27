from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from app.models import GroupModel, CourseModel, StudentModel
from wtforms_alchemy import ModelForm


def get_list_for_choices(query, field_name):
    items = [(item.name, item.name) for item in query]
    default_choice = f'Choice {field_name}'
    items.append(('', default_choice))

    return items


class SearchStudent(FlaskForm):
    groups = []
    courses = []
    first_name = StringField(u'First name')
    last_name = StringField(u'Last name')
    choice_group = SelectField(u'Groups', default='')
    choice_course = SelectField(u'Courses', default='')
    submit = SubmitField(u'Submit')

    @classmethod
    def get_choices(cls):
        cls.groups = get_list_for_choices(GroupModel.query.all(), 'group')
        cls.courses = get_list_for_choices(CourseModel.query.all(), 'course')

    def __init__(self):
        super(SearchStudent, self).__init__()
        self.choice_group.choices = SearchStudent.groups
        self.choice_course.choices = SearchStudent.courses


class SearchGroup(FlaskForm):
    size = IntegerField(u'Group size')
    submit = SubmitField(u'Submit')


class StudentForm(FlaskForm, ModelForm):
    class Meta:
        model = StudentModel
    submit = SubmitField(u'Submit')

from flask_wtf import FlaskForm
from wtforms import Form, FormField, StringField, SubmitField, SelectField, IntegerField, FieldList
from app.models import GroupModel, CourseModel
from app.main.common_funcs import get_list_for_choices


class CourseForm(Form):
    name = StringField(u'Course name')
    description = StringField(u'Description')


class SearchGroup(FlaskForm):
    size = IntegerField(u'Group size')
    submit = SubmitField(u'Search')


class StudentBaseForm(FlaskForm):
    """
    :py:class: 'SearchStudent'
    """
    all_courses = []
    all_groups = []
    first_name = StringField(u'First name')
    last_name = StringField(u'Last name')
    submit = SubmitField(u'Create')

    @classmethod
    def get_choices(cls):
        cls.all_groups = get_list_for_choices(GroupModel.query.all(), 'group')
        cls.all_courses = get_list_for_choices(CourseModel.query.all(), 'course')


class StudentUpdateForm(StudentBaseForm):
    group = StringField(u'Group')
    courses = FieldList(FormField(CourseForm), u'Courses')
    av_courses = SelectField(u'Add courses', default='')
    submit = SubmitField(u'Ok')

    def __init__(self, obj, *args, **kwargs):
        super().__init__(obj=obj, *args, **kwargs)
        self.av_courses.choices = get_list_for_choices(obj.get_av_courses(), 'course')


class SearchStudent(StudentBaseForm):
    """
    :py:class: 'StudentBaseForm'
    """
    group = SelectField(u'Groups', default='')
    course = SelectField(u'Add courses', default='')
    submit_search = SubmitField(u'Search')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.course.choices = StudentBaseForm.all_courses
        self.group.choices = StudentBaseForm.all_groups

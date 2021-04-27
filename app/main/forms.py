from flask_wtf import FlaskForm
from wtforms import Form, FormField, StringField, SubmitField, SelectField, IntegerField, FieldList
from app.models import GroupModel, CourseModel
from app.main.common_funcs import get_list_for_choices


class CourseForm(Form):
    name = StringField('Course name')
    description = StringField('Description')


class SearchGroup(FlaskForm):
    size = IntegerField('Group size')
    submit = SubmitField('Search')


class StudentBaseForm(FlaskForm):
    """
    :py:class: 'SearchStudent'
    """
    all_courses = []
    all_groups = []
    first_name = StringField('First name')
    last_name = StringField('Last name')
    submit = SubmitField('Create')


class StudentUpdateForm(StudentBaseForm):
    group = StringField('Group')
    courses = FieldList(FormField(CourseForm), 'Courses')
    av_courses = SelectField('Add courses', default='')
    submit = SubmitField('Ok')

    def __init__(self, obj, *args, **kwargs):
        super().__init__(obj=obj, *args, **kwargs)
        self.av_courses.choices = get_list_for_choices(obj.get_av_courses(), 'course')


class SearchStudent(StudentBaseForm):
    """
    :py:class: 'StudentBaseForm'
    """
    group = SelectField('Groups', default='')
    course = SelectField('Add courses', default='')
    submit_search = SubmitField('Search')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.course.choices = get_list_for_choices(CourseModel.query.with_entities(CourseModel.name).all(), 'course')
        self.group.choices = get_list_for_choices(GroupModel.query.with_entities(GroupModel.name).all(), 'group')

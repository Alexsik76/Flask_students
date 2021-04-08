from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, FieldList
from app.models import GroupModel, CourseModel


class StudentBaseForm(FlaskForm):
    first_name = StringField(u'First name')
    last_name = StringField(u'Last name')
    av_courses = SelectField(u'Add courses', default='')
    submit = SubmitField(u'Ok')


class StudentUpdateForm(StudentBaseForm):
    group = StringField(u'Group')
    courses = FieldList(StringField(u'Courses'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.av_courses.choices = get_list_for_choices(kwargs.get('obj', None).get_av_courses(), 'course')


def get_list_for_choices(values, field_name):
    items = [(item.name, item.name) for item in values]
    default_choice = f'Choice {field_name}'
    items.append(('', default_choice))
    return items


class SearchStudent(StudentBaseForm):
    """ Subclass of StudentBaseForm.


    """
    group = SelectField(u'Groups', default='')

    @classmethod
    def get_choices(cls):
        cls.all_groups = get_list_for_choices(GroupModel.query.all(), 'group')
        cls.all_courses = get_list_for_choices(CourseModel.query.all(), 'course')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group.choices = SearchStudent.all_groups
        self.av_courses.choices = SearchStudent.all_courses


class SearchGroup(FlaskForm):
    size = IntegerField(u'Group size')
    submit = SubmitField(u'Submit')

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, FieldList
from app.models import GroupModel, CourseModel


class StudentForm(FlaskForm):
    all_groups = []
    all_courses = []
    first_name = StringField(u'First name')
    last_name = StringField(u'Last name')
    group = StringField(u'Group')
    courses = FieldList(StringField(u'Courses'))
    choice_course = SelectField(u'Add courses', default='')
    submit = SubmitField(u'Ok')

    @classmethod
    def get_choices(cls):
        cls.all_groups = get_list_for_choices(GroupModel.query.all(), 'group')
        cls.all_courses = get_list_for_choices(CourseModel.query.all(), 'course')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.group.choices = SearchStudent.all_groups
        selected_courses = [str(item) for item in self.courses.data]
        self.choice_course.choices = [choice for choice in self.all_courses if choice[0] not in selected_courses]


def get_list_for_choices(values, field_name):
    items = [(item.name, item.name) for item in values]
    default_choice = f'Choice {field_name}'
    items.append(('', default_choice))
    return items


class SearchStudent(StudentForm):
    group = SelectField(u'Groups', default='')
    choice_course = SelectField(u'Courses', default='')
    submit = SubmitField(u'Submit')


class SearchGroup(FlaskForm):
    size = IntegerField(u'Group size')
    submit = SubmitField(u'Submit')

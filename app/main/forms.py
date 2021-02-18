from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from app.models import GroupModel, CourseModel


def get_list_for_choices(query, field_name):
    items = [(item.name, item.name) for item in query]
    default_choice = f'Choice {field_name}'
    items.append(('', default_choice))
    print('Choices are created')
    return items


class SearchForm(FlaskForm):
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
        super(SearchForm, self).__init__()
        self.choice_group.choices = SearchForm.groups
        self.choice_course.choices = SearchForm.courses




from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from app.models import GroupModel, CourseModel


class SearchForm(FlaskForm):
    first_name = StringField(u'First name')
    last_name = StringField(u'Last name')
    choice_group = SelectField(u'Groups', default='')
    choice_course = SelectField(u'Courses', default='')
    submit = SubmitField(u'Submit')

    def __init__(self):
        super(SearchForm, self).__init__()

        def get_list_for_choices(query, field_name):
            with current_app.app_context():
                items = [(item.name, item.name) for item in query]
                default_choice = f'Choice {field_name}'
                items.append(('', default_choice))
            return items
        self.choice_group.choices = get_list_for_choices(GroupModel.query.all(), 'group')
        self.choice_course.choices = get_list_for_choices(CourseModel.query.all(), 'course')




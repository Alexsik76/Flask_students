from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from app.models import GroupModel, CourseModel
from werkzeug.utils import cached_property

search_fields = [('first_name', 'First name'), ('last_name', 'Last name'), ('group', 'Group'), ('course', 'Course')]


def get_list(app, query):
    with app.app_context():
        groups = [group.name for group in query]
    return groups


class SearchForm(FlaskForm):
    choice_group = SelectField(u'Groups', choices=get_list(current_app, GroupModel.query.all()))
    choice_course = SelectField(u'Courses', choices=get_list(current_app, CourseModel.query.all()))
    search_text = StringField('Search')
    search_by = SelectField(u'Search by', choices=search_fields, default='first_name')
    submit = SubmitField('Submit')

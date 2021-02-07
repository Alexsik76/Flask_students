from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField


search_fields = [('first_name', 'First name'), ('last_name', 'Last name'), ('group', 'Group'), ('course', 'Course')]


class SearchForm(FlaskForm):
    choice_group = SelectField(u'Groups', default=None)
    choice_course = SelectField(u'Courses', default=None)
    search_text = StringField(u'Search')
    search_by = SelectField(u'Search by', choices=search_fields, default='first_name')
    submit = SubmitField(u'Submit')

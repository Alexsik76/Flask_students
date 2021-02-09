from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField


class SearchForm(FlaskForm):
    first_name = StringField(u'First name')
    last_name = StringField(u'Last name')
    choice_group = SelectField(u'Groups', default='')
    choice_course = SelectField(u'Courses', default='')
    submit = SubmitField(u'Submit')

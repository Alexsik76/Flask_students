from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    search_text = StringField('Search')
    search_by = SelectField(u'Search by', choices=[('first_name', 'First name'), ('last_name', 'Last name')], default='first_name')
    submit = SubmitField('Submit')

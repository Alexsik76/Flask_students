from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, FieldList
from app.models import GroupModel, CourseModel


class StudentForm(FlaskForm):
    first_name = StringField(u'First name')
    last_name = StringField(u'Last name')
    group = StringField(u'Group')
    courses = FieldList(StringField(u'Courses'))
    av_courses = SelectField(u'Add courses', default='')
    submit = SubmitField(u'Ok')

    @classmethod
    def get_choices(cls):
        cls.all_groups = get_list_for_choices(GroupModel.query.all(), 'group')
        cls.all_courses = get_list_for_choices(CourseModel.query.all(), 'course')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group.choices = StudentForm.all_groups
        self.selected_courses = [str(item) for item in self.courses.data]
        if student := kwargs.get('obj', None):
            self.av_courses.choices = get_list_for_choices(student.get_av_courses(), 'course')
        else:
            self.av_courses.choices = StudentForm.all_courses


def get_list_for_choices(values, field_name):
    items = [(item.name, item.name) for item in values]
    default_choice = f'Choice {field_name}'
    items.append(('', default_choice))
    return items


# class CreateStudentForm(FlaskForm):
#     first_name = StringField(u'First name')
#     last_name = StringField(u'Last name')
#     submit_c = SubmitField(u'Create')
#
#
class SearchStudent(StudentForm):
    group = SelectField(u'Groups', default='')


class SearchGroup(FlaskForm):
    size = IntegerField(u'Group size')
    submit = SubmitField(u'Submit')

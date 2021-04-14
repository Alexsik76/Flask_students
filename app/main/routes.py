import os
from random import choice
from functools import wraps
from flask import render_template, current_app, url_for, flash, redirect, request, jsonify, session
from sqlalchemy import and_, func
from app.models import GroupModel, CourseModel, StudentModel
from app.main import bp
from app.main.forms import SearchGroup,  StudentBaseForm, SearchStudent, StudentUpdateForm
from app.schemas import StudentSchema, CourseSchema
from app import db

students_schema = StudentSchema(many=True)
courses_schema = CourseSchema(many=True)


def get_readme_text() -> str:
    """ Read README.md file

    :return: text from file
    """
    path_to_file = os.path.join(current_app.config['BASE_DIR'], 'README.md')
    with open(path_to_file, encoding='utf8') as file:
        readme = file.read()
    return readme


@bp.route('/')
@bp.route('/index')
def index():
    text = get_readme_text()
    return render_template('index.html', md_text=text)


def create_query(form):
    query_dict = {
        'group': StudentModel.group.has(GroupModel.name == form.group.data),
        'av_courses': StudentModel.courses.any(CourseModel.name == form.av_courses.data),
        'first_name': StudentModel.first_name == form.first_name.data,
        'last_name': StudentModel.last_name == form.last_name.data
    }
    queries = tuple(value for key, value in query_dict.items() if getattr(form, key).data)
    return queries


def filter_groups_by_size(max_size, min_size=0):
    filtered_groups = GroupModel.query \
        .join(GroupModel.students) \
        .group_by(GroupModel) \
        .having(func.count_(GroupModel.students) <= max_size) \
        .having(func.count_(GroupModel.students) >= min_size) \
        .all()
    return filtered_groups


def with_search_modal(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        form_dict = {
            'search_groups': (SearchGroup(), 'search_groups.html'),
            'search_student': (SearchStudent(), 'search_student.html')
        }
        if form_name := request.args.get('needed_form'):
            form, template = form_dict[form_name]
            return render_template(template, search_form=form)
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/students/', methods=['GET', 'POST'])
@with_search_modal
def students():
    search_form = SearchStudent()
    if search_form.is_submitted() and search_form.submit_search.data:
        queries = create_query(search_form)
        data = StudentModel.query.filter(and_(*queries)).order_by('id').all()
    else:
        data = StudentModel.query.order_by('id').all()
    data_json = students_schema.dump(data)
    last_modified = session.pop('last_modified', data[0].id)
    return render_template('students.html', data_students=data_json, l_m=last_modified)


@bp.route('/groups/', methods=['GET', 'POST'])
@with_search_modal
def groups():
    search_form = SearchGroup()
    source_data = filter_groups_by_size(search_form.size.data or 100)
    data = [item.get_dict() for item in source_data]
    titles = [('name', 'Group name'), ('size', 'Group size')]
    return render_template('groups.html', data_groups=data, titles=titles)


@bp.route('/create_student/', methods=['GET', 'POST'])
def create_student():
    create_form = StudentBaseForm()
    if create_form.is_submitted():
        available_groups = filter_groups_by_size(29, 9)
        group = choice(available_groups)
        new_student = StudentModel(
            first_name=create_form.first_name.data,
            last_name=create_form.last_name.data,
            group_id=group.id)
        db.session.add(new_student)
        db.session.commit()
        session['last_modified'] = new_student.id
        return redirect(url_for('main.students'), 302)
    return render_template('create_student.html', create_student=create_form)


@bp.route('/delete_student/', methods=['GET', 'POST'])
def delete_student():
    student_id = int(request.form['student_id'])
    current_student = StudentModel.query.get_or_404(student_id)
    neighbour = StudentModel.query.filter(StudentModel.id > student_id).first() or StudentModel.query.first()
    session['last_modified'] = neighbour.id
    db.session.delete(current_student)
    db.session.commit()
    return jsonify({"success": True})


@bp.route('/students/<pk>', methods=['GET', 'POST'])
def student(pk):
    this_student = StudentModel.query.get_or_404(pk)
    form = StudentUpdateForm(obj=this_student)
    if form.is_submitted():
        return redirect(url_for('main.students'), 302)
    return render_template('student.html', form=form, student_id=pk)


@bp.route('/update_courses/', methods=['GET', 'POST'])
def process_course():
    course_name, student_id, action = request.form.values()
    course = CourseModel.query.filter_by(name=course_name).first_or_404()
    student_obj = StudentModel.query.get_or_404(student_id)
    getattr(student_obj.courses, action)(course)
    db.session.commit()
    session['last_modified'] = student_obj.id
    data = {'courses': courses_schema.dump(student_obj.courses),
            'av_courses': courses_schema.dump(student_obj.get_av_courses())}
    return jsonify(data)


@bp.app_errorhandler(404)
def page_not_found(error):
    flash(error.description, 'error')
    return redirect(url_for('main.index'), 302)

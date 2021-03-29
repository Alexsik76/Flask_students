import os
from flask import render_template, current_app, url_for, flash, redirect, request, Response, json, jsonify
from sqlalchemy import and_, func
from app.models import GroupModel, CourseModel, StudentModel
from app.main import bp
from app.main.forms import SearchStudent, SearchGroup, StudentForm
from app import db


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
        'choice_course': StudentModel.courses.any(CourseModel.name == form.choice_course.data),
        'first_name': StudentModel.first_name == form.first_name.data,
        'last_name': StudentModel.last_name == form.last_name.data
    }
    queries = tuple(value for key, value in query_dict.items() if getattr(form, key).data)
    return queries


@bp.route('/students', methods=['GET', 'POST'])
def students():
    search_form = SearchStudent()
    queries = create_query(search_form)
    data = StudentModel.query.all()
    if search_form.is_submitted():
        data = StudentModel.query.filter(and_(*queries)).all()
    student_form = StudentForm()
    return render_template('students.html', data=data, search_form=search_form, student_form=student_form)


@bp.route('/students/<pk>', methods=['GET', 'POST'])
def student(pk):
    this_student = StudentModel.query.get_or_404(pk)
    form = StudentForm(obj=this_student)
    if form.is_submitted():
        return redirect(url_for('main.students'), 302)
    return render_template('student.html', form=form, student_id=pk)


def get_course_student(request_data):
    course, student_id = request_data.form.values()
    this_student = StudentModel.query.get_or_404(student_id)
    course = CourseModel.query.filter_by(name=course).first()
    return course, this_student


@bp.route('/add_course/', methods=['POST'])
def add_course():
    course, student_obj = get_course_student(request)
    student_obj.courses.append(course)
    db.session.commit()
    flash(f'Course {course} added.', 'success')
    return student(student_obj.id)


def make_response(obj):
    courses = [str(course) for course in obj.courses]
    available_courses = [str(av_course) for av_course in CourseModel.query.all() if str(av_course) not in courses]
    response = jsonify(courses=courses, av_courses=available_courses)
    return response


@bp.route('/del_course/', methods=['POST'])
def del_course():
    course, student_obj = get_course_student(request)
    student_obj.courses.remove(course)
    db.session.commit()
    flash(f'Course {course} deleted.', 'success')
    _, student_obj = get_course_student(request)
    result = make_response(student_obj)
    # response = Response(result, mimetype='application/json')
    return result


@bp.route('/groups', methods=['GET', 'POST'])
def groups():
    form = SearchGroup()
    if form.is_submitted() and (size := form.size.data):
        source_data = GroupModel.query \
            .join(GroupModel.students) \
            .group_by(GroupModel).having(
             func.count_(GroupModel.students) <= size
             ).all()
    else:
        source_data = GroupModel.query.all()
    data = [item.get_dict() for item in source_data]
    titles = [('name', 'Group name'), ('size', 'Group size')]
    return render_template('groups.html', data=data, titles=titles, search_form=form)


@bp.app_errorhandler(404)
def page_not_found(error):
    flash(error.description, 'error')
    return index()


def has_no_empty_params(rule) -> bool:
    """
    Filters rules without arguments.

    :param rule: app or blueprint rule
    :return: True or False
    :rtype: bool
    """
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@bp.route("/site-map")
def site_map():
    links = []
    for rule in current_app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return render_template("all_links.html", links=links)

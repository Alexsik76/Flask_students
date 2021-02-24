import os
from flask import render_template, request, current_app, abort, url_for, flash, redirect, session
from sqlalchemy import and_, func
from app.models import GroupModel, CourseModel, StudentModel
from app.main import bp
from app.main.forms import SearchStudent, SearchGroup


def html_from_readme() -> str:
    """ Read README.md file

    :return: text from file
    """
    path_to_file = os.path.join(current_app.config['BASE_DIR'], 'README.md')
    with open(path_to_file, encoding='utf8') as file:
        readme_html = file.read()
    return readme_html


@bp.route('/')
@bp.route('/index')
def index():

    return render_template('index.html', md_text=html_from_readme())


def create_query(form):
    query_dict = {
        'choice_group': StudentModel.group.has(GroupModel.name == form.choice_group.data),
        'choice_course': StudentModel.courses.any(CourseModel.name == form.choice_course.data),
        'first_name': StudentModel.first_name == form.first_name.data,
        'last_name': StudentModel.last_name == form.last_name.data
    }
    queries = tuple(value for key, value in query_dict.items() if getattr(form, key).data)
    return queries


@bp.route('/students', methods=['GET', 'POST'])
def students():
    form = SearchStudent()
    queries = create_query(form)
    data = StudentModel.query.all()
    if form.is_submitted():
        data = StudentModel.query.filter(and_(*queries)).all()
    return render_template('students.html', data=data, form=form, search='students')


@bp.route('/students/<pk>')
def info_student(pk):
    this_student = StudentModel.query.get_or_404(pk)
    return render_template('student.html', student=this_student)


@bp.route('/groups', methods=['GET', 'POST'])
def groups():
    form = SearchGroup()
    if form.is_submitted() and (size := form.size.data):
        source_data = GroupModel.query \
            .outerjoin(GroupModel.students) \
            .group_by(GroupModel).having(
             func.count_(GroupModel.students) <= size
             ).all()
    else:
        source_data = GroupModel.query.all()
    data = [item.get_dict() for item in source_data]
    titles = [('name', 'Group name'), ('size', 'Group size')]
    return render_template('groups.html', data=data, titles=titles, form=form, search='groups')


@bp.app_errorhandler(404)
def page_not_found(error):
    flash(error, 'danger')
    return render_template('index.html', md_text=html_from_readme())


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

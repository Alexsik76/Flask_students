import os
from flask import render_template, request, current_app, abort, url_for, flash

from app.models import GroupModel, CourseModel, StudentModel
from app.main import bp



# def flash_content(is_desc) -> tuple:
#     """Forms params of the flash function.
#
#     :param is_desc: boolean format of the sort order
#     :return: tuple(text of a flash message, category of the message)
#     """
#     sort_order = 'DESC' if is_desc else 'ASC'
#     founded = (f'Data sorted by {sort_order}', 'primary')
#     not_founded = ('Application did not found needed data files.', 'danger')
#     return founded if Racer.select() else not_founded


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
    # select = Racer.select()
    # rows = f'tables = {len(select)}'
    # if rows:
    #     flash(f'Database has "{rows}" rows. Application ready to work.', 'primary')
    # else:
    #     flash('Application did not found needed data files.', 'danger')
    return render_template('index.html', md_text=html_from_readme())


@bp.route('/students')
def all_students():
    students = StudentModel.query.all()
    return render_template('students.html', students=students)


@bp.route('/students/<pk>')
def info_student(pk):
    this_student = StudentModel.query.get_or_404(pk)
    return render_template('student.html', student=this_student)


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

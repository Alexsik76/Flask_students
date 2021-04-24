from random import choice
from functools import wraps
from flask import render_template, url_for, flash, redirect, request, jsonify, session
from sqlalchemy import and_
from app.models import CourseModel, StudentModel
from app.main import bp
from app.main.forms import SearchGroup, StudentBaseForm, SearchStudent, StudentUpdateForm
from app.schemas import StudentSchema
from app import db
from app.main.common_funcs import get_readme_text, search_student_query, filter_groups_by_size


students_schema = StudentSchema(many=True)


@bp.route('/')
@bp.route('/index')
def index():
    """ Display base page with readme."""
    text = get_readme_text()
    return render_template('index.html', md_text=text)


def with_search_modal(f):
    """ Add modal to the 'students' and 'groups' pages.
    Both those pages need a similar modal for search.
    To not repeat both function are wrapped in this decorator.

    :param f: students() or groups()
    :type f: function
    :return: page with modal
    :rtype: Response or None
    """
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
    """Display table with all students if all fields of search form are empty or if you are not searching.
    Else displays the search result.
    Also transfers data about last modified student to the template for JS functions.
    """
    search_form = SearchStudent()
    if search_form.is_submitted() and search_form.submit_search.data:
        queries = search_student_query(search_form.data)
        data = StudentModel.query.filter(and_(*queries)).order_by('id').all()
    else:
        data = StudentModel.query.order_by('id').all()
    data_json = students_schema.dump(data)
    last_modified = session.pop('last_modified', None)
    return render_template('students.html', data_students=data_json, l_m=last_modified)


@bp.route('/groups/', methods=['GET', 'POST'])
@with_search_modal
def groups():
    """ Display table with all groups if field of search form is empty or if you are not searching.
    Else displays the search result.
    """
    search_form = SearchGroup()
    source_data = filter_groups_by_size(search_form.size.data or 100)
    data = [item.get_dict() for item in source_data]
    titles = [('name', 'Group name'), ('size', 'Group size')]
    return render_template('groups.html', data_groups=data, titles=titles)


@bp.route('/_create_student/', methods=['GET', 'POST'])
def create_student():
    """ Create student from form data. Automatically sets a group.
    May be called only from main.js by clicking on a button.
    Update the session['last_modified'] variable.
    """
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
        session['last_modified'] = {"updated": new_student.id}
        return redirect(url_for('main.students'), 302)
    return render_template('create_student.html', create_student=create_form)


@bp.route('/_delete_student/', methods=['GET', 'POST'])
def delete_student():
    """" Delete the chosen student.
    May be called only from main.js by clicking on a button.
    Update the session['last_modified'] variable by number of the nearest neighbour before deleted student.
    """
    student_id = request.form['student_id']
    assert type(request.form['student_id']) == str
    current_student = StudentModel.query.get_or_404(student_id)
    db.session.delete(current_student)
    db.session.commit()
    neighbour = StudentModel.query\
        .with_entities(StudentModel.id) \
        .filter(StudentModel.id < student_id) \
        .order_by(StudentModel.id.desc()) \
        .first() \
        or StudentModel.query.first()
    session['last_modified'] = {"after_deleted": neighbour.id}
    print(neighbour.id)
    return jsonify({"success": True})


@bp.route('/students/<pk>', methods=['GET', 'POST'])
def student(pk):
    """Display modal with information about this <pk> student."""
    this_student = StudentModel.query.get_or_404(pk)
    form = StudentUpdateForm(obj=this_student)
    if form.is_submitted():
        return redirect(url_for('main.students'), 302)
    return render_template('student.html', form=form, student_id=pk)


@bp.route('/_update_courses/', methods=['GET', 'POST'])
def process_course():
    """ Serve AJAX queries about adding or removing course of the student.
    Update the session['last_modified'] variable.
    """
    course_name, student_id, action = request.form.values()
    course = CourseModel.query.filter_by(name=course_name).first_or_404()
    student_obj = StudentModel.query.get_or_404(student_id)
    getattr(student_obj.courses, action)(course)
    db.session.commit()
    session['last_modified'] = {"updated": student_obj.id}
    new_form = StudentUpdateForm(obj=student_obj, formdata=None)
    new_template = render_template('student.html', form=new_form, student_id=student_id)
    return jsonify({'new_template': new_template})


@bp.app_errorhandler(404)
def page_not_found(error):
    flash(error.description, 'error')
    return redirect(url_for('main.index'), 302)

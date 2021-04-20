import os
from flask import current_app
from sqlalchemy import func
from app.models import GroupModel, CourseModel, StudentModel


def get_readme_text() -> str:
    """ Read README.md file

    :return: text from file
    """
    path_to_file = os.path.join(current_app.config['BASE_DIR'], 'README.md')
    with open(path_to_file, encoding='utf8') as file:
        readme = file.read()
    return readme


def search_student_query(form):
    query_dict = {
        'group': StudentModel.group.has(GroupModel.name == form.group.data),
        'course': StudentModel.courses.any(CourseModel.name == form.course.data),
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


def get_list_for_choices(values, field_name):
    items = [(item.name, item.name) for item in values]
    default_choice = f'Choice {field_name}'
    items.append(('', default_choice))
    return items

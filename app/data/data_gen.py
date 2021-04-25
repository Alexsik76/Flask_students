import os
import json
from random import choice
from string import ascii_lowercase as letters
from string import digits
import names


def get_student():
    """ Generate random first and last names of the students from the 'names' package.

    :rtype: (str, str)
    :return: First name, Last name
    """
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    return first_name, last_name


def get_courses():
    """ Get list of courses from the local file.

    :rtype: dict
    :return: dict {course_name: description}
    """
    basedir = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(basedir, 'data.json')) as file:
        data = json.load(file)
    return data['courses']


def get_group():
    """ Generate group name which contains 2 characters, hyphen, 2 numbers.

    :rtype: str
    :return: Group name
    """
    return f'{choice(letters)}{choice(letters)}-' \
           f'{choice(digits)}{choice(digits)}'


def generate():
    """ Generate lists of students, groups and courses of given sizes.
    Also print sizes of these lists to the console.

    :rtype: (list, list, dict)
    :return: tuple (list[str], list[str], dict{str:str}).
    """
    students = [get_student() for _ in range(200)]
    groups = [get_group() for _ in range(10)]
    courses = get_courses()
    print('Students:\t\t', len(students), '\nGroups:\t\t', len(groups), '\nCourses:\t', len(courses))
    return students, groups, courses

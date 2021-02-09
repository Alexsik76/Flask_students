import json
from random import choice
from string import ascii_lowercase as letters
from string import digits
import names


def get_student():
    first_name = names.get_first_name(gender=choice(('male', 'female')))
    last_name = names.get_last_name()
    return first_name, last_name


def get_course():
    with open('data/data.json') as file:
        data = json.load(file)
    return choice(data['courses'])


def get_group():
    return f'{choice(letters)}{choice(letters)}-' \
           f'{choice(digits)}{choice(digits)}'


def generate():
    students = [get_student() for i in range(200)]
    groups = [get_group() for j in range(10)]
    courses = get_course()
    print('Students:\t\t', len(students), '\nGroups:\t\t', len(groups), '\nCourses:\t', len(courses))
    return students, groups, courses

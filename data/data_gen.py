import json
from random import choice
from string import ascii_lowercase as letters
from string import digits


with open('data.json') as file:
    data = json.load(file)


def get_user():
    return choice(data['first_names']), \
           choice(data['last_names'])


def get_course():
    return choice(data['courses'])


def get_group():
    return f'{choice(letters)}{choice(letters)}-' \
           f'{choice(digits)}{choice(digits)}'


users = [get_user() for i in range(200)]
groups = [get_group() for j in range(10)]
courses = data['courses']

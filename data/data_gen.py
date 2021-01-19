from random import choice
import string


with open('first_names.txt') as file:
    first_names = list(file)

with open('last_names.txt') as file:
    last_names = list(file)


print(*first_names)


def get_group_name():
    letter = choice(string.ascii_lowercase)
    number = choice(string.digits)
    return f'{letter}{letter}{number}{number}{letter}{letter}'


def get_user_name():
    return f'{choice(first_names)} {choice(last_names)}'


def get_course_name():
    pass


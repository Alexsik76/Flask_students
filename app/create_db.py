import click
from flask.cli import with_appcontext
from random import randint, sample

from app import db
from app.models import GroupModel, CourseModel, StudentModel
from data.data_gen import generate


def init_db():
    if db.table:
        db.drop_all()
    db.create_all()
    students, groups, courses = generate()
    courses_db = [CourseModel(name=course) for course in courses]
    db.session.add_all(courses_db)
    students_db = []
    for student in students:
        first_name, last_name = student
        target_courses = sample(courses_db, randint(1, 3))
        students_db.append(StudentModel(first_name=first_name,
                                        last_name=last_name,
                                        courses=target_courses))
    db.session.add_all(students_db)
    groups_db = [GroupModel(name=group) for group in groups]
    db.session.add_all(groups_db)
    for group in groups_db:
        for group_size in range(randint(10, 30)):
            student = students_db.pop()
            student.group = group
    db.session.commit()
    print('Data stored to the DB')


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.cli.add_command(init_db_command)

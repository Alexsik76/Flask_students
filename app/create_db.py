import click
from flask.cli import with_appcontext
from random import randint

from app import db
from app.models import GroupModel, CourseModel, StudentModel
from data.data_gen import students, groups, courses


def init_db():
    if db.table:
        db.drop_all()
    db.create_all()
    groups_db = [GroupModel(name=group) for group in groups]
    db.session.add_all(groups_db)
    courses_db = [CourseModel(name=course) for course in courses]
    db.session.add_all(courses_db)
    students_db = []
    for group in GroupModel.query.all():
        for number in range(randint(10, 30)):
            if students:
                first_name, last_name = students.pop()
                students_db.append(StudentModel(first_name=first_name, last_name=last_name, group_id=group.id))
    db.session.add_all(students_db)
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

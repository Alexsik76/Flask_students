import click
from tqdm import tqdm
from app.models import GroupModel, CourseModel, StudentModel
from flask.cli import with_appcontext
from random import randint, sample
from app import db
from app.data.data_gen import generate


def init_db():
    db.drop_all()
    print('All tables are dropped.')
    db.create_all()
    print('Created new tables.')
    students, groups, courses = generate()
    print('Students, groups names are generated. Courses names and descriptions loaded from file.')
    db.session.add_all([CourseModel(name=name, description=description) for name, description in courses.items()])
    print('10 courses were add to db.')
    db.session.add_all([GroupModel(name=group) for group in groups])
    print('10 groups were add to db.')
    students_db = []
    print('Creating students...')
    for student in tqdm(students):
        first_name, last_name = student
        target_courses = sample(CourseModel.query.all(), randint(1, 3))
        students_db.append(StudentModel(first_name=first_name,
                                        last_name=last_name,
                                        courses=target_courses))
    db.session.add_all(students_db)
    print('Randomly assigning students to groups...')
    pbar = tqdm(total=200)
    while StudentModel.query.filter_by(group_id=None).count() > 9:
        for group in GroupModel.query.all():
            for group_size in range(randint(10, 30)):
                if student := StudentModel.query.filter_by(group_id=None).first():
                    student.group_id = group.id
                    pbar.update(1)
    pbar.close()
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

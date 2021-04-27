from app import create_app, db
from app.models import StudentModel, GroupModel, CourseModel
app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'StudentModel': StudentModel, 'GroupModel': GroupModel, 'CourseModel': CourseModel}

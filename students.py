from app.models import StudentModel, GroupModel, CourseModel
from app import db, create_app
app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'StudentModel': StudentModel, 'GroupModel': GroupModel, 'CourseModel': CourseModel}

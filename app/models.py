from app import db


courses = db.Table('courses',
                   db.Column('student_id', db.Integer, db.ForeignKey('student_model.id'), primary_key=True),
                   db.Column('course_id', db.Integer, db.ForeignKey('course_model.id'), primary_key=True))


class CourseModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), index=True)
    description = db.Column(db.String(124), index=True)

    def __repr__(self):
        return f'<{self.name=} {self.description=}>'


class GroupModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(5), index=True)
    students = db.relationship('StudentModel', backref='group', lazy=True)

    def get_dict(self):
        return {'name': self.name, 'size': len(self.students)}

    def __repr__(self):
        return f'<Group {self.name}>'


class StudentModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(24), index=True)
    last_name = db.Column(db.String(24), index=True)
    courses = db.relationship('CourseModel', secondary=courses, lazy='subquery',
                              backref=db.backref('students', lazy=True))
    group_id = db.Column(db.Integer, db.ForeignKey('group_model.id'))

    def __repr__(self):
        return f'<Student {self.first_name} {self.last_name}\n' \
               f'Group {self.group.name}\n>'

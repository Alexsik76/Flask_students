from app import db


courses = db.Table('courses',
                   db.Column('student_id', db.Integer, db.ForeignKey('student_model.id'), primary_key=True),
                   db.Column('course_id', db.Integer, db.ForeignKey('course_model.id'), primary_key=True))


class CourseModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), index=True)
    description = db.Column(db.String(124))

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class GroupModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(5), index=True)
    students = db.relationship('StudentModel', backref='group', lazy=True)

    def get_dict(self):
        return {'name': self.name, 'size': StudentModel.query.with_parent(self).count()}

    def __repr__(self):
        return f'<Group {self.name}>'

    def __str__(self):
        return self.name


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

    def __str__(self):
        courses_str = [course.name for course in self.courses]
        return f'{self.first_name} {self.last_name} {self.group.name} {courses_str}'

    def get_av_courses(self):
        my_courses = CourseModel.query\
            .with_parent(self)\
            .with_entities(CourseModel.id)
        av_courses = CourseModel.query\
            .filter(CourseModel.id.notin_(my_courses)).all()
        return av_courses

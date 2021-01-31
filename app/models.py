from app import db


class GroupModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(6), index=True)

    def __repr__(self):
        return f'<Group {self.name}>'


class CourseModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), index=True)
    description = db.Column(db.String(124), index=True)

    def __repr__(self):
        return f'<Student {self.name} {self.description}>'


class StudentModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(24), index=True)
    last_name = db.Column(db.String(24), index=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group_model.id'), nullable=False)
    group = db.relationship('GroupModel', backref=db.backref('students', lazy=True))

    def __repr__(self):
        return f'<Student {self.first_name} {self.last_name}\n' \
               f'Group {self.group}\n>'

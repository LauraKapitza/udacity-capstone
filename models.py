from sqlalchemy.dialects.postgresql import ARRAY

from config import db
import enum


class DanceTypes(enum.Enum):
    hiphop = "Hip-Hop"
    ballet = "Ballet"
    ballroom = "Ballroom"
    contemporary = "Contemporary"
    afrobeat = "Afrobeat"
    jazz = "Jazz Dance"
    tap = "Tap Dance"
    folk = "Folk Dance"
    dancehall = "Dancehall"
    modern = "Modern Dance"
    swing = "Swing Dance"

    def format(self):
        return self.name


classes_through_students_table = db.Table(
    "classes_through_students_table",
    db.Model.metadata,
    db.Column("class_id", db.ForeignKey("classes.id"), primary_key=True),
    db.Column("student_id", db.ForeignKey("students.id"), primary_key=True),
)


class Class(db.Model):
    __tablename__ = "classes"

    id = db.Column(db.Integer, primary_key=True)
    participants = db.relationship("Student",
                                   secondary=classes_through_students_table, back_populates="dance_classes"
                                   )
    teacher_id = db.Column(db.ForeignKey("teachers.id"))
    teacher = db.relationship("Teacher", back_populates="classes")
    dance_types = db.Column(ARRAY(db.Enum(DanceTypes)))
    title = db.Column(db.String)
    description = db.Column(db.String)
    max_participants = db.Column(db.Integer)
    date = db.Column(db.Date)
    start_time = db.Column(db.String)
    end_time = db.Column(db.String)

    # def __init__(self, teacher, dance_types, title, description, max_participants, date, start_time, end_time, participants):
    #     self.teacher = teacher
    #     self.dance_types = dance_types
    #     self.title = title
    #     self.description = description
    #     self.max_participants = max_participants
    #     self.date = date
    #     self.start_time = start_time
    #     self.end_time = end_time
    #     self.participants = participants

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format_short(self):
        return {
            "id": self.id,
            "dance_types": [t.format() for t in self.dance_types],
            "title": self.title,
            "description": self.description,
            "max_participants": self.max_participants,
            "date": self.date,
            "start_time": self.start_time,
            "end_time": self.end_time,
        }

    def format_long(self):
        return {
            "id": self.id,
            "participants": [p.format_short() for p in self.participants],
            "teacher": self.teacher.format_short(),
            "dance_types": [t.format() for t in self.dance_types],
            "title": self.title,
            "description": self.description,
            "max_participants": self.max_participants,
            "date": self.date,
            "start_time": self.start_time,
            "end_time": self.end_time,
        }


class Teacher(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    classes = db.relationship("Class", back_populates="teacher")
    dance_types = db.Column(ARRAY(db.Enum(DanceTypes)))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format_short(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name
        }

    def format_long(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "dance_types": [t.format() for t in self.dance_types],
            "classes": [c.format_short() for c in self.classes]
        }


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    dance_classes = db.relationship("Class",
                                    secondary=classes_through_students_table, back_populates="participants"
                                    )

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format_short(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name
        }

    def format_long(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "dance_classes": [c.format_short() for c in self.dance_classes]
        }

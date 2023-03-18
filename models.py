import sqlalchemy.dialects.postgresql as pg

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


classes_through_students_table = db.Table(
    "classes_through_students_table",
    db.Model.metadata,
    db.Column("class_id", db.ForeignKey("classes.id"), primary_key=True),
    db.Column("student_id", db.ForeignKey("students.id"), primary_key=True),
)


class Class(db.Model):
    __tablename__ = "classes"

    id = db.Column(db.Integer, primary_key=True)
    participants = db.relationship("participants",
        secondary=classes_through_students_table, backref="dance_classes"
    )
    teacher_id = db.Column(db.ForeignKey("teachers.id"))
    teacher = db.relationship("teacher",backref="classes")
    dance_types = db.Column(pg.ARRAY(db.Enum(DanceTypes)))
    title = db.Column(db.String)
    description = db.Column(db.String)
    max_participants = db.Column(db.Integer)
    date = db.Column(db.Date)
    start_time = db.Column(db.String)
    end_time = db.Column(db.String)


class Teacher(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    classes = db.relationship("classes",backref="teacher")
    dance_types = db.Column(pg.ARRAY(db.Enum(DanceTypes)))


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    dance_classes = db.relationship("dance_classes",
        secondary=classes_through_students_table, backref="participants"
    )

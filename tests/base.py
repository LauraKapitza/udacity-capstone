import unittest


from app import app
from config import db
from models import Teacher, DanceTypes, Student, Class

import random
import string


def get_random_string(length):
    return "".join(random.choice(string.ascii_lowercase) for i in range(length))


def teacher_factory(teacher_id=None, first_name=None, last_name=None, dance_types=None):
    data = {}
    data["id"] = teacher_id or f"auth0|teacher-{get_random_string(4)}"
    data["first_name"] = first_name or "Batman"
    data["last_name"] = last_name or "Wayne"
    data["dance_types"] = dance_types or [DanceTypes.jazz]
    teacher = Teacher(**data)
    teacher.insert()
    print(teacher)
    return teacher


def student_factory(student_id=None, first_name=None, last_name=None):
    data = {}
    data["id"] = student_id or f"auth0|student-{get_random_string(4)}"
    data["first_name"] = first_name or "Robin"
    data["last_name"] = last_name or "Grayson"

    student = Student(**data)
    student.insert()
    return student


def classes_factory(
    teacher_id=None,
    dance_types=None,
    title=None,
    description=None,
    max_participants=None,
    date=None,
    start_time=None,
    end_time=None,
    participants=None,
):
    data = {}
    if not teacher_id:
        s = teacher_factory()
        data["teacher_id"] = s.id
    else:
        data["teacher_id"] = teacher_id
    data["dance_types"] = dance_types or [DanceTypes.jazz]
    data["title"] = title or "Dancing queen"
    data["description"] = description or "Dance"
    data["max_participants"] = max_participants or 10
    data["date"] = date or "2023-03-20"
    data["start_time"] = start_time or "18:00"
    data["end_time"] = end_time or "20:00"
    if not participants:
        data["participants"] = [student_factory()]
    else:
        data["participants"] = participants

    c = Class(**data)
    c.insert()
    return c


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

        # Force the test suite to run inside this app context
        app.app_context().push()

    def tearDown(self):
        # Force the test suite to run inside this app context
        app.app_context().push()

        meta = db.metadata
        for table in reversed(meta.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()

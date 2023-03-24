import json
import unittest
from unittest.mock import patch


from models import Class


from tests.base import BaseTestCase, classes_factory, teacher_factory, student_factory


class TeachersTestCase(BaseTestCase):
    @patch("auth.auth.validate_token_or_raise")
    def test_get_list(self, _mock):
        teacher = teacher_factory()

        res = self.client.get("/teachers")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        self.assertDictEqual(teacher.format_long(), data["teachers"][0])

    @patch("auth.auth.validate_token_or_raise")
    def test_get_detail(self, _mock):
        c = classes_factory()

        res = self.client.get(f"/classes/{c.id}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        self.assertDictEqual(c.format_long(), data["class"])

    @patch("auth.auth.validate_token_or_raise")
    def test_post(self, _mock):
        teacher = teacher_factory()
        # Mock teacher token
        _mock.return_value = {"sub": teacher.id}

        res = self.client.post(
            "/classes",
            json={
                "date": "2023-03-20",
                "description": "I am an amazing dance class",
                "end_time": "20:00",
                "max_participants": 15,
                "start_time": "18:00",
                "title": "Amazing class",
                "dance_types": [teacher.dance_types[0].name],
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        c = Class.query.first()
        self.assertEqual(data["class"]["title"], c.title)

    @patch("auth.auth.validate_token_or_raise")
    def test_patch(self, _mock):
        teacher = teacher_factory()
        # Mock teacher token
        _mock.return_value = {"sub": teacher.id}

        c = classes_factory(teacher_id=teacher.id)

        res = self.client.patch(
            f"/classes/{c.id}",
            json={
                "title": "bat dance",
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        c = Class.query.first()
        self.assertEqual(data["class"]["title"], "bat dance")

    @patch("auth.auth.validate_token_or_raise")
    def test_delete(self, _mock):
        c = classes_factory()

        res = self.client.delete(f"/classes/{c.id}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(Class.query.count(), 0)


if __name__ == "__main__":
    unittest.main()

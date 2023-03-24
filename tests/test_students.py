import json
import unittest
from unittest.mock import patch


from models import Class, DanceTypes, Student

from tests.base import BaseTestCase
from tests.fixtures import student_factory


class StudentsTestCase(BaseTestCase):
    @patch("auth.auth.validate_token_or_raise")
    def test_get_list(self, _mock):
        student = student_factory()

        res = self.client.get("/students")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        self.assertDictEqual(student.format_long(), data["students"][0])

    @patch("auth.auth.validate_token_or_raise")
    def test_get_detail(self, _mock):
        student = student_factory()

        res = self.client.get(f"/students/{student.id}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        self.assertDictEqual(student.format_long(), data["student"])

    @patch("auth.auth.validate_token_or_raise")
    def test_get_detail__404(self, _mock):
        res = self.client.get(f"/students/999")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    @patch("auth.auth.validate_token_or_raise")
    def test_post(self, _mock):
        res = self.client.post(
            "/students",
            json={
                "user_id": "auth0|random-value",
                "first_name": "John",
                "last_name": "Doe",
                "dance_types": [DanceTypes.ballroom.name],
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        student = Student.query.first()
        self.assertEqual(data["student"]["id"], student.id)

    @patch("auth.auth.validate_token_or_raise")
    def test_post__400(self, _mock):
        res = self.client.post(
            "/students",
            json={},
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)

    @patch("auth.auth.validate_token_or_raise")
    def test_patch(self, _mock):
        student = student_factory()
        res = self.client.patch(
            f"/students/{student.id}",
            json={
                "first_name": "batman",
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        c = Class.query.first()
        self.assertEqual(data["student"]["first_name"], "batman")

    @patch("auth.auth.validate_token_or_raise")
    def test_patch__404(self, _mock):
        student = student_factory()

        res = self.client.patch(
            f"/students/999",
            json={
                "first_name": "batman",
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    @patch("auth.auth.validate_token_or_raise")
    def test_delete(self, _mock):
        student = student_factory()

        res = self.client.delete(f"/students/{student.id}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(student.query.count(), 0)

    @patch("auth.auth.validate_token_or_raise")
    def test_delete__404(self, _mock):
        res = self.client.delete("/students/99")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)


if __name__ == "__main__":
    unittest.main()

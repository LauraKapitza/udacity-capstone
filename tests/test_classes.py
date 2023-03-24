import json
import unittest
from unittest.mock import patch


from models import Class


from tests.base import BaseTestCase
from tests.fixtures import classes_factory, teacher_factory, student_factory


class ClassesTestCase(BaseTestCase):
    @patch("auth.auth.validate_token_or_raise")
    def test_get_list(self, _mock):
        c = classes_factory()

        res = self.client.get("/classes")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        self.assertDictEqual(c.format_long(), data["classes"][0])

    @patch("auth.auth.validate_token_or_raise")
    def test_get_detail(self, _mock):
        c = classes_factory()

        res = self.client.get(f"/classes/{c.id}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        self.assertDictEqual(c.format_long(), data["class"])

    @patch("auth.auth.validate_token_or_raise")
    def test_get_detail__404(self, _mock):
        res = self.client.get(f"/classes/999")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

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
    def test_post__400(self, _mock):
        teacher = teacher_factory()
        # Mock teacher token
        _mock.return_value = {"sub": teacher.id}

        res = self.client.post(
            "/classes",
            json={},
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)

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
    def test_patch__404(self, _mock):
        teacher = teacher_factory()
        # Mock teacher token
        _mock.return_value = {"sub": teacher.id}

        res = self.client.patch(
            "/classes/999",
            json={
                "title": "bat dance",
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    @patch("auth.auth.validate_token_or_raise")
    def test_delete(self, _mock):
        c = classes_factory()

        res = self.client.delete(f"/classes/{c.id}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(Class.query.count(), 0)

    @patch("auth.auth.validate_token_or_raise")
    def test_delete__404(self, _mock):
        res = self.client.delete("/classes/99")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    @patch("auth.auth.validate_token_or_raise")
    def test_post_add_participant(self, _mock):
        student = student_factory()
        # Mock student token
        _mock.return_value = {"sub": student.id}

        c = classes_factory(participants=[])

        res = self.client.post(
            f"/classes/{c.id}/participants",
            json={},
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        c = Class.query.first()
        self.assertEqual(c.participants[0], student)
        self.assertEqual(data["added_participant"], student.format_short())

    @patch("auth.auth.validate_token_or_raise")
    def test_post_add_participant__maximum(self, _mock):
        student = student_factory()
        # Mock student token
        _mock.return_value = {"sub": student.id}

        c = classes_factory(
            participants=[student_factory(), student_factory()],
            max_participants=2,
        )

        res = self.client.post(
            f"/classes/{c.id}/participants",
            json={},
        )
        self.assertEqual(res.status_code, 400)

    @patch("auth.auth.validate_token_or_raise")
    def test_post_remove_participant(self, _mock):
        student = student_factory()
        # Mock student token
        _mock.return_value = {"sub": student.id}

        c = classes_factory(participants=[student])

        res = self.client.delete(
            f"/classes/{c.id}/participants",
            json={},
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        c = Class.query.first()
        self.assertEqual(len(c.participants), 0)
        self.assertEqual(data["removed_participant"], student.format_short())

    @patch("auth.auth.validate_token_or_raise")
    def test_post_remove_participant__student_not_participant(self, _mock):
        student = student_factory()
        # Mock student token
        _mock.return_value = {"sub": student.id}

        c = classes_factory(participants=[])

        res = self.client.delete(
            f"/classes/{c.id}/participants",
            json={},
        )
        self.assertEqual(res.status_code, 400)


if __name__ == "__main__":
    unittest.main()

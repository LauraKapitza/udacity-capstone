import json
import unittest
from unittest.mock import patch


from models import Class, DanceTypes, Teacher

from tests.base import BaseTestCase
from tests.fixtures import teacher_factory


class TeachersTestCase(BaseTestCase):
    @patch("auth.auth.validate_token_or_raise")
    def test_me(self, _mock):
        teacher = teacher_factory()
        # Mock teacher token
        _mock.return_value = {"sub": teacher.id}

        res = self.client.get("/me")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        self.assertDictEqual(teacher.format_long(), data["me"])

    @patch("auth.auth.validate_token_or_raise")
    def test_me__404(self, _mock):
        # Mock teacher token
        _mock.return_value = {"sub": "not_found"}

        res = self.client.get("/me")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

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
        teacher = teacher_factory()

        res = self.client.get(f"/teachers/{teacher.id}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        self.assertDictEqual(teacher.format_long(), data["teacher"])

    @patch("auth.auth.validate_token_or_raise")
    def test_get_detail__404(self, _mock):
        res = self.client.get(f"/teachers/999")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    @patch("auth.auth.validate_token_or_raise")
    def test_post(self, _mock):
        res = self.client.post(
            "/teachers",
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
        teacher = Teacher.query.first()
        self.assertEqual(data["teacher"]["id"], teacher.id)

    @patch("auth.auth.validate_token_or_raise")
    def test_post__400(self, _mock):
        res = self.client.post(
            "/teachers",
            json={},
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)

    @patch("auth.auth.validate_token_or_raise")
    def test_patch(self, _mock):
        teacher = teacher_factory()
        res = self.client.patch(
            f"/teachers/{teacher.id}",
            json={
                "first_name": "batman",
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        c = Class.query.first()
        self.assertEqual(data["teacher"]["first_name"], "batman")

    @patch("auth.auth.validate_token_or_raise")
    def test_patch__404(self, _mock):
        teacher = teacher_factory()

        res = self.client.patch(
            f"/teachers/999",
            json={
                "first_name": "batman",
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    @patch("auth.auth.validate_token_or_raise")
    def test_delete(self, _mock):
        teacher = teacher_factory()

        res = self.client.delete(f"/teachers/{teacher.id}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(Teacher.query.count(), 0)

    @patch("auth.auth.validate_token_or_raise")
    def test_delete__404(self, _mock):
        res = self.client.delete("/teachers/99")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)


if __name__ == "__main__":
    unittest.main()

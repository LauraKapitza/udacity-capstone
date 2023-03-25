import json
import unittest
from unittest.mock import patch


from models import Class, DanceTypes, Student

from tests.base import BaseTestCase
from tests.fixtures import student_factory


class RBACTestCase(BaseTestCase):
    @patch("auth.auth.extract_token_or_raise")
    def test_role_student__valid(self, _mock):
        _mock.return_value = {
            "permissions": [
                "classes:join",
                "classes:read",
                "students:read",
                "teachers:read",
            ]
        }

        res = self.client.get("/me")
        self.assertNotEqual(res.status_code, 403)

        res = self.client.get("/students")
        self.assertNotEqual(res.status_code, 403)

        res = self.client.get("/students/1")
        self.assertNotEqual(res.status_code, 403)

        res = self.client.get("/classes")
        self.assertNotEqual(res.status_code, 403)

        res = self.client.get("/classes/1")
        self.assertNotEqual(res.status_code, 403)

        res = self.client.post("/classes/1/participants")
        self.assertNotEqual(res.status_code, 403)

        res = self.client.delete("/classes/1/participants")
        self.assertNotEqual(res.status_code, 403)

    @patch("auth.auth.extract_token_or_raise")
    def test_role_student__forbidden(self, _mock):
        _mock.return_value = {
            "permissions": [
                "classes:join",
                "classes:read",
                "students:read",
                "teachers:read",
            ]
        }

        res = self.client.post("/students")
        self.assertEqual(res.status_code, 403)

        res = self.client.delete("/students/1")
        self.assertEqual(res.status_code, 403)

        res = self.client.patch("/students/1")
        self.assertEqual(res.status_code, 403)

        res = self.client.post("/teachers")
        self.assertEqual(res.status_code, 403)

        res = self.client.delete("/teachers/1")
        self.assertEqual(res.status_code, 403)

        res = self.client.patch("/teachers/1")
        self.assertEqual(res.status_code, 403)

        res = self.client.post("/classes")
        self.assertEqual(res.status_code, 403)

        res = self.client.delete("/classes/1")
        self.assertEqual(res.status_code, 403)

        res = self.client.patch("/classes/1")
        self.assertEqual(res.status_code, 403)

    @patch("auth.auth.extract_token_or_raise")
    def test_role_teacher__valid(self, _mock):
        _mock.return_value = {
            "permissions": [
                "classes:create",
                "classes:delete",
                "classes:read",
                "classes:update",
                "students:read",
                "teachers:read",
                "teachers:update",
            ]
        }

        res = self.client.get("/me")
        self.assertNotEqual(res.status_code, 403)

        res = self.client.get("/students")
        self.assertNotEqual(res.status_code, 403)

        res = self.client.get("/students/1")
        self.assertNotEqual(res.status_code, 403)

        res = self.client.get("/teachers")
        self.assertNotEqual(res.status_code, 403)

        res = self.client.get("/teachers/1")
        self.assertNotEqual(res.status_code, 403)

        res = self.client.patch("/teachers/1")
        self.assertNotEqual(res.status_code, 403)

        res = self.client.get("/classes")
        self.assertNotEqual(res.status_code, 403)

        res = self.client.get("/classes/1")
        self.assertNotEqual(res.status_code, 403)

        res = self.client.post("/classes")
        self.assertNotEqual(res.status_code, 403)

        res = self.client.patch("/classes/1")
        self.assertNotEqual(res.status_code, 403)

        res = self.client.delete("/delete/1")
        self.assertNotEqual(res.status_code, 403)

    @patch("auth.auth.extract_token_or_raise")
    def test_role_teacher__forbidden(self, _mock):
        _mock.return_value = {
            "permissions": [
                "classes:create",
                "classes:delete",
                "classes:read",
                "classes:update",
                "students:read",
                "teachers:read",
                "teachers:update",
            ]
        }

        res = self.client.post("/students")
        self.assertEqual(res.status_code, 403)

        res = self.client.delete("/students/1")
        self.assertEqual(res.status_code, 403)

        res = self.client.patch("/students/1")
        self.assertEqual(res.status_code, 403)

        res = self.client.post("/teachers")
        self.assertEqual(res.status_code, 403)

    @patch("auth.auth.extract_token_or_raise")
    def test_role_manager__valid(self, _mock):
        _mock.return_value = {
            "permissions": [
                "classes:create",
                "classes:delete",
                "classes:join",
                "classes:read",
                "classes:update",
                "students:create",
                "students:delete",
                "students:read",
                "students:update",
                "teachers:create",
                "teachers:delete",
                "teachers:read",
                "teachers:update",
            ]
        }

        res = self.client.get("/students")
        self.assertNotEqual(res.status_code, 403)

        res = self.client.get("/students/1")
        self.assertNotEqual(res.status_code, 403)

        res = self.client.post("/students/1")
        self.assertNotEqual(res.status_code, 403)

        res = self.client.patch("/students/1")
        self.assertNotEqual(res.status_code, 403)

        res = self.client.delete("/students/1")
        self.assertNotEqual(res.status_code, 403)

        res = self.client.get("/teachers")
        self.assertNotEqual(res.status_code, 403)

        res = self.client.get("/teachers/1")
        self.assertNotEqual(res.status_code, 403)

        res = self.client.patch("/teachers/1")
        self.assertNotEqual(res.status_code, 403)

        res = self.client.delete("/teachers/1")
        self.assertNotEqual(res.status_code, 403)

        res = self.client.get("/classes")
        self.assertNotEqual(res.status_code, 403)

        res = self.client.get("/classes/1")
        self.assertNotEqual(res.status_code, 403)

        res = self.client.post("/classes")
        self.assertNotEqual(res.status_code, 403)

        res = self.client.delete("/classes")
        self.assertNotEqual(res.status_code, 403)

        res = self.client.patch("/classes/1")
        self.assertNotEqual(res.status_code, 403)

        res = self.client.delete("/classes/1")
        self.assertNotEqual(res.status_code, 403)

        res = self.client.post("/classes/1/participants")
        self.assertNotEqual(res.status_code, 403)

        res = self.client.delete("/classes/1/participants")
        self.assertNotEqual(res.status_code, 403)


if __name__ == "__main__":
    unittest.main()

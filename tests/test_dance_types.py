import json
import unittest

from models import DanceTypes
from tests.base import BaseTestCase


class DanceTypesTestCase(BaseTestCase):
    def test_get_get_dance_types(self):
        res = self.client.get("/dance-types")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        dance_types = [type.format() for type in DanceTypes]
        self.assertEqual(data["dance_types"], dance_types)
        self.assertEqual(data["total_dance_types"], len(dance_types))


if __name__ == "__main__":
    unittest.main()

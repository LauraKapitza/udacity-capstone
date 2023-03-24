import unittest


from app import app
from config import db


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

        # Force the test suite to run inside this app context
        app.app_context().push()

    def tearDown(self):
        meta = db.metadata
        for table in reversed(meta.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()

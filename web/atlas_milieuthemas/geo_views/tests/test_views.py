from django.db import connection

from django.test import TestCase


class ViewsTest(TestCase):
    def get_row(self, view_name):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM " + str(view_name) + " LIMIT 1")
        result = cursor.fetchone()
        self.assertIsNotNone(result)

        return dict(zip([col[0] for col in cursor.description], result))

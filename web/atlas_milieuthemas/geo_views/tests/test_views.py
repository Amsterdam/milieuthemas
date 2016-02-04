from django.db import connection

from django.test import TestCase

from datasets.schiphol.tests import factories as schiphol_factories


class ViewsTest(TestCase):
    def get_row(self, view_name):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM " + str(view_name) + " LIMIT 1")
        result = cursor.fetchone()
        self.assertIsNotNone(result)

        return dict(zip([col[0] for col in cursor.description], result))

    def test_schiphol_hoogte_point(self):
        l = schiphol_factories.HoogtebeperkendeVlakkenPointFactory.create()
        row = self.get_row('geo_schiphol_hoogte_point_layer')
        self.assertEqual(row['id'], l.id)
        self.assertNotEqual(row['geometrie'], None)

    def test_schiphol_hoogte_line(self):
        l = schiphol_factories.HoogtebeperkendeVlakkenLineFactory.create()
        row = self.get_row('geo_schiphol_hoogte_line_layer')
        self.assertEqual(row['id'], l.id)
        self.assertNotEqual(row['geometrie'], None)

    def test_schiphol_hoogte_poly(self):
        l = schiphol_factories.HoogtebeperkendeVlakkenPolyFactory.create()
        row = self.get_row('geo_schiphol_hoogte_polygon_layer')
        self.assertEqual(row['id'], l.id)
        self.assertNotEqual(row['geometrie'], None)

    def test_schiphol_geluid(self):
        l = schiphol_factories.GeluidzoneFactory.create()
        row = self.get_row('geo_schiphol_geluidzone')
        self.assertEqual(row['id'], l.id)
        self.assertNotEqual(row['geometrie'], None)

from unittest import skip
from django.db import connection

from django.test import TestCase

from datasets.schiphol.tests import factories as schiphol_factories
from datasets.bodeminformatie.tests import factories as bodeminformatie_factories
from datasets.veiligheidsafstanden.tests import factories as veiligheidsafstanden_factories
from datasets.risicozones_bedrijven.tests import factories as risicozones_bedrijven_factories


class ViewsTest(TestCase):
    def get_row(self, view_name):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM " + str(view_name) + " LIMIT 1")
        result = cursor.fetchone()
        self.assertIsNotNone(result)

        return dict(zip([col[0] for col in cursor.description], result))

    # schiphol
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

    def test_schiphol_vogel(self):
        l = schiphol_factories.VogelvrijwaringsgebiedFactory.create()
        row = self.get_row('geo_schiphol_vogelvrijwaringsgebied')
        self.assertEqual(row['id'], l.id)
        self.assertNotEqual(row['geometrie'], None)

    # bodeminformatie
    def test_bodeminformatie_grondmonster(self):
        l = bodeminformatie_factories.GrondmonsterFactory.create()
        row = self.get_row('geo_bodeminformatie_grondmonster')
        self.assertEqual(row['id'], l.id)
        self.assertNotEqual(row['eindoordeel'], None)
        self.assertNotEqual(row['geometrie'], None)

    def test_bodeminformatie_grondwatermonster(self):
        l = bodeminformatie_factories.GrondwatermonsterFactory.create()
        row = self.get_row('geo_bodeminformatie_grondwatermonster')
        self.assertEqual(row['id'], l.id)
        self.assertNotEqual(row['eindoordeel'], None)
        self.assertNotEqual(row['geometrie'], None)

    def test_bodeminformatie_asbest(self):
        l = bodeminformatie_factories.AsbestFactory.create()
        row = self.get_row('geo_bodeminformatie_asbest')
        self.assertEqual(row['id'], l.id)
        self.assertNotEqual(row['concentratie'], None)
        self.assertNotEqual(row['geometrie'], None)

    # veiligheidsafstanden
    def test_veiligheidsafstanden_point(self):
        l = veiligheidsafstanden_factories.VeiligheidsafstandPointFactory.create()
        row = self.get_row('geo_veiligheidsafstanden_point_layer')
        self.assertEqual(row['id'], l.id)
        self.assertNotEqual(row['type'], None)
        self.assertNotEqual(row['locatie'], None)
        self.assertNotEqual(row['geometrie'], None)

    def test_veiligheidsafstanden_polygon(self):
        l = veiligheidsafstanden_factories.VeiligheidsafstandPolygonFactory.create()
        row = self.get_row('geo_veiligheidsafstanden_polygon_layer')
        self.assertEqual(row['id'], l.id)
        self.assertNotEqual(row['type'], None)
        self.assertNotEqual(row['locatie'], None)
        self.assertNotEqual(row['geometrie'], None)

    # risicozones_bedrijven
    def test_risicozones_bedrijven_lpgstation_point_layer(self):
        l = risicozones_bedrijven_factories.LPGStationPointFactory.create()
        row = self.get_row('geo_risicozones_bedrijven_lpgstation_point_layer')
        self.assertEqual(row['id'], l.id)
        self.assertNotEqual(row['bedrijfsnaam'], None)
        self.assertNotEqual(row['dossiernummer'], None)
        self.assertNotEqual(row['geometrie'], None)

    def test_risicozones_bedrijven_lpgstation_polygon_layer(self):
        l = risicozones_bedrijven_factories.LPGStationPolygonFactory.create()
        row = self.get_row('geo_risicozones_bedrijven_lpgstation_polygon_layer')
        self.assertEqual(row['id'], l.id)
        self.assertNotEqual(row['bedrijfsnaam'], None)
        self.assertNotEqual(row['dossiernummer'], None)
        self.assertNotEqual(row['geometrie'], None)

    def test_risicozones_bedrijven_lpgvulpunt_point_layer(self):
        l = risicozones_bedrijven_factories.LPGVulpuntPointFactory.create()
        row = self.get_row('geo_risicozones_bedrijven_lpgvulpunt_point_layer')
        self.assertEqual(row['id'], l.id)
        self.assertNotEqual(row['type'], None)
        self.assertNotEqual(row['afstandseis'], None)
        self.assertNotEqual(row['voldoet'], None)
        self.assertNotEqual(row['geometrie'], None)

    def test_risicozones_bedrijven_lpgvulpunt_polygon_layer(self):
        l = risicozones_bedrijven_factories.LPGVulpuntPolygonFactory.create()
        row = self.get_row('geo_risicozones_bedrijven_lpgvulpunt_polygon_layer')
        self.assertEqual(row['id'], l.id)
        self.assertNotEqual(row['type'], None)
        self.assertNotEqual(row['afstandseis'], None)
        self.assertNotEqual(row['voldoet'], None)
        self.assertNotEqual(row['geometrie'], None)

    def test_risicozones_bedrijven_lpgtank(self):
        l = risicozones_bedrijven_factories.LPGTankFactory.create()
        row = self.get_row('geo_risicozones_bedrijven_lpgtank')
        self.assertEqual(row['id'], l.id)
        self.assertNotEqual(row['type'], None)
        self.assertNotEqual(row['afstandseis'], None)
        self.assertNotEqual(row['voldoet'], None)
        self.assertNotEqual(row['geometrie'], None)

    def test_risicozones_bedrijven_lpgafleverzuil_point_layer(self):
        l = risicozones_bedrijven_factories.LPGAfleverzuilPointFactory.create()
        row = self.get_row('geo_risicozones_bedrijven_lpgafleverzuil_point_layer')
        self.assertEqual(row['id'], l.id)
        self.assertNotEqual(row['station_id'], None)
        self.assertNotEqual(row['geometrie'], None)

    def test_risicozones_bedrijven_lpgafleverzuil_polygon_layer(self):
        l = risicozones_bedrijven_factories.LPGAfleverzuilPolygonFactory.create()
        row = self.get_row('geo_risicozones_bedrijven_lpgafleverzuil_polygon_layer')
        self.assertEqual(row['id'], l.id)
        self.assertNotEqual(row['station_id'], None)
        self.assertNotEqual(row['geometrie'], None)

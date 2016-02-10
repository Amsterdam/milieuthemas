from datapunt_generic.batch.test import TaskTestCase
from .. import batch, models

from datasets.themas.tests.factories import ThemaFactory


class ImportLPGVulpuntTest(TaskTestCase):
    def setUp(self):
        ThemaFactory.create(pk=6)

    def task(self):
        return batch.ImportLPGVulpuntTask()

    def test_import(self):
        self.run_task()

        imported = models.LPGVulpunt.objects.all()
        self.assertEqual(len(imported), 2)

        vulpunt = models.LPGVulpunt.objects.get(geo_id=2)
        self.assertEqual(vulpunt.type, 'Vulpunt')
        self.assertNotEqual(vulpunt.geometrie_point, None)
        self.assertEqual(vulpunt.geometrie_polygon, None)

        vulpunt = models.LPGVulpunt.objects.get(geo_id=69)
        self.assertEqual(vulpunt.type, 'Plaatsgebonden risico 10-5')
        self.assertEqual(vulpunt.geometrie_point, None)
        self.assertNotEqual(vulpunt.geometrie_polygon, None)

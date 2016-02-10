from datapunt_generic.batch.test import TaskTestCase
from .. import batch, models

from datasets.themas.tests.factories import ThemaFactory


class ImportVeiligheidsafstandenTest(TaskTestCase):
    def setUp(self):
        ThemaFactory.create(pk=3)
        ThemaFactory.create(pk=4)
        ThemaFactory.create(pk=5)
        ThemaFactory.create(pk=8)

    def task(self):
        return batch.ImportVeiligheidsafstandenTask()

    def test_import(self):
        self.run_task()

        imported = models.Veiligheidsafstand.objects.all()
        self.assertEqual(len(imported), 2)

        afstand = models.Veiligheidsafstand.objects.get(geo_id=60)
        self.assertEqual(afstand.locatie, 'Spaarndammerstraat 135-137')
        self.assertNotEqual(afstand.geometrie_point, None)
        self.assertEqual(afstand.geometrie_multipolygon, None)

        afstand = models.Veiligheidsafstand.objects.get(geo_id=57)
        self.assertEqual(afstand.locatie, 'Monding ARK')
        self.assertEqual(afstand.geometrie_point, None)
        self.assertNotEqual(afstand.geometrie_multipolygon, None)

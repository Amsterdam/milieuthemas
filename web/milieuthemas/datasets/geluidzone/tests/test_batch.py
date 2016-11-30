from datapunt_generic.batch.test import TaskTestCase
from .. import batch, models

from datasets.themas.tests.factories import ThemaFactory


class ImportGeluidzoneTest(TaskTestCase):
    def setUp(self):
        ThemaFactory.create(pk=1)
        ThemaFactory.create(pk=10)

    def task(self):
        return batch.ImportGeluidzoneTask()

    def test_import(self):
        self.run_task()

        spoorwegen = models.Spoorwegen.objects.all()
        self.assertEqual(len(spoorwegen), 1)

        model = models.Spoorwegen.objects.get(geo_id=12)
        self.assertEqual(model.type, 'Geluidszone spoorwegen')
        self.assertNotEqual(model.geometrie, None)

        metro = models.Metro.objects.all()
        self.assertEqual(len(metro), 1)

        model = models.Metro.objects.get(geo_id=11)
        self.assertEqual(model.type, 'Geluidszone metro')
        self.assertNotEqual(model.geometrie, None)

        industrie = models.Industrie.objects.all()
        self.assertEqual(len(industrie), 1)

        model = models.Industrie.objects.get(geo_id=25)
        self.assertEqual(model.naam, 'AMC Zuidoost')
        self.assertNotEqual(model.geometrie, None)

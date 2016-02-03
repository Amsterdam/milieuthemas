from datapunt_generic.batch.test import TaskTestCase
from .. import batch, models

from datasets.themas.tests.factories import ThemaFactory


NAP = 'diva/milieuthemas'


class ImportMeetboutenTest(TaskTestCase):
    def task(self):
        return batch.ImportHoogtebeperkendeVlakkenTask(NAP)

    def test_import(self):
        ThemaFactory.create(pk=6)

        self.run_task()

        imported = models.HoogtebeperkendeVlakken.objects.all()
        self.assertEqual(len(imported), 20)

        vlak = models.HoogtebeperkendeVlakken.objects.get(geo_id=16)
        self.assertEqual(vlak.bouwhoogte, '1.5-2.0')

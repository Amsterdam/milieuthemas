from datapunt_generic.batch.test import TaskTestCase
from .. import batch, models


class ImportGrondmonsterTest(TaskTestCase):
    def setUp(self):
        pass

    def task(self):
        return batch.ImportGrondmonster()

    def test_import(self):
        self.run_task()

        imported = models.Grondmonster.objects.all()
        self.assertEqual(len(imported), 9)

        monster = models.Grondmonster.objects.get(geo_id=41)
        self.assertEqual(monster.rapportnummer, '24030974')
        self.assertNotEqual(monster.geometrie, None)



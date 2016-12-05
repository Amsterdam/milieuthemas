from datapunt_generic.batch.test import TaskTestCase
from .. import batch, models


class ImportBomInslagTest(TaskTestCase):

    def setUp(self):
        pass

    def task(self):
        return batch.ImportInslagenTask(path='bommenkaart/csv/')

    def test_import(self):
        self.run_task()

        imported = models.BomInslag.objects.all()
        self.assertEqual(len(imported), 27)

        monster = models.BomInslag.objects.get(kenmerk='KR_430722001')
        self.assertNotEqual(monster.geometrie_point, None)


class GevrijwaardGebiedTest(TaskTestCase):

    def setUp(self):
        pass

    def task(self):
        return batch.ImportGevrijwaardTask(path='bommenkaart/csv/')

    def test_import(self):
        self.run_task()

        imported = models.GevrijwaardGebied.objects.all()
        self.assertEqual(len(imported), 19)

        monster = models.GevrijwaardGebied.objects.get(kenmerk='GG_014')
        # self.assertEqual(monster.rapportnummer, '24030974')
        self.assertNotEqual(monster.geometrie_polygon, None)

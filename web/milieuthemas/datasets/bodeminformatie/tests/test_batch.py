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


class ImportGrondwatermonsterTest(TaskTestCase):
    def setUp(self):
        pass

    def task(self):
        return batch.ImportGrondwatermonster()

    def test_import(self):
        self.run_task()

        imported = models.Grondwatermonster.objects.all()
        self.assertEqual(len(imported), 14)

        monster = models.Grondwatermonster.objects.get(geo_id=34)
        self.assertEqual(monster.rapportnummer, '24029542')
        self.assertNotEqual(monster.geometrie, None)


class ImportAsbestTest(TaskTestCase):
    def setUp(self):
        pass

    def task(self):
        return batch.ImportAsbest()

    def test_import(self):
        self.run_task()

        imported = models.Asbest.objects.all()
        self.assertEqual(len(imported), 9)

        monster = models.Asbest.objects.get(geo_id=54)
        self.assertEqual(monster.locatie, 'WCW-terrein 2')
        self.assertNotEqual(monster.geometrie, None)



from datapunt_generic.batch.test import TaskTestCase
from .. import batch, models


TEST_INSLAGEN_PATH = 'Inslagen_ea_test.shp'
TEST_VERDACHTE_GEBIEDEN_PATH = 'Verdachte_gebieden_test.shp'
TEST_UITGEVOERD_ONDERZOEK_PATH = 'Reeds_uitgevoerde_CE_onderzoeken_test.shp'
TEST_GEVRIJWAARD_GEBIED_PATH = 'Gevrijwaard_gebied_test.shp'


class ImportBomInslagTest(TaskTestCase):

    def setUp(self):
        pass

    def task(self):
        return batch.ImportInslagenTask(path=TEST_INSLAGEN_PATH)

    def test_import(self):
        self.run_task()

        imported = models.BomInslag.objects.all()
        self.assertEqual(len(imported), 5)

        inslag = models.BomInslag.objects.get(kenmerk='A003_002')
        self.assertNotEqual(inslag.geometrie_point, None)


class ImportGevrijwaardGebiedTest(TaskTestCase):

    def setUp(self):
        pass

    def task(self):
        return batch.ImportGevrijwaardTask(path=TEST_GEVRIJWAARD_GEBIED_PATH)

    def test_import(self):
        self.run_task()

        imported = models.GevrijwaardGebied.objects.all()

        self.assertEqual(len(imported), 1)

        gebied = models.GevrijwaardGebied.objects.get(kenmerk='GG_004')

        self.assertNotEqual(gebied.geometrie_polygon, None)


class ImportVerdachtGebiedTest(TaskTestCase):

    def setUp(self):
        pass

    def task(self):
        return batch.ImportVerdachtGebiedTask(path=TEST_VERDACHTE_GEBIEDEN_PATH)

    def test_import(self):
        self.run_task()

        imported = models.VerdachtGebied.objects.all()
        self.assertEqual(len(imported), 6)

        gebieden = models.VerdachtGebied.objects.filter(
            kenmerk='A003')

        self.assertNotEqual(gebieden[0].geometrie_polygon, None)


class ImportOnderzochtGebiedTest(TaskTestCase):

    def setUp(self):
        pass

    def task(self):
        return batch.ImportUitgevoerdOnderzoekTask(path=TEST_UITGEVOERD_ONDERZOEK_PATH)

    def test_import(self):
        self.run_task()

        imported = models.UitgevoerdOnderzoek.objects.all()
        self.assertEqual(len(imported), 1)

        gebied = models.UitgevoerdOnderzoek.objects.get(
            kenmerk='72491-AR-08')

        self.assertNotEqual(gebied.geometrie_polygon, None)

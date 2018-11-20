from datapunt_generic.batch.test import TaskTestCase
from datasets.bommenkaart.batch import TEST_INSLAGEN_PATH, TEST_GEVRIJWAARD_GEBIED_PATH, TEST_VERDACHTE_GEBIEDEN_PATH, \
    TEST_UITGEVOERD_ONDERZOEK_PATH
from .. import batch, models


class ImportBomInslagTest(TaskTestCase):

    def setUp(self):
        pass

    def task(self):
        return batch.ImportInslagenTask(path=TEST_INSLAGEN_PATH)

    def test_import(self):
        self.run_task()

        imported = models.BomInslag.objects.all()
        self.assertEqual(len(imported), 27)

        inslag = models.BomInslag.objects.get(kenmerk='KR_430722001')
        self.assertNotEqual(inslag.geometrie_point, None)


class ImportGevrijwaardGebiedTest(TaskTestCase):

    def setUp(self):
        pass

    def task(self):
        return batch.ImportGevrijwaardTask(path=TEST_GEVRIJWAARD_GEBIED_PATH)

    def test_import(self):
        self.run_task()

        imported = models.GevrijwaardGebied.objects.all()

        self.assertEqual(len(imported), 19)

        gebied = models.GevrijwaardGebied.objects.get(kenmerk='GG_014')

        self.assertNotEqual(gebied.geometrie_polygon, None)


class ImportVerdachtGebiedTest(TaskTestCase):

    def setUp(self):
        pass

    def task(self):
        return batch.ImportVerdachtGebiedTask(path=TEST_VERDACHTE_GEBIEDEN_PATH)

    def test_import(self):
        self.run_task()

        imported = models.VerdachtGebied.objects.all()
        self.assertEqual(len(imported), 4)

        gebied = models.VerdachtGebied.objects.get(
            kenmerk='VGA_400630B')

        self.assertNotEqual(gebied.geometrie_polygon, None)


class ImportOnderzochtGebiedTest(TaskTestCase):

    def setUp(self):
        pass

    def task(self):
        return batch.ImportUitgevoerdOnderzoekTask(path=TEST_UITGEVOERD_ONDERZOEK_PATH)

    def test_import(self):
        self.run_task()

        imported = models.UitgevoerdOnderzoek.objects.all()
        self.assertEqual(len(imported), 9)

        gebied = models.UitgevoerdOnderzoek.objects.get(
            kenmerk='35279')

        self.assertNotEqual(gebied.geometrie_polygon, None)

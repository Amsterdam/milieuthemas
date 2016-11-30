# Project
from datapunt_generic.batch.test import TaskTestCase
from .. import batch, models


class ImportAardgasleidingTest(object):
    def task(self):
        return batch.ImportAardgasleidingTask()

    def test_import(self):
        self.run_task()

        imported = models.Aardgasleiding.objects.count()
        self.assertEqual(9, imported)
        
        entry = models.Aardgasleiding.objects.get(pk=3)
        assertNotEqual(entry.geometrie, None)


class ImportImportAardgasGebiedTest(object):
    def task(self):
        return batch.ImportAardgasGebiedTask()

    def test_import(self):
        self.run_task()

        # Checking result per type
        results = (('la', 1), ('l1', 1), ('pr', 11), ('zk', 4))
        for res in result:
            imported = models.AardgasGebied.objects.filter(type=res[0]).count()
            assertEqual(imported, res[1])


class ImportInfrastructuurTestBase(object):
    """
    Base infrastructuur test class
    
    Sub class must define:
    task_name - the task to run
    infrastructuur_type - the two letter code for the type
    exp_count - the expected count
    geos_val - the geod field expected to have a value
    """
    def task(self):
        return self.task_name()

    def test_import(self):
        self.run_task()

        imported = models.Infrastructuur.objects.filter(type=self.infrastructuur_type).count()
        self.assertEqual(self.exp_count, imported)

        entry = models.Infrastructuur.objects.filter(type=self.infrastructuur_type).first()
        self.assertNotEqual(getattr(entry, self.geos_val, None), None)


class ImportSpoorwegTest(ImportInfrastructuurTestBase, TaskTestCase):
    task_name = batch.ImportSpoorwegTask
    infrastructuur_type = 'sw'
    exp_count = 1
    geos_val = 'geometrie'


class ImportVaarpwegTest(ImportInfrastructuurTestBase, TaskTestCase):
    task_name = batch.ImportVaarwegTask
    infrastructuur_type = 'vw'
    exp_count = 1
    geos_val = 'geometrie'


class ImportWegTest(ImportInfrastructuurTestBase, TaskTestCase):
    task_name = batch.ImportWegTask
    infrastructuur_type = 'wg'
    exp_count = 1
    geos_val = 'geometrie'

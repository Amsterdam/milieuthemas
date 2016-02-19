# Project
from datapunt_generic.batch.test import TaskTestCase
from .. import batch, models


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
    
    
class ImportAardgasbuisleidingTest(ImportInfrastructuurTestBase, TaskTestCase):
    task_name = batch.ImportAardgasbuisleidingTask
    infrastructuur_type = 'ag'
    exp_count = 9
    geos_val = 'geometrie_line'


class ImportSpoorwegTest(ImportInfrastructuurTestBase, TaskTestCase):
    task_name = batch.ImportSpoorwegTask
    infrastructuur_type = 'sw'
    exp_count = 1
    geos_val = 'geometrie_polygon'


class ImportVaarpwegTest(ImportInfrastructuurTestBase, TaskTestCase):
    task_name = batch.ImportVaarwegTask
    infrastructuur_type = 'vw'
    exp_count = 1
    geos_val = 'geometrie_polygon'


class ImportWegTest(ImportInfrastructuurTestBase, TaskTestCase):
    task_name = batch.ImportWegTask
    infrastructuur_type = 'wg'
    exp_count = 1
    geos_val = 'geometrie_polygon'

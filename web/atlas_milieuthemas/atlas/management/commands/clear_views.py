from django.core.management import BaseCommand
from django.db import connection


class Command(BaseCommand):

    def handle(self, *args, **options):
        cursor = connection.cursor()
        tables = connection.introspection.get_table_list(cursor)
        removed = 0

        for table_info in tables:
            if table_info.type == 'v':
                cursor.execute("DROP VIEW IF EXISTS {}".format(table_info.name))
                removed += 1

        print('removed {} views'.format(removed))

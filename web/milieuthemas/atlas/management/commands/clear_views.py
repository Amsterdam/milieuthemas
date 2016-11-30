from django.core.management import BaseCommand
from django.db import connection

from .sync_views import GEO_VIEW_PREFIX


class Command(BaseCommand):

    def handle(self, *args, **options):
        cursor = connection.cursor()
        tables = connection.introspection.get_table_list(cursor)
        removed = 0

        for table_info in tables:
            if table_info.type == 'v' and table_info.name[0:4] == GEO_VIEW_PREFIX:
                cursor.execute("DROP VIEW {}".format(table_info.name))
                removed += 1

        self.stdout.write('removed {} views'.format(removed))

from django.conf import settings
from django.contrib.contenttypes import models
from django.core.management import BaseCommand
from django.db import connection

from datapunt_generic.generic.mixins import ModelViewFieldsMixin

GEO_VIEW_PREFIX = 'geo_'


class Command(BaseCommand):
    views = []

    def handle(self, *args, **options):
        self.fill_views()
        self.sync_views()

    def sync_views(self):
        cursor = connection.cursor()

        for view in self.views:
            cursor.execute("DROP VIEW IF EXISTS {}".format(view['view_name']))
            cursor.execute("CREATE VIEW {} AS {}".format(view['view_name'], view['sql']))

        print('synced {} views'.format(len(self.views)))

    def fill_views(self):
        app_models = models.ContentType.objects.all()

        for app_model in app_models:
            model_class = app_model.model_class()

            if not issubclass(model_class, ModelViewFieldsMixin):
                continue

            model = model_class()

            view_fields = ', '.join(model.get_view_fields())
            model_table = '{}_{}'.format(app_model.app_label, app_model.model)

            for geo_field in model.model_geo_fields:
                view_name = '{}{}_{}'.format(GEO_VIEW_PREFIX, app_model.app_label, app_model.model)

                if 'line' in geo_field:
                    view_name += '_line'
                elif 'polygon' in geo_field:
                    view_name += '_polygon'
                elif 'point' in geo_field:
                    view_name += '_point'
                elif 'raster' in geo_field:
                    view_name += '_raster'

                self.views.append({
                    'view_name': view_name,
                    'sql': 'SELECT %s, %s as geometrie FROM %s WHERE %s IS NOT NULL' % (
                        view_fields,
                        geo_field,
                        model_table,
                        geo_field
                    )
                })

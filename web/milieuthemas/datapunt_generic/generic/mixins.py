# Packages
from django.contrib.gis.db import models as geo
from django.db import models
# Project
from django.conf import settings


class ImportStatusMixin(models.Model):
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class DocumentStatusMixin(models.Model):
    document_mutatie = models.DateField(null=True)
    document_nummer = models.CharField(max_length=20, null=True)

    class Meta:
        abstract = True


class GeldigheidMixin(models.Model):
    begin_geldigheid = models.DateField(null=True)
    einde_geldigheid = models.DateField(null=True)

    class Meta:
        abstract = True


class MutatieGebruikerMixin(models.Model):
    mutatie_gebruiker = models.CharField(max_length=30, null=True)

    class Meta:
        abstract = True


class CodeOmschrijvingMixin(models.Model):
    code = models.CharField(max_length=4, primary_key=True)
    omschrijving = models.CharField(max_length=150, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return "{}: {}".format(self.code, self.omschrijving)


class ModelViewFieldsMixin(object):
    """
    Mixin to be used for creating geo_views.

    Things that still have to be added:

    - easily add exclude fields on model
    - handle models.CharField(choices=())

    searchable:
    - require a `display` field to be present
    """
    _geo_views = None

    geo_fields = [geo.GeometryCollectionField, geo.GeometryField, geo.LineStringField, geo.MultiLineStringField,
                  geo.MultiPointField, geo.MultiPolygonField, geo.PointField, geo.PolygonField, geo.RasterField]

    def get_model_fields(self):
        """
        Returning a list of the fields
        Because Django names a foreign key
        colums with _id, the field name is altered
        to reflect that as we are generating the SQL
        ourselves
        """
        return [f.name if not isinstance(f, models.ForeignKey) else f'{f.name}_id' for f in self._meta.fields]

    def get_geo_classnames(self):
        return [f.__name__ for f in self.geo_fields]

    @property
    def model_geo_fields(self):
        if not self._geo_views:
            geo_classes = self.get_geo_classnames()

            self._geo_views = [f.name for f in self._meta.fields if f.__class__.__name__ in geo_classes]

        return self._geo_views

    def get_view_fields(self):
        exclude = list(set(getattr(self, 'geo_view_exclude', ['date_modified']) + self.model_geo_fields))
        include = getattr(self, 'geo_view_include', [])

        return list(set(include + [fld for fld in self.get_model_fields() if fld not in exclude]))

    @property
    def model_display_field(self) -> str:
        """
        Specify a display field for the view
        If the model has a display_field set, it is
        added to the view as the 'display'. If not
        an empty string is returnd. This makes it safe
        to include this in every query
        """
        try:
            return f', {self.display_field} as display'
        except AttributeError:
            return ''

    @property
    def uri(self) -> str:
        """
        Generate a url for the model
        If the model has a url_path parameter
        a url will be built and added to the view
        otherwise an empty string is returned
        """
        try:
            return f", '{settings.DATAPUNT_API_URL}{self.url_path}' || id || '/' as uri"
        except AttributeError:
            return ''

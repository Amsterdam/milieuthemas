from django.contrib.gis.db import models as geo
from django.db import models


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

    - handle foreign keys more easy
    - easily add exclude fields on model
    - handle URI field in view
    - handle models.CharField(choices=())
    """
    _geo_views = None

    geo_fields = [geo.GeometryCollectionField, geo.GeometryField, geo.LineStringField, geo.MultiLineStringField,
                  geo.MultiPointField, geo.MultiPolygonField, geo.PointField, geo.PolygonField, geo.RasterField]

    def get_model_fields(self):
        return [f.name for f in self._meta.fields]

    def get_geo_classnames(self):
        return [f.__name__ for f in self.geo_fields]

    @property
    def model_geo_fields(self):
        if not self._geo_views:
            geo_classes = self.get_geo_classnames()

            self._geo_views = [f.name for f in self._meta.fields if f.__class__.__name__ in geo_classes]

        return self._geo_views

    def get_view_fields(self):
        exclude = ['date_modified'] + self.model_geo_fields
        return [fld for fld in self.get_model_fields() if fld not in exclude]


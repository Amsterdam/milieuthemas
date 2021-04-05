Atlas Milieuthema's
====================


## Requirements

* Docker-Compose (required)


## Developing


Use `docker-compose` to start a local database.

	docker-compose up -d


Run migrate to create the needed database tables

    docker-compose exec web python manage.py migrate


Import db data from prod

    docker-compose exec database update-db.sh milieuthemas


The API should now be available on http://localhost:8101/milieuthemas/


Accessing the docker database container for view testing:

	psql -h localhost -p 5402 -U milieuthemas

## Understaing Geoviews

Much of the work in this project is in order to provide geoviews to the map server and the atlas application. In this chapter I will explain how the geoviews are made,
and provide a list of steps needed to add a geoview. The geoviews are used by the map server to generate WMS/WMF data and by the geosearch service
to spatially find data.

### Generating Geoviews
The geoviews are generated using the manage command `sync_views`. This managment commands collects all the models which meet the geoviews criteria (more later) and
generate geoviews for those models. This allows the view to be defiend by the model it is representing, making it very DRY. There are several option to customize the
wat the view is generated. This is mostly done by adding certain parameters to the model. For details refer to the `ModelViewFieldsMixin` class definition.

### Steps in adding a Geoview
To make a geoview out of a django model the following steps are needed:

- Make sure the model subclasses the `ModelViewFieldsMixin` defined in `datapunt_generic.generic.mixins`. Only subclasses of this class will be used in geoview generation.
- If required, add in the model class any fields name you want excluded to the `geo_view_exclude` parameter.
- If A URL is needded in the view add the `url_path` parameter which notes the path part between the domain and the item id
- If a display field is needed ad the `display_field` parameter. The value should be the (string) name of the field to use as source for the display field

The model should now generate the desired geoview

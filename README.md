Atlas Milieuthema's
====================


##Requirements

* Docker-Compose (required)


##Developing


Use `docker-compose` to start a local database.

	(sudo) docker-compose start

or

	docker-compose up


Run migrate to create the needed database tables

    manage.py migrate 


Import db data from prod

    docker-compose exec database update-db.sh milieuthemas


The API should now be available on http://localhost:8000/


Accessing the docker database container for view testing:

	psql -h 192.168.99.100 -p 5402 -U postgres


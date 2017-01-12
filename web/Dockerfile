FROM build.datapunt.amsterdam.nl:5000/atlas/python:latest
MAINTAINER datapunt.ois@amsterdam.nl

ENV PYTHONUNBUFFERED 1
ENV CONSUL_HOST=${CONSUL_HOST:-notset}
ENV CONSUL_PORT=${CONSUL_PORT:-8500}


EXPOSE 8000

RUN apt-get update \
	&& apt-get install -y \
		libgeos-dev \
		gdal-bin \
		netcat \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
	&& adduser --system datapunt \
	&& mkdir -p /static \
	&& chown datapunt /static \
	&& pip install uwsgi

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY milieuthemas /app/

RUN chmod -R 777 /app/data/

USER datapunt
CMD /app/docker-entrypoint.sh

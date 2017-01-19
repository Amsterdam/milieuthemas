FROM datapunt/docker_python:testing
MAINTAINER datapunt.ois@amsterdam.nl

ENV PYTHONUNBUFFERED 1
ENV CONSUL_HOST=${CONSUL_HOST:-notset}
ENV CONSUL_PORT=${CONSUL_PORT:-8500}
ENV DATAPUNT_API_URL=${DATAPUNT_API_URL:-https://api.datapunt.amsterdam.nl/}


EXPOSE 8000

RUN apt-get update \
	&& apt-get install -y \
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

RUN chown -R datapunt /app
RUN chmod +x /app/*.sh

USER datapunt
CMD /app/docker-entrypoint.sh

import os
import re

from django.db import connection

BATCH_SIZE = 50000


def clear_models(*models):
    """
    Truncates the table associated with ``model`` and all related tables.
    """
    for model in models:
        # noinspection PyProtectedMember
        connection.cursor().execute(
            "TRUNCATE {} CASCADE".format(model._meta.db_table))


def clear_model_by_value(model, column, value):
    """
    Clears part of a model based on the value in a given column.

    Important!
    Since this is not truncating the table the pk is not reset.
    """
    # In case of a string encapsulating it in quotes
    if isinstance(value, str):
        value = "'{}'".format(value)
    connection.cursor().execute(
        "DELETE FROM {0} WHERE {0}.{1} = {2}".format(
            model._meta.db_table, column, value
        ))


def get_docker_host():
    """
    Looks for the DOCKER_HOST environment variable to find the VM
    running docker-machine.

    If the environment variable is not found, it is assumed that
    you're running docker on localhost.
    """
    d_host = os.getenv('DOCKER_HOST', None)
    if d_host:
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', d_host):
            return d_host

        return re.match(r'tcp://(.*?):\d+', d_host).group(1)
    return 'localhost'


def in_docker():
    """
    Checks pid 1 cgroup settings to check with reasonable certainty we're in a
    docker env.
    :return: true when running in a docker container, false otherwise
    """
    try:
        return ':/docker/' in open('/proc/1/cgroup', 'r').read()
    except:
        return False

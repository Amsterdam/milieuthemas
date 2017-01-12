#!/usr/bin/env bash

set -u
set -e

# wait for postgres
while ! nc -z database 5401
do
	echo "Waiting for postgres..."
	sleep 2
done

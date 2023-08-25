#!/bin/sh


container_id=$(docker ps -aqf "name=buscamascota_app")
docker cp $container_id:/app/db.sqlite3 /home/roshka/buscamascota/db.sqlite3


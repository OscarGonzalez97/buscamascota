# Gracias / Contribuciones
* Ximena Gonzalez
* Lujan Gonzalez
* Maria Ferreira
* Uri Yael
* Ricardo Dos Santos
* Jorge Saldivar

# TODO
* Agregar filtros en busqueda de reportes (rango de fecha, pais, ciudad) ✅
* Hacer que funcione los filtros de la busqueda ✅
* Hacer pagina de colaboraciones ✅
* Hacer vistas de cuando ve el reporte completo ✅
* Controlar publicaciones que no pueda acceder varias veces ✅
* Solucionar que las views puedan cambiar y mantenerse cuando se clicka en alguna de ellas ✅
* En admin que pueda cambiar la publicacion de allowed a False ✅
* Agregar Google Analytics
* Agregar logger
* Agregar que pueda reportarse las publicaciones
* Crear contenedor para probar (docker)
* Improve doc
* crear pip requirements

# Technologies
* Python 3.8
* Django 3.1
* Postgresql 1x
* venv

# Instalacion / Installation (Ubuntu 18.04)
* `sudo apt-get update`
* `sudo apt-get install python3-pip libpq-dev postgresql postgresql-contrib`
* `sudo - postgres psql` iniciamos sesion en el usuario de postgres y accedemos a la consola psql.
* `CREATE DATABASE buscamascota;` esto es en la consola psql para crear la base de datos.
* `CREATE USER myuser WITH PASSWORD 'password';` para crear usuario (guardar datos para poner en archivo .env).
* `GRANT ALL PRIVILEGES ON DATABASE buscamascota TO myuser;` damos privilegios al usuario que creamos.
* `\q` salimos de la consola psql.
* `python3 -m venv NAMEPROJECT` creamos un virtual enviroment.
* `source NAMEPROJECT/bin/activate` activamos el virtual enviroment.
* `git clone https://github.com/OscarGonzalez97/buscamascota.git`
* `cd buscamascota`
* `git checkout -b origin develop`
* `chmod +x scripts/prepare.sh`
* `./scripts/prepare.sh`
* Completar archivo .env con toda las variables creadas en pasos anteriores.
* `pip3 install -r requirements.txt`
* `python3 manage.py runserver`
* Ir a la dirección indicada y usar la aplicación.
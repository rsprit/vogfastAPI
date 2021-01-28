# Running in docker

## Installation

```bash
sudo apt-get install docker.io docker-compose
```

## Services

Currently two services are defined in `docker-compose.yaml`:

* db

  This is the Mysql database server. It's data is stored on a persistent volume, therefore
  `docker-compose down db` will leave the database intact, whereas `docker-compose down -v db`
  will remove the volume and you will start with an empty database.

  You start the db service with `docker-compose up -d db`.

  Currently port 3306 is exposed from the db service to facilitate local development. This
  is **not** required in production.

* loader

  This is not a service per se, but a job that will load the latest dataset, erase the contents
  of the database and populate the database with the latest data.

  You start the loader job with `docker-compose run --rm loader`. Since it has a dependency on 
  db, db will be start if necessary.

## Building the images

If you change the definition of the db or loader images, you will have to rebuild them by issueing
`docker-compose build`

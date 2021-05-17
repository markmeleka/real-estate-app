# Real Estate Listings App
An app to manage real estate listings of interest.

Prerequisites:
 * Docker and docker-compose [https://docs.docker.com/get-docker/]

How to run:
 * In the root directory run `docker-compose build` then `docker-compose up`
 * The Django server should be running locally on port 8000 [http://localhost:8000/]
 * To open a shell in the Docker container run `docker-compose run --rm app sh`
 * To run a command in the Docker container directly run `docker-compose run --rm app sh c "<command>"`

Useful commands: 
 * To reset the database run `docker-compose run --rm app sh -c "python manage.py reset_db"`

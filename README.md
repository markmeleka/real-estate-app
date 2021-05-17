# Real Estate Listings App
An app to manage real estate listings of interest.

Prerequisites:
 * Docker and docker-compose [https://docs.docker.com/get-docker/]

How to run:
 1. Run the docker image with: `docker-compose up`
    * The Django server should be running locally on port 8000 [http://localhost:8000/]
 2. Seed the database with:
    `docker-compose run --rm app sh -c "python manage.py load_realtor_ca_data realtor_ca_cleaned_data.csv"`
 3. Make a user for authentication with: `docker-compose run --rm app sh -c "python manage.py createsuperuser"`
 4. Access the API documentation locally at /swagger [http://localhost:8000/swagger/]
    and authorize using your credentials from Step 3.
    * Example GET usage: http://localhost:8000/api/listing/listings/?min_bedrooms=4&ordering=price

Useful commands:
 * To open a shell in the Docker container run: `docker-compose run --rm app sh`
 * To run a django command directly in the Docker container run:
   `docker-compose run --rm app sh c "python manage.py <command>"`
   * To reset the database use the command: `reset_db`
   * To run tests use the command: `test`
   * To find other available commands use the command: `help`

TODOs:
 * Automate Steps 2 and 3 with a shorter command.
 * API tests for updating and deleting a listing.
 * Add type hints

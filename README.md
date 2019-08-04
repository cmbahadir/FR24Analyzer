# FR24 Analyzer

FR24 Analyzer caches the flights to redis to calculate the approach duration. And after calculation flight is written to DB (postgreSQL). Data will be used by an another image to predict the approach duration of the future flights to the determined airport. 

## How to run the data gatherer
All configuration can be done by editting config.yml but below modifications has to be done currently.

### Steps
1 - Set the IPs for postgresql and redis containers on config.yaml.

2 - Run the 1-init.sql query to init the postgresql db. (Currently docker-compose.yml cannot do it.)
Run;

    docker-compose build
    docker-compose up

# FR24 Analyzer

FR24 Analyzer is a project to predict the approach time of the aircrafts to a certain airport by using the data gathered from FR24 (flightradar24.com). There are two main functions, first to gather the data "get" and then run the random forest algorithm on it "fit". Code is python version independent but it is suggested to use python 2.7 to address any configuration issue.

All the application configuration can be done by modifying the config.yaml file which consists below options;

```yaml
bounds : "41.39,40.44,28.69,29.68"  #Bounded area to cover for approaching planes
airportName : "SAW"                 #Airport name which is used as a filter parameter in request
airportLat : 40.899876              #Airports exact lattitude
airportLon : 29.310093              #Airports exact longtitude
redis_ip : 127.0.0.1                #Redis instance ip - default
redis_port : 6379                   #Redis instance port - default
postgres_ip : 127.0.0.1             #Postgres instance ip -default
postgres_port : 5432                #Postgres instance port - default
```

### How to run the data gatherer (get)
Make sure that postgresql and redis are running and properly configured.
```
python fr24Analyzer.py -g GET
```
Logging is optional and can be triggered as below and starts to log to a file named "log" under current directory.
```
python fr24Analyzer.py -g GET -l LOG
```


### How to run the data analyzer (fit)
```
python fr24Analyzer.py -f FIT
```

### Docker

Currently docker images are not stable and requires few improvements. But if you are still interested in running them follow these steps:

1 - Set the IPs for postgresql and redis containers on config.yaml.

2 - Run the 1-init.sql query to init the postgresql db. (Currently docker-compose.yml cannot do it.)
Run;

    docker-compose build
    docker-compose up

## Contributing
Please create issues for the problems you have faced and also for feature requests. If you have any feature implementation and fix, all kind of PRs are welcomed.

## Warning
Keep in mind that this is just an experimental project and data requests from FR24 may require paid account. You can get further information about data services from here; https://www.flightradar24.com/commercial-services/data-services



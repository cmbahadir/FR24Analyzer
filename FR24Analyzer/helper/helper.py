from math import sin, cos, sqrt, atan2, radians
import yaml

class Helper(object):
    def readFromConfigFile(self, fileName):
        configParameters = dict()
        try:
            configFile = open(fileName)
            config = yaml.safe_load(configFile)
            configParameters["bounds"] = config["bounds"]
            configParameters["airportName"] = config["airportName"]
            configParameters["airportLat"] = config["airportLat"]
            configParameters["airportLon"] = config["airportLon"]
            configParameters["redis_ip"] = config["redis_ip"]
            configParameters["redis_port"] = config["redis_port"]
            configParameters["postgres_ip"] = config["postgres_ip"]
            configParameters["postgres_port"] = config["postgres_port"]
            configFile.close()
            return configParameters
        except:
            return False

    def writeToConfigFile(self, fileName, userConfiguration):
        try:
            #Flush the file first
            configFile = open(fileName, 'w+')
            configFile.flush()
            configFile.close()
            #Write to config file
            configFile = open(fileName, 'a+')
            configFile.write("bounds : " + '"' + userConfiguration['bounds'] + '"' + '\n')
            configFile.write("airportName : " + '"' + userConfiguration['airportName'] + '"' + '\n')
            configFile.write("airportLat : " + userConfiguration['airportLat'] + '\n')
            configFile.write("airportLon : " + userConfiguration['airportLon'] + '\n')
            configFile.write("redis_ip : " + userConfiguration['redis_ip'] + '\n')
            configFile.write("redis_port : " + userConfiguration['redis_port'] + '\n')
            configFile.write("postgres_ip : " + userConfiguration['postgres_ip'] + '\n')
            configFile.write("postgres_port : " + userConfiguration['postgres_port'])
            configFile.close()
        except:
            return False

    def calcDistanceFromAirport(self, latPlane, lonPlane, latAirport, lonAirport):
        R = 6373.0
        lat1 = radians(latPlane)
        lon1 = radians(lonPlane)
        lat2 = radians(latAirport)
        lon2 = radians(lonAirport)
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        return distance
    
    def addTitleToLogFile(self, fileName):
        f = open(fileName, 'a+')
        f.write("Flight" + "," + "Lattitude" + "," + "Longtitude" + "," +
                "Heading" + "," + "Altitude" + "," + "Speed" + "," + "Time" + "," +  "DistanceToAirport" "\n")
        f.close()


    


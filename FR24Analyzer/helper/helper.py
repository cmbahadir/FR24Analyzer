from math import sin, cos, sqrt, atan2, radians
import yaml

class Helper(object):
    def readFromConfigFile(self, fileName):
        configParameters = dict()
        configFile = open(fileName)
        config = yaml.safe_load(configFile)
        configParameters["bounds"] = config["bounds"]
        configParameters["airportName"] = config["airportName"]
        configParameters["airportLat"] = config["airportLat"]
        configParameters["airportLon"] = config["airportLon"]
        return configParameters

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


    


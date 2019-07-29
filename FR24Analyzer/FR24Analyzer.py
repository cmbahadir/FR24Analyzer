from .helper import helper
from .store import store
import requests
import time
import json
from datetime import datetime


class FR24Analyzer(object):

    def __init__(self, configFile="config.yaml", logFile="log"):
        self._hlp = helper.Helper()
        self.configFile = configFile
        
        #Set the log file and add titles to logfile
        self.logFile = logFile
        self._hlp.addTitleToLogFile(self.logFile)

        configParameters = self._hlp.readFromConfigFile(self.configFile)
        self.bounds = configParameters["bounds"]
        self.airportName = configParameters["airportName"]
        self.airportLat = configParameters["airportLat"]
        self.airportLon = configParameters["airportLon"]
        self._url = "https://data-live.flightradar24.com/zones/fcgi/feed.js?"
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}

    def __del__(self):
        del self._hlp

    def getLandingTimeToAirport(self):
        payload = {"bounds": str(self.bounds),
                "faa": 1,
                "satellite": 1,
                "mlat": 1,
                "flarm": 1,
                "adsb": 1,
                "gnd": 1,
                "air": 1,
                "vehicles": 1,
                "estimated": 1,
                "maxage": 14400,
                "gliders": 1,
                "stats": 1,
                "to": str(self.airportName)}
        response = requests.get(self._url, headers=self._headers, params=payload)
        responseJSON = response.json()
        self._readKeysFromJSONObject(responseJSON)


    def _readKeysFromJSONObject(self, jsonObject):
        flightData = dict()
        #TODO: Move redis connection configuration to configuration file
        redisInstance = store.store()
        airportCoordinates = [self.airportLat, self.airportLon]
        f = open(self.logFile, 'a+')
        for key in jsonObject:
                if key not in ["version", "full_count", "stats"]:
                    value = jsonObject[key]
                    #Write to csv File
                    lat = value[1]
                    lon = value[2]
                    hdg = value[3]
                    alt = value[4]
                    spd = value[5]
                    flight = value[0]
                    _now = datetime.now()
                    _time = time.mktime(_now.timetuple())
                    distanceToAirport = str(self._hlp.calcDistanceFromAirport(value[1], value[2], airportCoordinates[0], airportCoordinates[1]))
                    f.write(str(flight) + "," + str(lat) + "," + str(lon) + "," + str(hdg) +
                            "," + str(alt) + "," + str(spd) + "," + str(_time) + "," + str(distanceToAirport) + "\n")

                    # Write to REDIS                            
                    flightData['lat'] = lat
                    flightData['lon'] = lon
                    flightData['hdg'] = hdg
                    flightData['alt'] = alt
                    flightData['spd'] = spd
                    flightData['distance'] = distanceToAirport
                    flightData['time'] = _time

                    #TODO: Add check to here if the same flight is exist on the REDIS
                    # do not add and check if the al value 0 than add it with an extension
                    redisInstance.writeToRedis(flight, flightData)
        f.close()
import requests
import time
from datetime import datetime
import json
from apscheduler.schedulers.background import BackgroundScheduler
from FR24Analyzer.store import store
from FR24Analyzer.helper import helper

def addTitleToFile():
    f = open('toIST.csv', 'a+')
    f.write("Flight" + "," + "Lattitude" + "," + "Longtitude" + "," +
            "Heading" + "," + "Altitude" + "," + "Speed" + "," + "Time" + "," +  "DistanceToAirport" "\n")
    f.close()

def getLandingToIST():
    test_url = "https://data-live.flightradar24.com/zones/fcgi/feed.js?"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
    #TODO : Move bounds, to variables to configuration file.
    payload = {"bounds": "41.39,40.44,28.69,29.68",
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
               "to": "SAW"}
    response = requests.get(test_url, headers=headers, params=payload)
    responseJSON = response.json()
    readKeysFromJSONObject(responseJSON)
    # print(response.json())


def readKeysFromJSONObject(jsonObject):
    flightData = dict()
    #TODO: Move redis connection configuration to configuration file
    storeToRedis = store.store()
    utility = helper.Helper()
    #Aiport coordinates TODO: Move to configuration file
    airportCoordinates = [40.899876, 29.310093]
    f = open('toIST.csv', 'a+')
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
                distanceToAirport = str(utility.calcDistanceFromAirport(value[1], value[2], airportCoordinates[0], airportCoordinates[1]))
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
                storeToRedis.writeToRedis(flight, flightData)
    f.close()


def gatherResults():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(getLandingToIST, 'interval', minutes=1)
    sched.start()


if __name__ == "__main__":
    addTitleToFile()
    while True:
        getLandingToIST()
        time.sleep(2)

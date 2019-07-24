import requests
import time
from datetime import datetime
import json
from apscheduler.schedulers.background import BackgroundScheduler
from math import sin, cos, sqrt, atan2, radians
import toRedis

def addTitleToFile():
    f = open('toIST.csv', 'a+')
    f.write("Flight" + "," + "Lattitude" + "," + "Longtitude" + "," +
            "Heading" + "," + "Altitude" + "," + "Speed" + "," + "Time" + "," +  "DistanceToAirport" "\n")
    f.close()

def getLandingToIST():
    test_url = "https://data-live.flightradar24.com/zones/fcgi/feed.js?"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
    payload = {"bounds": "41.55,40.61,28.19,29.47",
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
               "to": "IST"}
    response = requests.get(test_url, headers=headers, params=payload)
    responseJSON = response.json()
    readKeysFromJSONObject(responseJSON)
    # print(response.json())


def readKeysFromJSONObject(jsonObject):
    flightData = dict()
    r = toRedis.connectToRedis()
    istCoordinates = [41.259899, 28.7427334]
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
                distanceToAirport = str(calcDistanceFromAirport(value[1], value[2], istCoordinates[0], istCoordinates[1]))
                f.write(str(flight) + "," + str(lat) + "," + str(lon) + "," + str(hdg) +
                        "," + str(alt) + "," + str(spd) + "," + str(datetime.now()) + "," + str(distanceToAirport) + "\n")

                # Write to REDIS                            
                flightData['flight'] = flight
                flightData['lat'] = lat
                flightData['lon'] = lon
                flightData['hdg'] = hdg
                flightData['alt'] = alt
                flightData['spd'] = spd
                flightData['distance'] = distanceToAirport
                flightData['time'] = str(datetime.now())

                #TODO: Add check to here if the same flight is exist on the REDIS
                # do not add and check if the al value 0 than add it with an extension
                toRedis.writeToRedis(r, flightData['flight'], flightData)
    f.close()


def gatherResults():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(getLandingToIST, 'interval', minutes=1)
    sched.start()


def calcDistanceFromAirport(latPlane, lonPlane, latAirport, lonAirport):
    # approximate radius of earth in km
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


if __name__ == "__main__":
    addTitleToFile()
    while True:
        getLandingToIST()
        time.sleep(2)

import redis
import datetime

def connectToRedis():
    r = redis.Redis(host='localhost')
    return r

#Write Tests:
#Check if the altitude-lat-lon are not changed when the plane reaches 1150 feet (0 feet for SAW)
#Check the time difference if it works properly
def writeToRedis(r, name, data):
    check = r.exists(name)
    lastAltitude = data['alt']
    lastTime = data['time']
    if check == 1:
        firstTime = r.hmget(name, 'time')
        #TODO: Change the altitude when the airport is changed as SAW - Currently IST new airport
        #does not cover adsb data continuously
        if lastAltitude == 0:
                firstTimeObject = datetime.datetime.strptime(
                    firstTime, '%b %d %Y %I:%M%p')
                lastTimeObject = datetime.datetime.strptime(
                    lastTime, '%b %d %Y %I:%M%p')
                duration = lastTimeObject - firstTimeObject
                r.hmset(name, 'time', str(duration))
    else:
        r.hmset(name, data)
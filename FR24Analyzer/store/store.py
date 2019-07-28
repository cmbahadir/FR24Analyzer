import redis
import datetime


class store(object):
    def __init__(self, ip=None, port=None):
        if ip is None:
            ip = 'localhost'
        if port is None:
            port = 6379
        self._redis_connection = redis.Redis(host=ip, port=port)

    def writeFirstOccurence(self, name, data):
        firstOccurence = data['time']
        firstKey = "first:" + name
        checkFirstOccurenceFlight = self._redis_connection.exists(firstKey)
        if checkFirstOccurenceFlight == 1:
            return
        else:
            self._redis_connection.lpush(firstKey, firstOccurence)

    def writeToHash(self, name, data):
        flightKey = 'flight:' + name
        checkFlightExists = self._redis_connection.exists(flightKey)
        firstAltitude = data['alt']
        if checkFlightExists == 1 or firstAltitude == 0:
            return
        else:
            self._redis_connection.hmset(flightKey, data)

    def writeLandTime(self, name, data):
        flightKey = 'flight:' + name
        lastKey = 'last:' + name
        lastOccurence = data['time']
        checkFlightKey = self._redis_connection.exists(flightKey)
        checkLastKey = self._redis_connection.exists(lastKey)
        checkAltitude = data['alt']
        if checkFlightKey == 1 and checkLastKey == 0 and checkAltitude == 0:
            self._redis_connection.lpush(lastKey, lastOccurence)
        else:
            return
    
    def writeToRedis(self, name, data):
        self.writeFirstOccurence(name, data)
        self.writeToHash(name, data)
        self.writeLandTime(name, data)
    

    def __del__(self):
        return
        #No need to delete the redis instance since it is already deleted
        #When got out of scope by redis library.

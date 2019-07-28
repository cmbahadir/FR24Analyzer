import redis
import datetime


class store(object):
    def __init__(self, ip=None, port=None):
        if ip is None:
            ip = 'localhost'
        if port is None:
            port = 6379
        self._redis_connection = redis.Redis(host=ip, port=port)

    def _writeFirstOccurence(self, name, data):
        firstOccurence = data['time']
        firstKey = "first:" + name
        checkFirstOccurenceFlight = self._redis_connection.exists(firstKey)
        if checkFirstOccurenceFlight == 1:
            return
        else:
            self._redis_connection.lpush(firstKey, firstOccurence)

    def _writeToHash(self, name, data):
        flightKey = 'flight:' + name
        checkFlightExists = self._redis_connection.exists(flightKey)
        firstAltitude = data['alt']
        if checkFlightExists == 1 and firstAltitude != 0:
            return
        else:
            self._redis_connection.hmset(flightKey, data)

    def _writeLandTime(self, name, data):
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
        self._writeFirstOccurence(name, data)
        self._writeToHash(name, data)
        self._writeLandTime(name, data)
    

    def __del__(self):
        return
        #No need to delete the redis instance since it is already deleted
        #When got out of scope by redis library.

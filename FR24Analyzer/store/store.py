import redis
import datetime


class store(object):
    def __init__(self, ip=None, port=None):
        if ip is None:
            ip = '172.18.0.2'
        if port is None:
            port = 6379
        self.__redis_connection = redis.Redis(host=ip, port=port)

    def writeFirstOccurence(self, name, data):
        firstOccurence = data['time']
        firstKey = "first:" + name
        checkFirstOccurenceFlight = self.__redis_connection.exists(firstKey)
        if checkFirstOccurenceFlight == 1:
            return
        else:
            self.__redis_connection.lpush(firstKey, firstOccurence)

    def writeToHash(self, name, data):
        flightKey = 'flight:' + name
        checkFlightExists = self.__redis_connection.exists(flightKey)
        firstAltitude = data['alt']
        if checkFlightExists == 1 or firstAltitude == 0:
            return
        else:
            self.__redis_connection.hmset(flightKey, data)
            self.__redis_connection.hset(flightKey, 'isLanded', 0)

    def writeLandTime(self, name, data):
        flightKey = 'flight:' + name
        lastKey = 'last:' + name
        lastOccurence = data['time']
        checkFlightKey = self.__redis_connection.exists(flightKey)
        checkLastKey = self.__redis_connection.exists(lastKey)
        checkAltitude = data['alt']
        if checkFlightKey == 1 and checkLastKey == 0 and checkAltitude == 0:
             self.__redis_connection.lpush(lastKey, lastOccurence)   
        else:
            return
    
    def writeToRedis(self, name, data):
        self.writeFirstOccurence(name, data)
        self.writeToHash(name, data)
        self.writeLandTime(name, data)
        self.updateTheHash(name, data)


    def updateTheHash(self, name, data):
        flightKey = 'flight:' + name
        lastKey = 'last:' + name
        lastOccurence = data['time']
        checkLastKey = self.__redis_connection.exists(lastKey)
        isLanded = self.__redis_connection.hget(flightKey, 'isLanded')
        if checkLastKey == 1 and isLanded != 1:
            firstOccurenceTime = self.__redis_connection.lrange('first:' + name, 0, 1)
            firstOccurenceTime_Float = self.__convertByteToFloat(firstOccurenceTime[0])
            calculatedDuration = lastOccurence - firstOccurenceTime_Float
            self.__redis_connection.hset(flightKey, 'time', calculatedDuration)
            self.__redis_connection.hset(flightKey, 'isLanded', 1)
            # TODO: After the plane is landed first: and last: keys can be deleted.
            # TODO: Move the flight:* hashes to a permenant DB (postgreSQL)
        else:
            return
    
    def __convertByteToFloat(self, byteData):
        stringData = byteData.decode('utf-8')
        floatData = float(stringData)
        return floatData
    
    def __del__(self):
        return
        #No need to delete the redis instance since it is already deleted
        #When got out of scope by redis library.

import redis
import datetime
import psycopg2


class store(object):
    def __init__(self, redis_ip=None, redis_port=None,
                 postgres_ip=None, postgres_port=None):
        if redis_ip is None:
            redis_ip = '127.0.0.1'
        if redis_port is None:
            redis_port = 6379
        self.__redis_connection = redis.Redis(host=redis_ip, port=redis_port)
        self.__postgres_connection = PostGreSQL(postgres_ip=postgres_ip, postgres_port=postgres_port)

    def writeFirstOccurence(self, name, data):
        firstOccurence = data['time']
        firstKey = "first:" + name
        flightKey = "flight:" + name
        checkFirstOccurenceFlight = self.__redis_connection.exists(firstKey)
        checkFlightExistance = self.__redis_connection.exists(flightKey)
        if checkFirstOccurenceFlight == 1 or checkFlightExistance == 0:
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
            flightDict = self.__redis_connection.hgetall(flightKey)
            flightDict["key"] = name
            self.__postgres_connection.writeToDB(flightDict)

            #Delete the keys for the landed plane
            self.__redis_connection.delete(flightKey)
            self.__redis_connection.delete(lastKey)
            self.__redis_connection.delete("first:" + name)
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

class PostGreSQL():
    def __init__(self, postgres_ip='localhost', postgres_port=5432):
        if postgres_ip is None:
            postgres_ip = '127.0.0.1'
        if postgres_port is None:
            postgres_port = 5432
        self.__postgresql_connection = psycopg2.connect(host=postgres_ip, port=postgres_port, database="fr24", user="cmb", password="postgres.123")
        self.__postgresql_cursor = self.__postgresql_connection.cursor()
        self.__postgresql_cursor.execute("CREATE TABLE IF NOT EXISTS SAW (Flight varchar, Lat real,Lon real, Hdg real, Altitude real, Speed real, Duration real, Distance real);")
        self.__postgresql_connection.commit()
    
    def __del__(self):
        self.__postgresql_cursor.close()
        self.__postgresql_connection.close()

    def writeToDB(self, dataDict):
        self.__postgresql_cursor.execute(
            """
            INSERT INTO SAW (Flight, Lat, Lon, Hdg, Altitude, Speed, Duration, Distance)
            VALUES (%(key)s, %(lat)s, %(lon)s, %(hdg)s, %(alt)s, %(spd)s, %(time)s, %(distance)s);
            """, {  "key" : dataDict['key'], 
                    "lat" : float(dataDict[b'lat'].decode('utf-8')), 
                    "lon" : float(dataDict[b'lon'].decode('utf-8')),
                    "hdg" : float(dataDict[b'hdg'].decode('utf-8')),
                    "alt" : float(dataDict[b'alt'].decode('utf-8')),
                    "spd" : float(dataDict[b'spd'].decode('utf-8')),
                    "time": float(dataDict[b'time'].decode('utf-8')),
                    "distance": float(dataDict[b'distance'].decode('utf-8'))
                 })
        self.__postgresql_connection.commit()
    
    def getFromDB(self):
        query = "select * from saw"
        self.__postgresql_cursor.execute(query)
        flightRecords = self.__postgresql_cursor.fetchall()
        return flightRecords


from store import store
import redis

def check_the_key_existance():
    redis_Test = redis.Redis(host='localhost', port=6379)
    existingKeys = redis_Test.keys()
    return str(existingKeys)

#Check redis connection over store instance
def test_connect_to_redis():
    """
    Connect to Redis and Return the connection instance.
    """
    storeInstance = store.store()
    assert storeInstance

#Check writing to redis over connection
def test_write_to_redis():
    """
    Check writing a dictionary to redis.
    """
    test_flight_dict = {'alt': 5025, 'distance': '43.85733437539533', 'flight': '4BAAA9',
                         'hdg': 89, 'lat': 40.996, 'lon': 28.3538, 'spd': 255, 'time': '2019-07-28 13:16:02.958279'}
    test_flight = '4BAAA9'
    storeInstance = store.store()
    storeInstance.writeToRedis(test_flight, test_flight_dict)
    keys = check_the_key_existance()
    assert test_flight in keys


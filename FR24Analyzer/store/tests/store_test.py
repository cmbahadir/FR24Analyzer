from FR24Analyzer.store import store as st
import redis
import pytest
import psycopg2

class Test_Store(object):
    def setup_method(self):
        self.storeInstance = st.store()
        self.redis_Test = redis.Redis(host='localhost', port=6379)
        self.postgres_Test_conn = psycopg2.connect(host='localhost', port=5432, database='fr24', user='cmb', password='postgres.123')
        self.postgres_Test_cursor = self.postgres_Test_conn.cursor()

    # def teardown_method(self):
    #     self.redis_Test.flushall()

    #Check redis connection over store instance
    def test_connect_to_redis(self):
        """
        Connect to Redis and Return the connection instance.
        """
        assert self.storeInstance

    #Check writing to redis over connection
    def test_001_write_to_hash(self):
        """
        Check writing a dictionary to redis.
        """
        test_flight_dict = {'alt': 5025, 'distance': '43.85733437539533', 'flight': '4BAAA9',
                            'hdg': 89, 'lat': 40.996, 'lon': 28.3538, 'spd': 255, 'time': '2019-07-28 13:16:02.958279', 'isLanded': 0}
        test_flight = '4BAAA9'
        self.storeInstance.writeToHash(test_flight, test_flight_dict)
        assert self.redis_Test.exists("flight:" + test_flight) == 1

    def test_002_write_last_appearance_time(self):
        """
        Check if the method writes the time in sec when the plane is landed with its name as key.
        """
        test_flight_dic_landed = {'alt': 0, 'distance': '43.85733437539533', 'flight': '4BAAA9',
                                  'hdg': 89, 'lat': 40.996, 'lon': 28.3538, 'spd': 255, 'time': '2019-07-28 13:22:02.958279', 'isLanded': 0}
        test_flight = '4BAAA9'
        self.storeInstance.writeLandTime(test_flight, test_flight_dic_landed)
        assert self.redis_Test.exists("last:" + test_flight) == 1

    def test_003_taxiing_plane_is_not_duplicated(self):
        """
        try to insert the second time when the plane is taxiing (alt = 0) over its landed value.
        """
        test_flight_dic_taxiing = {'alt': 0, 'distance': '43.85733437539533', 'flight': '4BAAA9',
                                   'hdg': 89, 'lat': 40.996, 'lon': 28.3538, 'spd': 255, 'time': '2019-07-28 13:24:02.958279'}
        test_flight = '4BAAA9'
        self.storeInstance.writeLandTime(test_flight, test_flight_dic_taxiing)
        landingTimeList = self.redis_Test.lrange("last:" + test_flight, 0, 10)
        assert '2019-07-28 13:22:02.958279' in str(landingTimeList[0])
    
    def test_004_check_the_landed_plane(self):
        test_flight_dic_approaching = {'alt': 200, 'distance': '43.85733437539533', 'flight': '4BAAA10',
                                   'hdg': 89, 'lat': 40.996, 'lon': 28.3538, 'spd': 255, 'time': 100, 'isLanded': 0}
        test_flight_dic_landing = {'alt': 0, 'distance': '43.85733437539533', 'flight': '4BAAA10',
                                   'hdg': 89, 'lat': 40.996, 'lon': 28.3538, 'spd': 255, 'time': 200.9, 'isLanded': 0}
        test_flight = '4BAAA10'
        self.storeInstance.writeToHash(test_flight, test_flight_dic_approaching)
        self.storeInstance.writeFirstOccurence(test_flight, test_flight_dic_approaching)
        self.storeInstance.writeLandTime(test_flight, test_flight_dic_landing)
        self.storeInstance.updateTheHash(test_flight, test_flight_dic_landing)
        self.postgres_Test_cursor.execute("select * from saw where flight='4BAAA10';")
        fetchedFlight = self.postgres_Test_cursor.fetchone()
        assert fetchedFlight[0] == test_flight


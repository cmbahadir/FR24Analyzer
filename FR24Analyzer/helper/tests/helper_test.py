from FR24Analyzer.helper import helper
import pytest


class TestObject(object):
    def setup_method(self):
        self.hlp = helper.Helper()

    @pytest.mark.parametrize("test_lat, test_lon,expected_distance", [(41.39, 28.69, 75.29753975122823), (40.44, 29.68, 59.91991319963786)])
    def test_calculate_distance_to_airport(self, test_lat, test_lon, expected_distance):
        # Coordinates of the airport
        latAirport = 40.899876
        lonAirport = 29.310093
        distance = self.hlp.calcDistanceFromAirport(
            test_lat, test_lon, latAirport, lonAirport)
        assert distance == expected_distance

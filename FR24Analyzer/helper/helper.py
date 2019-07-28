from math import sin, cos, sqrt, atan2, radians

class Helper(object):
    def calcDistanceFromAirport(self, latPlane, lonPlane, latAirport, lonAirport):
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
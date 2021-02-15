"""
This module includes function which works\
with geolocations and so on(to find coordinates/distance).
"""
from geopy.geocoders import Nominatim
from math import sin, cos, sqrt, atan2, radians


def city_and_country(film_and_location):
    """
    This function returns information about city and country,\
    where the film was made.
    >>> city_and_country(['Spiderman', 'New York studio,
    Marshall street, New York, USA'])
    ('USA', 'New York')
    """
    location = film_and_location[1]
    if len(location.split(', ')) > 1:
        if location.split(' ')[-1] == 'UK'\
           and len(location.split(' ')[-1]) > 2:
            return location.split(', ')[-2], location.split(', ')[-3]
        return location.split(', ')[-1], location.split(', ')[-2]
    else:
        return location


def find_latitude_and_longtitude(city_and_country):
    """
    This function finds latitude and longitude of city.
    >>> find_latitude_and_longtitude(('USA', 'New York'))
    (40.7127281, -74.0060152)
    """
    if isinstance(city_and_country, list):
        geolocator = Nominatim(user_agent="My_map")
        loc = geolocator.geocode(city_and_country[1] + ', ' +
                                 city_and_country[0])
        if loc is None:
            lat = None
            longt = None
        else:
            lat = loc.latitude
            longt = loc.longitude
    else:
        geolocator = Nominatim(user_agent="My_map")
        loc = geolocator.geocode(city_and_country)
        if loc is None:
            lat = None
            longt = None
        else:
            lat = loc.latitude
            longt = loc.longitude
    return lat, longt


def find_distance(film_latitude_longtitude, my_latitude_longtitude):
    """
    This function finds distance between two locations on the map.
    >>> find_distance((34.8765, 23.8976), (49,8306, 24.8765))
    1580.3891583080374
    """
    film_latitude = radians(film_latitude_longtitude[0])
    film_longtitude = radians(film_latitude_longtitude[1])
    my_latitude = radians(my_latitude_longtitude[0])
    my_longtitude = radians(my_latitude_longtitude[1])
    earth_radius = 6373.0
    longtitude = my_longtitude - film_longtitude
    latitude = my_latitude - film_latitude
    const_1 = sin(latitude/2)**2 + cos(film_latitude) * cos(my_latitude) * sin(longtitude/2)**2
    const = 2 * atan2(sqrt(const_1), sqrt(1-const_1))
    distance = earth_radius * const
    return distance

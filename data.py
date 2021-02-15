"""
This module includes functions which works with data:
prepare data for writing to csv file and writes needed information to file.
"""
import geo
import geopy
import pandas as pd
import os


def create_dictionary_with_locations(file):
    """
    This function creates dictionary where keys\
    are years of films and values are films.
    """
    diction = {}
    opened = open(file, 'r')
    for line in opened:
        if '\t' in line:
            part_1 = line.split('\t')[0]
            if line.split('\t')[-1].count(',') >= 1\
               or line.split('\t')[-1].count('(') == 0:
                part_2 = line.split('\t')[-1][:-1]
            else:
                part_2 = line.split('\t')[-2]
            key = part_1[part_1.find('(')+1:part_1.find(')')]
            if len(key) == 4:
                if key not in diction.keys():
                    lst_1 = [[part_1[0:part_1.find("(")-1], part_2]]
                    diction[key] = lst_1
                else:
                    if len(diction[key]) <= 50 and [part_1[0:part_1.find("(")],
                       part_2] not in diction[key]:
                        lst_2 = [part_1[0:part_1.find("(")], part_2]
                        diction[key].append(lst_2)
    return diction


def find_in_dictionary(diction, year):
    """
    This fuction returns films of needed year.
    >>> find_in_dictionary({'2008': ['Iron Man', 'L.O.V.E.'],\
'2011': ['Iron Man 2', 'Secrets']}, '2011')
    ['Iron Man 2', 'Secrets']
    """
    if year in diction.keys():
        return diction[year]
    else:
        return 'Sorry... Try to enter another year.'


def add_distance(list_of_films, user_input):
    """
    This function adds distance between user and film's location to list.
    >>> add_distance([["Iron Man", "New York, USA"]], (49.8307, 24.6893))
    [['Iron Man', 'New York, USA', 40.7127281, -74.0060152, 7216.655735850788]]
    """
    new_lst = []
    for film in list_of_films:
        city_country = geo.city_and_country(film)
        try:
            latit_and_longtit = geo.find_latitude_and_longtitude(city_country)
            if latit_and_longtit[0] is None:
                distance = "can't find"
            else:
                distance = geo.find_distance(latit_and_longtit, user_input)
        except geopy.exc.GeocoderUnavailable:
            pass
        film.append(latit_and_longtit[0])
        film.append(latit_and_longtit[1])
        film.append(distance)
        if distance != "can't find":
            new_lst.append(film)
    return sorted(new_lst, key=lambda x: x[-1])[0:10]


def create_csv(list_of_lists):
    """
    This function creates csv with infos\
    about nearest films and returns path to this csv.
    """
    headers = ['Films', 'Location', 'Latitude', 'Longtitude', 'Distance']
    data = pd.DataFrame(list_of_lists)
    data.to_csv('locations.csv', index=False, header=headers)
    return os.path.realpath('locations.csv')

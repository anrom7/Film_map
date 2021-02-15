"""
This module includes function which creates html map.
"""
import folium
import pandas as pd
import os.path


def show_locations(file, coordinates):
    """
    This function returns html map with two layers:
    'Film locations' shows user's location on the map and locations of films;
    'Population' shows population in countries.
    >>> show_locations(os.path.realpath('locations.csv'), (43.9876, 22.9873))
    'map1.html'
    """
    data = pd.read_csv(file, error_bad_lines=False)
    latitude = data['Latitude']
    longtitude = data['Longtitude']
    film_name = data['Films']
    distance = data['Distance']
    map = folium.Map(location=[coordinates[0], coordinates[1]])
    film_loc = folium.FeatureGroup(name='Film locations')
    same = []
    diff = -0.2
    for lt, lg, film, ds in zip(latitude, longtitude, film_name, distance):
        same.append(lt)
        if lt in same:
            lt = lt + diff
            diff -= 0.2
        film_loc.add_child(folium.Marker(location=[lt, lg],
                                         popup=film + '\n' + str(ds) + ' km',
                                         icon=folium.Icon()))
    film_loc.add_child(folium.Marker(location=[coordinates[0], coordinates[1]],
                                     icon=folium.Icon(color='red')))
    pop_amount = folium.FeatureGroup(name="Population")
    pop_amount.add_child(
        folium.GeoJson(data=open('world.json', 'r',
                       encoding='utf-8-sig').read(),
                       style_function=lambda x:
                           {'fillColor': 'green'
                            if x['properties']['POP2005'] < 10000000
                            else 'orange'
                            if
                            10000000 <= x['properties']['POP2005'] < 20000000
                            else 'red'}))
    map.add_child(pop_amount)
    map.add_child(film_loc)
    map.add_child(folium.LayerControl())
    map.save('map1.html')
    return 'map1.html'

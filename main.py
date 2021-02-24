"""
This module includes function which creates html map.
"""
import os.path
import webbrowser
import data
import geo
import create_map



def main():
    """
    This function creates the htnl map and returns html string.
    >>> main()
    Please enter the year:
    Please enter your latitude:
    Please enter your longitude:
    Wait a minute...
    'map1.html'
    """
    print("Please enter the year:")
    users_year = input()
    print("Please enter your latitude:")
    users_latitude = float(input())
    print("Please enter your longitude:")
    users_longitude = float(input())
    print("Wait a minute...")
    users_coordinates = users_latitude, users_longitude
    file_path = os.path.realpath('locations.list')
    dictionary = data.create_dictionary_with_locations(file_path)
    films_of_year = data.find_in_dictionary(dictionary, users_year)
    list_with_distance = data.add_distance(films_of_year, users_coordinates)
    csv_file_path = data.create_csv(list_with_distance)
    html = create_map.show_locations(csv_file_path, users_coordinates)
    path = os.path.abspath(html)
    url = 'file://' + path
    webbrowser.open(url)
    return html

if __name__ == "__main__":
    print(main())

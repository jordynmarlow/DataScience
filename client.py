# client.py

import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from haversine import haversine, Unit
from math import *

hospitals = pd.read_excel('hospital_data.xlsx')

geolocator = Nominatim(user_agent="hospital_data")
user_lat = 0
user_lon = 0

def get_hospital_data(address):
    # verify the zip code is in the data frame
    #if zip in hospitals['zip']:
    # if true, send data
    global user_lat, user_lon

    location = geolocator.geocode(address)
    user_lat = location.latitude
    user_lon = location.longitude
    print([user_lat, user_lon])
    # get three closest hospitals with availability
    # return data frame
    hospitals['dist'] = np.nan
    
    hospitals['dist'] = hospitals.apply(get_distance, axis=1)

    #return hospitals[hospitals['taken_beds'] < hospitals['total_beds']].nsmallest(3, 'dist')
    df = hospitals[hospitals['taken_beds'] < hospitals['total_beds']].sort_values('dist')
    return df



def get_distance(row):
    #lat1 = radians(user_lat)
    #lon1 = radians(user_lon)
    #lat2 = radians(float(row['lat']))
    #lon2 = radians(float(row['lon']))

    #dlon = lon2 - lon1
    #dlat = lat2 - lat1

    #a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    #c = 2 * atan2(sqrt(a), sqrt(1 - a))

    #distance = 6373.0 * c
    #return distance

    user = (user_lat, user_lon)
    hospital = (float(row['lat']), float(row['lon']))

    print([user, hospital])

    return geodesic(user, hospital).km

print(get_hospital_data('1700 University Ave Flint'))
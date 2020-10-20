# https://towardsdatascience.com/geoparsing-with-python-c8f4c9f78940
import numpy as np
import matplotlib.pyplot as plt 
#%matplotlib inline

import pandas as pd
import geopandas as gpd

from urllib import request
from geotext import GeoText

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import geopy
from shapely.geometry import Point, Polygon
import descartes


cities = ['Jönkööping stad har en anrik tradition', 'Stockholm är Sveriges största stad', 
'I Göteborg stad är mest akvedukter och tunnlar', 
'I Borås kommun regnar det mycket', 'I Malmö är det fullt krig']

#geolocator = Nominatim(timeout=2)

nominatim_service = Nominatim(user_agent='SC') 
#and then call the service on whatever your input data is 
#geolocator = RateLimiter(nominatim_service.geocode, min_delay_seconds=1, timeout=2) collisions['geocodes'] = collisions['location_string'].apply(geolocator) 
geolocator = nominatim_service.geocode

cities_clean = []
for city in cities:
    print(GeoText(city).cities)
    cities_clean.append(GeoText(city).cities)
    
lat_lon = []
for city in cities_clean: 
    try:
        location = geolocator(city)
        if location:
            print(location.latitude, location.longitude)
            lat_lon.append(location)
    except GeocoderTimedOut as e:
        print("Error: geocode failed on input %s with message %s" + (city, e))
#print(lat_lon)
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
import random


bigCitiesSweden = ["Stockholm", "Göteborg", "Malmö", "Uppsala", "Upplands Väsby", "Sollentuna", "Västerås", "Örebro", "Linköping", 
    "Helsingborg" "Jönköping", "Norrköping", "Lund", "Umeå", "Gävle", "Södertälje", "Borås", "Eskilstuna", "Växjö", "Halmstad", "Karlstad"]
listC = ['Lidingö stad har en anrik tradition']

bigCityRandomVar = 0.04
cityRandomVar = 0.02


#geolocator = Nominatim(timeout=2)


#NEW
nominatim_service = Nominatim(user_agent='SCC', timeout=3)
geolocator = nominatim_service.geocode

#nominatim_service = Nominatim(user_agent='SC') 
#and then call the service on whatever your input data is 
#geolocator = rateLimiter(nominatim_service.geocode, min_delay_seconds=1, timeout=3) #collisions['geocodes'] = collisions['location_string'].apply(geolocator) 
#geolocator = nominatim_service.geocode

citiesClean = []
def geoparseListofCities(list):
    for city in list:
        #print(GeoText(city).cities)
        citiesClean.append(GeoText(city).cities)
    global latLong    
    latLong = []
    for city in citiesClean: 
        try:
            location = geolocator(city)
            if location:
                #print(location.latitude, location.longitude)
                latLong.append(location)
        except GeocoderTimedOut as e:
            print("Error: geocode failed on input %s with message %s" + (city, e))

def geopaseSingleCity(city):
    location = geolocator(city)
    if location:
        #print(location.latitude, location.longitude)
        latLong.append(location)
    return(location.latitude, location.longitude)
    # except GeocoderTimedOut as e:
    #     print("Error: geocode failed on input %s with message %s" + (city, e))

def geoparseLatitude(city, randomize):
    location = geolocator(city)
    if location:
        if randomize == True: #Sample LAT 59.3251172, index of values we want to change is 3-5, generate random number between 10-50, 325 + 50 = 
            if city in bigCitiesSweden:            
                lowerBound = (location.latitude-bigCityRandomVar)
                upperBound = (location.latitude+bigCityRandomVar)
                newRandomLat = random.uniform(lowerBound, upperBound)
                return(round(newRandomLat, 7))
            else:
                lowerBound = (location.latitude-cityRandomVar)
                upperBound = (location.latitude+cityRandomVar)
                newRandomLat = random.uniform(lowerBound, upperBound)
                return(round(newRandomLat, 7))
        else:
            return(round(location.latitude, 7))
    

def geoparseLongitude(city, randomize):
    location = geolocator(city)
    if location:
        if randomize == True: #Stockholm LAT 59.3251172 LONG 18.0710935, first decimal = 11km, second decimal = 1km STANDARD RANDOM VALUE WILL BE 5km from center lat/long in each direction
            if city in bigCitiesSweden:            
                lowerBound = (location.longitude-bigCityRandomVar)
                upperBound = (location.longitude+bigCityRandomVar)
                newRandomLong = random.uniform(lowerBound, upperBound)
                return(round(newRandomLong, 7))
            else:
                lowerBound = (location.longitude-cityRandomVar)
                upperBound = (location.longitude+cityRandomVar)
                newRandomLong = random.uniform(lowerBound, upperBound)
                return(round(newRandomLong, 7))
        else:
            return(round(location.longitude, 7))

def testFunction():
    one, two = geoparseLatitude("Stockholm", True), geoparseLongitude("Stockholm", True)
    return(one, two)
    
#print(testFunction())    
#geoparseListofCities(listC)
#print(latLong)
#print(type(latLong))
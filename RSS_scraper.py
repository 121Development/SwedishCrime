# -*- coding: utf-8 -*-
import pandas as pd
import datefinder
from bs4 import BeautifulSoup
import requests
import csv

url = "https://polisen.se/aktuellt/rss/hela-landet/handelser-i-hela-landet/"
resp = requests.get(url)

soup = BeautifulSoup(resp.content, features="xml")
items = soup.findAll('item')

item = items[0]


handelser_hela_landet_fler = []

for item in items:
    # if latest entry in items is not equal to latest variable stored, then go ahead and store.
    handelser_hela_landet = {}
    handelser_hela_landet['title'] = item.title.text
    handelser_hela_landet['description'] = item.description.text
    handelser_hela_landet['date'] = item.pubDate.text
    handelser_hela_landet['link'] = item.link.text
    latest_date_rss = item.pubDate.text
    handelser_hela_landet_fler.append(handelser_hela_landet)
    # if keyword in title is this then category is that.
    if latest_date == handelser_hela_landet_fler[0]

    # Category of crime
    # Region
    # Part of city or city
    # Detailed time
    # push to SQL DB
# print(handelser_hela_landet_fler[0])
# print(handelser_hela_landet)

# Parse date, imported code from date_parser.py
matches = list(datefinder.find_dates(handelser_hela_landet['date']))
date = matches[0]
print(date)
# https://pbpython.com/pandas-list-dict.html


datamatris_polisen_rss = pd.DataFrame.from_dict(handelser_hela_landet_fler)
datamatris_polisen_rss.to_csv('ny.csv', encoding='utf-8-sig')

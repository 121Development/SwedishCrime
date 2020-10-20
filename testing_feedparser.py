import feedparser
import datetime
#import pandas as pd
from pprint import pprint
import re
import mysql.connector
from mysql.connector import Error

feedparser = feedparser.parse("https://polisen.se/aktuellt/rss/hela-landet/handelser-i-hela-landet/")
#intialize list to store events
events = []
entries = feedparser['entries']

pprint(len(entries))
print(entries)
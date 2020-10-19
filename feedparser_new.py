# https://www.tutorialspoint.com/python_text_processing/python_reading_rss_feed.htm
import feedparser
import datetime
#import pandas as pd
from pprint import pprint
import re
import databaseConn
import mysql.connector
from mysql.connector import Error

# YOUR DB INFO #
host = "localhost"
user = "root"
password = ""
database = "swedishCrime"



# SET BELOW ROUNDS VARIABLE TO 2 ROUNDS MORE THAN NUMBER OF LEVELS OF YOUR DB
# PARENT TABLE, CHILD, CHILD OF CHILD ETC.
rounds = 6

# def test():
#     return("Hej")

#Establish the connection and set cursor
try:
    conn = mysql.connector.connect(
        user=user, password=password, host=host, database=database)
    cursor = conn.cursor()
    print(f"\nSuccessfully connected to database {database}\n")
except Error as err:
    print(f"Error: '{err}'")

# Function to read passed query
def read_query(conn, query):
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

# Function to execute passed query
def execute_query(conn, query):
    try:
        cursor.execute(query)
        conn.commit()
        print("Commited data")
    except Error as err:
        print(f"Error: '{err}'")

def delete_data(conn, query):
    try:
        cursor.execute(query)
        conn.commit()
    except Error as err:
        return("Error")
# Function to delete table data, takes variable rounds
def delete_table_data(rounds):
    n = 0
    while n < rounds:
        for name in table_names:
            delete_data(conn, f"DELETE FROM {name};")
        n += 1
    print("Sucessfully deleted all table data\n")

def get_all_table_names():
    sql = '''SHOW TABLES'''
    cursor.execute(sql)
    result = cursor.fetchall()
    table_names = [item for t in result for item in t] 
    return(table_names)


feedparser = feedparser.parse("https://polisen.se/aktuellt/rss/hela-landet/handelser-i-hela-landet/")

#print(databaseConn.test())


def split_title(title_for_current_entry, number):
    #Below takes the title and strips any : with a space after to separate an updated title from a normal title. Then splits all on , 
    list_of_event_location_location_detail = []
    list_of_event_location_location_detail = re.sub('\:\s', ', ', title_for_current_entry)
    list_of_event_location_location_detail = re.split(
        "\,\s", list_of_event_location_location_detail)
     

    if len(list_of_event_location_location_detail) == 5:
        if number == 0:
            return(list_of_event_location_location_detail[0])
        if number == 1:
            return(list_of_event_location_location_detail[1])
        if number == 2:
            return(list_of_event_location_location_detail[2])
        if number == 3:
            return(list_of_event_location_location_detail[3])
        if number == 4:
            return(list_of_event_location_location_detail[4])
        if number == 5:
            try:
                return(list_of_event_location_location_detail[5])
            except IndexError:
                return("")

    elif len(list_of_event_location_location_detail) == 3:
        if number == 0:
            return("")
            # return(updated)
        if number == 1:
            return(list_of_event_location_location_detail[0])
        if number == 2:
            return(list_of_event_location_location_detail[1])
        if number == 3:
            return("")
        if number == 4:
            return(list_of_event_location_location_detail[2])
        if number == 5:
            return("")

    elif len(list_of_event_location_location_detail) == 4:
        if list_of_event_location_location_detail[0][0].isupper():
            if number == 0:
                return(list_of_event_location_location_detail[0])
            if number == 1:
                return(list_of_event_location_location_detail[1])
            if number == 2:
                return(list_of_event_location_location_detail[2])
            if number == 3:
                return("")
            if number == 4:
                return(list_of_event_location_location_detail[3])
            if number == 5:
                try:
                    return(list_of_event_location_location_detail[5])
                except IndexError:
                    return("")
        else:
            if number == 0:
                return("")
            if number == 1:
                return(list_of_event_location_location_detail[0])
            if number == 2:
                return(list_of_event_location_location_detail[1])
            if number == 3:
                return(list_of_event_location_location_detail[2])

            if number == 4:
                return(list_of_event_location_location_detail[3])
            if number == 5:
                try:
                    return(list_of_event_location_location_detail[5])
                except IndexError:
                    return("")

#intialize list to store events
events = []
entries = feedparser['entries']

for entry in entries: 
    events.append({
        'link': entry['link'],
        'updated': split_title(entry['title'], 0),
        'event_time': split_title(entry['title'], 1),
        'category': split_title(entry['title'], 2),
        'category_detail': split_title(entry['title'], 3),
        'location': split_title(entry['title'], 4),
        'location_detail': split_title(entry['title'], 5),
        'summary': entry['summary'],
        'title': entry['title'],
        'published': entry['published'],
        'published_parsed': entry['published_parsed'],
    })

#Strip key value and keep value only from dict and store in list.
values_only = []
for event in events: 
    #print(event)
    values_only.append(list(event.values()))


#Loop through values in values_only and add '' around all and #replace '' with NULL in a loop
for entry in values_only: #lista med listor
    for n, i in enumerate(entry): #lista med title, link etc.
        if len(entry[n]) == 0:
            entry[n] = ""
        entry[-1] = "" #temporarily remove the time struct from the end for now
        # if entry[n] != "NULL":
        #     entry[n] = f"'{entry[n]}'"
tmp = ""

table_names = get_all_table_names()
delete_table_data(6)

for entry in values_only:
    tmp = str(entry).strip('[]')
    #print(type(tmp))
    #print(tmp)
    tmp = re.sub('"NULL"', '', tmp)
    pop_events = "INSERT INTO events VALUES (" + tmp + ");"
#    print(pop_events)
    execute_query(conn, pop_events)
#print(pop_events)




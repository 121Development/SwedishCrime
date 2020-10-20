import feedparser
import datetime
from pprint import pprint
import re
import DBConnector as db

feedparser = feedparser.parse("https://polisen.se/aktuellt/rss/hela-landet/handelser-i-hela-landet/")

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
entries = []
entries = feedparser['entries']
#pprint(entries)

def categorizeEntries():
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
timeList = []
def stripValues():
    #Strip key value and keep value only from dict and store in list.
    global values_only
    values_only = []
    for event in events: 
        values_only.append(list(event.values()))

def addNull():
    #Loop through values in values_only and add replace '' with NULL in a loop
    for entry in values_only: #lista med listor
        for n, i in enumerate(entry): #lista med title, link etc.
            if len(entry[n]) == 0:
                entry[n] = "NULL"
            # entry[-1] = re.sub(')', '', entry[-1])
        entry[-1] = f"{entry[-1]}"
        timeList.append(entry[-1])
def addToDB():
    #loop through enties and turn them into strings, look for "uppdaterad" and then update table instead of insert
    for entry in values_only:
        if entry[1][0] == "U":
            #print("Found U")
            linkPKforEntry = "".join(entry[0])
            
            # if updated is populated, skip below
            isUpdated = "SELECT updated FROM events WHERE link = '" + linkPKforEntry + "';"
            tmpResponse = db.read_query(isUpdated)
            
            try:
                tmpResponse[0][0]    
            except IndexError:
                pass
            
            try:
                if hasattr(tmpResponse, '__len__'):
                    if len(tmpResponse) < 7:
                        updateTmp = "".join(entry[1])
                        summaryTmp = "".join(entry[-4])
                        update_event = "UPDATE events SET updated = '" + updateTmp + "' WHERE link = '" + linkPKforEntry + "';"
                        db.update_query(update_event)
                        update_event = "UPDATE events SET summary = '" + summaryTmp + "' WHERE link = '" + linkPKforEntry + "';"
                        db.update_query(update_event)
            except Error as err:
                print(f"Error: '{err}'")
        else:
            tmp = str(entry).strip('[]')
            tmp = re.sub('\'NULL\'', 'NULL', tmp)
            pop_events = "INSERT INTO events VALUES (" + tmp + ");"
            db.execute_query(pop_events)

categorizeEntries()
stripValues()
addNull()
addToDB()

print(f"{len(values_only)} events processed")
print("Commited " + str(db.commitedSum) + "events")
print("Updated " + str(db.updatedSum) + "events")

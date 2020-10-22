import feedparser
import datetime
from pprint import pprint
import re
import DBConnector as db
import geoparser as gp

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

def categorizeEntries():
    global events, entries
    events, entries = [], []
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
        
def addCityToList():
    global listOfCities
    global listOfCitiesSet
    listOfCities, listOfCitiesSet = [], []
    for entry in values_only:
        #print(entry[5])
        listOfCities.append(entry[5])
        listOfCitiesSet = set(listOfCities)

# def checkIfLinkExists2(lank):
#     global listOf200links
#     tmpQuery = '''SELECT link FROM events limit 200;'''
#     listOf200links = db.read_query(tmpQuery)
#     tmp = []
#     for link in listOf200links:
#         tmp.append(str(link).strip("()',"))
#     if lank in tmp:
#         return(True)
#     return(False)

def checkIfLinkExists():
    global listOf200links
    tmpQuery = '''SELECT link FROM events limit 200;'''
    tmp = db.read_query(tmpQuery)
    listOf200links = []
    for link in tmp:
        listOf200links.append(str(link).strip("()',"))
    # if lank in tmp:
    #     return(True)
    # return(False)
    
def addLatLong():
    global valuesWithLatLong, ListOfLan, ListOfLanSet
    ListOfLan, ListOfLanSet = [], []
    valuesWithLatLong = []
#   valuesWithLatLong.append(values_only)
#    print(valuesWithLatLong[0][0])
    for entry in values_only:
        if entry[0] not in listOf200links:
            tmpEntryFive = entry[5]
            if "län" in entry[5] and entry[5] != "Borlänge":
                ListOfLan.append(entry[5])
                ListOfLanSet = set(ListOfLan)
            print(entry[5])   
            #tmpEntryFive = gp.geoparseLatitude(tmpEntryFive, False)
            valuesWithLatLong.append((gp.geoparseLatitude(tmpEntryFive, False)))
            valuesWithLatLong.append((gp.geoparseLongitude(tmpEntryFive, False)))
            valuesWithLatLong.append((gp.geoparseLatitude(tmpEntryFive, True)))
            valuesWithLatLong.append((gp.geoparseLongitude(tmpEntryFive, True))) 
    return(valuesWithLatLong)
        #valuesWithLatLong.append(gp.geoparseLatitude(tmpEntryFive, False))
        # entry.append(gp.geoparseLongitude(entry[5], False)
        # entry.append(gp.geoparseLatitude(entry[5], True)
        # entry.append(gp.geoparseLongitude(entry[5], True)


def addToDB():
    #loop through enties and turn them into strings, look for "uppdaterad" and then update table instead of insert, get lat long from geoparser and add random elements and add to DB
    for entry in values_only:
    #for entry in valuesWithLatLong
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
            #if checkIfLinkExists(entry[0]) == False:
            if entry[0] not in listOf200links:    
                tmp = str(entry).strip('[]')
                tmp = re.sub('\'NULL\'', 'NULL', tmp)
                pop_events = "INSERT INTO events VALUES (" + tmp + ");"
                db.execute_query(pop_events)
            else:
                pass

#initialize feedparser
feedparser = feedparser.parse("https://polisen.se/aktuellt/rss/hela-landet/handelser-i-hela-landet/")


categorizeEntries()
stripValues()
addNull()
addCityToList()
checkIfLinkExists()
print(addLatLong())
#print(valuesWithLatLong)
#addToDB()




# #intialize lists
# events, entries = [], [] 
# ListOfLan = []

# print(gp.geoparseLatitude("Stockholm", False, False))
# print(gp.geoparseLongitude("Stockholm", False, False))


print(f"{len(values_only)} events processed")
print("Commited " + str(db.commitedSum) + "events")
print("Updated " + str(db.updatedSum) + "events")

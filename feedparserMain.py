import feedparser
import datetime
from pprint import pprint
import re
import DBConnector as db
import geoparser as gp 



#create new DB
#Drop UQ keys
#add categories to it
#add cities to it

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
    global valuesOnly
    valuesOnly = []
    for event in events: 
        valuesOnly.append(list(event.values()))

def addNull():
    #Loop through values in valuesOnly and add replace '' with NULL in a loop
    for entry in valuesOnly: #lista med listor
        for n, i in enumerate(entry): #lista med title, link etc.
            if len(entry[n]) == 0:
                entry[n] = "NULL"
            # entry[-1] = re.sub(')', '', entry[-1])
        entry[-1] = f"{entry[-1]}"
        
def addCityToList():
    global listOfCities
    global listOfCitiesSet
    listOfCities, listOfCitiesSet = [], []
    for entry in valuesOnly:
        #print(entry[5])
        listOfCities.append(entry[5])
        listOfCitiesSet = set(listOfCities)

def addCategoryToList():
    global listOfCategories
    global listOfCategoriesSet
    listOfCategories, listOfCategoriesSet = [], []
    tmpQuery = '''SELECT category FROM events;'''
    tmp = db.read_query(tmpQuery)
    for category in tmp:
        if category not in listOfCategories:
            listOfCategories.append(str(category).strip("()',"))
    listOfCategoriesSet = set(listOfCategories)        
    #print(listOfCategoriesSet)

def latestLinks():
    global latest200links
    latest200links = []
    #tmpQuery = '''SELECT link FROM events ORDER BY event_time DESC limit 200;'''
    tmpQuery = '''SELECT link FROM events;'''
    tmp = db.read_query(tmpQuery)
    for link in tmp:
        tmp2 = str(link).strip("()',")
        latest200links.append(tmp2)

def checkIfExistsInDB():
    global eventsToCommitNew, linkForUpdatedEvents, updatedEvents
    eventsToCommitNew, linkForUpdatedEvents, updatedEvents = [], [], []

    for entry in valuesOnly:
        if entry[0] not in latest200links:
            print("Found new event")    
            eventsToCommitNew.append(entry)    

    print("[+] Will commit new data for " + str(len(eventsToCommitNew)) + " events")
    #print(eventsToCommitNew)
    # testtest = input("continue to add lat long for events? (y/n)? > ")
    # if testtest == "y":
    #     pass

def addUpdatedEventInfo():
    # testtest = input("Continue to update updated events? (y/n)? > ")
    # if testtest == "y":
    #     pass

    for entry in valuesOnly:
        if entry[1][0] == "U":
            #print("Found Updated event")
            updatedEvents.append(entry)
    print("[+] Will update data for " + str(len(updatedEvents)) + " events")

    for entry in updatedEvents:
        linkPKforEntry = entry[0]
        updateTmp = "".join(entry[1])
        summaryTmp = "".join(entry[-8])
        update_event = "UPDATE events SET updated = '" + updateTmp + "' WHERE link = '" + linkPKforEntry + "';"
        db.update_query(update_event)
        update_event = "UPDATE events SET summary = '" + summaryTmp + "' WHERE link = '" + linkPKforEntry + "';"
        db.update_query(update_event)
        #print("updated event")

def addLatLong():
    global eventsToCommitNewWithLatLong, listOfLan, listOfLanSet
    listOfLan, listOfLanSet = [], []
    eventsToCommitNewWithLatLong = eventsToCommitNew
        
    for n, i in enumerate(eventsToCommitNewWithLatLong): #lista med title, link etc.
        tmpEntryFive = i[5]      
        if "län" in tmpEntryFive and tmpEntryFive != "Borlänge":
            listOfLan.append(tmpEntryFive)
            listOfLanSet = set(listOfLan)
        
        eventsToCommitNewWithLatLong[n].append((gp.geoparseLatitude(tmpEntryFive, False)))
        eventsToCommitNewWithLatLong[n].append((gp.geoparseLongitude(tmpEntryFive, False)))
        eventsToCommitNewWithLatLong[n].append((gp.geoparseLatitude(tmpEntryFive, True)))
        eventsToCommitNewWithLatLong[n].append((gp.geoparseLongitude(tmpEntryFive, True))) 
        print("Added lat long for: " + eventsToCommitNewWithLatLong[n][5] + " to list eventsToCommitNewWithLatLong")
      
def commitNewEventToDB():
#add items do DB, update items where link is in linkupdatelist
    for entry in eventsToCommitNewWithLatLong:
    
        tmp = str(entry).strip('[]')
        tmp = re.sub('\'NULL\'', 'NULL', tmp)
        pop_events = "INSERT INTO events VALUES (" + tmp + ");"
        db.execute_query(pop_events)
            
#initialize feedparser
feedparser = feedparser.parse("https://polisen.se/aktuellt/rss/hela-landet/handelser-i-hela-landet/")




#google = True
db.whichConnection(0)
print(db.conn)
categorizeEntries()
stripValues()
addNull()
addCityToList()
addCategoryToList()
latestLinks()
checkIfExistsInDB()
#print(latest200links)
testtest = input("continue?")
if testtest == "y":
    print("fortsätter")

print("[+] calling latLong function")
addLatLong()
print("[+] commiting new data")
commitNewEventToDB()
print("[+] updating data for updated events")
addUpdatedEventInfo()
print("[+] Switching DB")
db.whichConnection(1)
checkIfExistsInDB()
print("[+] commiting new data")
commitNewEventToDB()
print("[+] updating data for updated events")
addUpdatedEventInfo()
print("[+] closing DB connection")
db.closeConnection()

# #intialize lists
# events, entries = [], [] 
# listOfLan = []

# print(gp.geoparseLatitude("Stockholm", False, False))
# print(gp.geoparseLongitude("Stockholm", False, False))

print('''
################################
'''
)
print("Commited " + str(db.commitedSum) + " events")
print("Updated " + str(int(db.updatedSum / 2)) + " events")
print('''
################################
'''
)
'''
Resposible for connecting to database hosted by
CouchDB and retrieving records or any related
information. 

Owner: MARSfarm Corporation
Authors: Jackie Zhong(zy99120@gmail.com)
Last Modified: 7/14/2020
'''

from couchdb import Server
import json
from datetime import datetime
from key import couch_access

#Query and return data as required for charting
def chart_query(db_name, limit, sensor):
    
    server = couch_access()
    db = server[db_name]
    result = {}

    #Mango query format used by CouchDB
    payload={"selector":{"status.status_qualifier":"Success", "activity_type":"Environment_Observation", 
             "subject.name":"Air","subject.attribute.name": str(sensor)}, "fields":["start_date.timestamp", "subject.attribute.value"],
             "sort":[{"start_date.timestamp":"desc"}], "limit":int(limit)}     

    data = db.find(payload)

    #Associate each timestamp with its value
    for row in data:
        result[row["start_date"]["timestamp"]] = row["subject"]["attribute"]["value"]

    return result

'''
BACKLOG CODE NOT IN ACTIVE USE

#return the number of records in the database
def count_records(db_name):

    server = couch_access()
    db = server[db_name]

    count = 0

    #the Mango Query criteria
    payload={"selector":{"activity_type":"Environment_Observation"}, "limit": 100000000}   

    data = db.find(payload)

    for row in data:
        count+=1 
    
    return count

#retrive the complete temperature record in json format
def get_tmp_json(db_name):

    server = couch_access()
    db = server[db_name]

    payload={"selector":{"activity_type":"Environment_Observation",
             "subject.name":"Air","subject.attribute.name": "Temperature"},
             "sort":[{"start_date.timestamp":"desc"}], "limit": 1}

    return list(db.find(payload))

#retrive the complete CO2 record in json format
def get_co2_json(db_name):

    server = couch_access()
    db = server[db_name]

    payload={"selector":{"activity_type":"Environment_Observation",
             "subject.name":"Air","subject.attribute.name": "CO2"},
             "sort":[{"start_date.timestamp":"desc"}], "limit": 1}

    return list(db.find(payload))

#retrive the complete humidity record in json format
def get_hum_json(db_name):

    server = couch_access()
    db = server[db_name]

    payload={"selector":{"activity_type":"Environment_Observation",
             "subject.name":"Air","subject.attribute.name": "Humidity"}, 
             "sort":[{"start_date.timestamp":"desc"}], "limit": 1}

    return list(db.find(payload))

#return the latest value of temperature, humidity, and CO2
def sensor_latest(db_name):

    server = couch_access()
    db = server[db_name]
    ts = datetime.utcnow().isoformat()[:19]
    li = []

    payload={"selector":{"start_date.timestamp":{"$lt":ts}, "status.status_qualifier":"Success", "activity_type":"Environment_Observation", 
             "subject.name":"Air","subject.attribute.name": "Temperature"}, "fields":["start_date.timestamp", "subject.attribute.value"],
             "sort":[{"start_date.timestamp":"desc"}], "limit":1}        

    data = db.find(payload)
    
    for row in data:
        li.append(float(row["subject"]["attribute"]["value"]))

    payload={"selector":{ "start_date.timestamp":{"$lt":ts}, "status.status_qualifier":"Success", "activity_type":"Environment_Observation", 
             "subject.name":"Air","subject.attribute.name": "Humidity"}, "fields":["start_date.timestamp", "subject.attribute.value"],
             "sort":[{"start_date.timestamp":"desc"}], "limit":1}        

    data = db.find(payload)
    
    for row in data:
        li.append(float(row["subject"]["attribute"]["value"]))

    payload={"selector":{ "start_date.timestamp":{"$lt":ts}, "status.status_qualifier":"Success", "activity_type":"Environment_Observation", 
             "subject.name":"Air","subject.attribute.name": "CO2"}, "fields":["start_date.timestamp", "subject.attribute.value"],
             "sort":[{"start_date.timestamp":"desc"}], "limit":1}        

    data = db.find(payload)
    
    for row in data:
        li.append(row["subject"]["attribute"]["value"])
    
    return li
'''
    

if __name__ == "__main__":
    print(chart_query("jackie_mvp_2", 24))
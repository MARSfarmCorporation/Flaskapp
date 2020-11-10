'''
Responsible for accessing, retrieving, and modifying user 
information in CouchDB

Owner: MARSfarm Corporation
Authors: Jackie Zhong(zy99120@gmail.com)
Last Modified: 7/14/2020
'''

from couchdb import Server
from key import couch_access
import json

#Verify whether a user exist or not by looking up email in CouchDB
def verify_usr(email):

    server = couch_access()
    db_name = "users"
    db = server[db_name]

    #Mango query: get one record that has the same email
    payload={"selector":{"Email":email}, "limit": 1}
    
    data = db.find(payload)

    if list(data) == []:
        return "new"
    else:
        return "exist"

#Retrieve fields from user profile given his email
def retrieve_rec(email):

    server = couch_access()
    db_name = "users"
    db = server[db_name]

    #Mango query: get one record that has the same email
    payload={"selector":{"Email":email}, "limit": 1}

    data = db.find(payload)

    #Put needed fields in list to return conveniently
    result = []
    for row in data:
        result.append(row["Database"])
        result.append(row["S3"])
        result.append(row["S3_link"])
    
    return result
    
def get_record(email):
    # Retreive full record from database based on email selector
    # Boilerplate database access
    
    server = couch_access()
    db_name = "users"
    db = server[db_name]
    
    # Query the database
    payload = {"selector":{"Email":email}, "limit":1}
    # Change binary return to list
    
    data = list(db.find(payload))

    # make sure have data    
    if data:
        # return first record of list, but should only be one
        return data[0]
    # if no record found, return empty list
    return {}

def set_default_device(email, device):
    # function to set default database information
    #print(device)
    
    # Get the full record
    rec = get_record(email)
    if not rec:
        # Fail if no record found
        return False

    # Create another server connection for saving data
    server = couch_access()
    db_name = "users"
    db = server[db_name]

    # Move the selected device info up a level
    # create device list
    dev_list = [dev['Device']['Name'] for dev in rec['Devices']]
    # get index of selected device name
    #print(dev_list)
    index = dev_list.index(device)
    # Update the default values
    rec["Device"] = rec["Devices"][index]["Device"]["Name"]
    rec["Database"] = rec["Devices"][index]["Device"]["Database"]
    rec["S3"] = rec["Devices"][index]["Device"]["S3"]
    rec["S3_link"] = rec["Devices"][index]["Device"]["S3_link"]

    # save back to database using the _id
    id = rec['_id']    
    #print(db[id])
    db[id] = rec
    return True

'''
BACKLOG CODE NOT IN ACTIVE USE

#save a user record given name, email, school, and device
def save_rec(name, email, school, device):

    server = couch_access()
    db_name = "users"
    db = server[db_name]
    doc_id, doc_rev = db.save({"Name": name, "Email": email, "School": school, "Device": device})
'''


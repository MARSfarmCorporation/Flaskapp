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

#Retrieve just the database from user profile given email
def retrieve_db(email):

    server = couch_access()
    db_name = "users"
    db = server[db_name]

    #Mango query: get one record that has the same email
    payload={"selector":{"Email":email}, "limit": 1}

    data = db.find(payload)

    result=[]
    for row in data:
        result.append(row["Database"])
    
    return result

'''
BACKLOG CODE NOT IN ACTIVE USE

#save a user record given name, email, school, and device
def save_rec(name, email, school, device):

    server = couch_access()
    db_name = "users"
    db = server[db_name]
    doc_id, doc_rev = db.save({"Name": name, "Email": email, "School": school, "Device": device})
'''


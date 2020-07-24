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

def verify_usr(email):

    server = couch_access()
    db_name = "users"
    db = server[db_name]

    payload={"selector":{"Email":email}, "limit": 1}
    
    data = db.find(payload)

    if list(data) == []:
        return "new"
    else:
        return "exist"


def save_rec(name, email, school, device):

    server = couch_access()
    db_name = "users"
    db = server[db_name]
    doc_id, doc_rev = db.save({"Name": name, "Email": email, "School": school, "Device": device})

def retrieve_rec(email):

    server = couch_access()
    db_name = "users"
    db = server[db_name]

    payload={"selector":{"Email":email}, "limit": 1}

    data = db.find(payload)

    result = []
    for row in data:
        result.append(row["Database"])
        result.append(row["S3"])
        result.append(row["S3_link"])
    
    return result

def retrieve_db(email):

    server = couch_access()
    db_name = "users"
    db = server[db_name]

    payload={"selector":{"Email":email}, "limit": 1}

    data = db.find(payload)

    result=[]
    for row in data:
        result.append(row["Database"])
    
    return result


if __name__ == "__main__":
    print(retrieve_db("jackie@marsfarm.io")[0])
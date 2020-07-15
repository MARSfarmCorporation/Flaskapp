'''
Responsible for accessing, retrieving, and modifying user 
information in CouchDB

Owner: MARSfarm Corporation
Authors: Jackie Zhong(zy99120@gmail.com)
Last Modified: 7/14/2020
'''

from couchdb import Server
import json

def verify_usr(email):

    url = "https://admin:marsfarm@data.marsfarm.io:6984/"
    db_name = "users"
    server = Server(url)
    db = server[db_name]

    payload={"selector":{"Email":email}, "limit": 1}
    
    data = db.find(payload)

    if list(data) == []:
        return "new"
    else:
        return "exist"


def save_rec(name, email, school, device):

    url = "https://admin:marsfarm@data.marsfarm.io:6984/"
    db_name = "users"
    server = Server(url)
    db = server[db_name]

    doc_id, doc_rev = db.save({"Name": name, "Email": email, "School": school, "Device": device})

def retrieve_rec(email):

    url = "https://admin:marsfarm@data.marsfarm.io:6984/"
    db_name = "users"
    server = Server(url)
    db = server[db_name]

    payload={"selector":{"Email":email}, "limit": 1}

    data = db.find(payload)

    result = []
    for row in data:
        result.append(row["School"])
        result.append(row["Device"])
    
    return result


if __name__ == "__main__":
    print(retrieve_rec("jackie@marsfarm.io"))
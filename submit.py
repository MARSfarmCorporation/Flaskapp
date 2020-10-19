'''
Resposible for formatting and submitting a phenotype
observation record to CouchDB
Owner: MARSfarm Corporation
Authors: Jackie Zhong(zy99120@gmail.com)
Last Modified: 6/29/2020
'''

from couchdb import Server

def submit(row, db_name):
    server = couch_access()
    db = server[db_name]

    rec = {}
    rec['start_date'] = {'timestamp': row[1]}
    rec['participant'] = {'type': 'person', 'name': row[2]}
    rec['status'] = {'status': 'Complete', 'status_qualifier': 'Success'}
    rec['activity_type'] = row[0]
    rec['subject'] = {'name': row[7], 'attribute':{'name': row[6], 'units': row[9], 'value': row[8]}}
    rec['location'] = {'field':row[3], 'trial':row[4], 'plot':row[5]}

    id, rev = db.save(rec)

    return rec




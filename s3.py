'''
This file is responsible for communicating with Amazon S3
to retrive objects or information from S3.
Tha "key_access" file imported by s3.py explicitly contains the
access key to S3 root user, and thus should be kept private
to administrator at all time.

Owner: MARSfarm Corporation
Authors: Jackie Zhong(zy99120@gmail.com)
Last Modified: 6/29/2020
Modified by Jackie 10/12/20
Modified by Peter Webb 10/09/20
'''

import boto3
from key import s3_access
import string
#get 28 images, theoratically one from each day
def get_28_days(bucket):
    s3 = s3_access()
    count = 0
    result = []
    get_last = lambda obj: obj['Key']
   
    objs = s3.list_objects_v2(Bucket=bucket)['Contents']
    for obj in sorted(objs, key=get_last, reverse = True):
        if count % 24 == 0:
            result.append(obj['Key'])
        count+=1
        if len(result) == 28:
            break
    #if there are less than so many days, fill with none
    while len(result) < 28:
        result.append("None")
    return result
#get the name of the latest images sorted by name
def show_latest(bucket):
   s3 = s3_access()
   get_last = lambda obj: obj['Key']
   
   objs = s3.list_objects_v2(Bucket=bucket)['Contents']
   last_added = [obj['Key'] for obj in sorted(objs, key=get_last, reverse = True)][0]
   return last_added
'''
BACKLOG CODE NOT IN ACTIVE USE
#count number of images in a given bucket
def count_img(bucket):
    
    s3 = s3_access()
    count = 0
	
    for item in s3.list_objects(Bucket=bucket)['Contents']:
        count+=1
    
    return count
#download a given image from a given bucket
def download_file(file_name, bucket):
    s3 = s3_access()
 
    x = file_name.split("/")
    name = x[-1]
    output = "/home/ubuntu/flaskapp/static/images/" + name
    s3.download_file(bucket, file_name, output)
'''

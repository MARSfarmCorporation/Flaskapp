'''
This file is responsible for communicating with Amazon S3
to retrive objects or information from S3.
Tha "key_access" file imported by s3.py explicitly contains the
access key to S3 root user, and thus should be kept private
to administrator at all time.

Owner: MARSfarm Corporation
Authors: Jackie Zhong(zy99120@gmail.com)
Last Modified: 6/29/2020
'''

import boto3
from key import s3_access
import string

def get_28_days(bucket):

    s3 = s3_access()
    count = 0
    result = []

    for item in s3.list_objects(Bucket=bucket)['Contents']:
        if count % 12 == 0:
            result.insert(0, item['Key'])
        count+=1
    
    while len(result) < 28:
        result.append("None")

    return result

#count number of images in a given bucket
def count_img(bucket):
    
    s3 = s3_access()
    count = 0
	
    for item in s3.list_objects(Bucket=bucket)['Contents']:
        count+=1
    
    return count

#get the name of the latest images sorted by name
def show_latest(bucket):

   s3 = s3_access()
   get_last = lambda obj: obj['Key']
   
   objs = s3.list_objects_v2(Bucket=bucket)['Contents']
   last_added = [obj['Key'] for obj in sorted(objs, key=get_last, reverse = True)][0]

   return last_added

#download a given image from a given bucket
def download_file(file_name, bucket):

    s3 = s3_access()
 
    x = file_name.split("/")
    name = x[-1]

    output = "/home/ubuntu/flaskapp/static/images/" + name
    s3.download_file(bucket, file_name, output)



if __name__ == "__main__":
    print(get_28_days("dev-jackie-bucket"))
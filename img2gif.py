'''
Based on user's desired time interval, retrieve the
images from S3 and generate a gif.
Owner: MARSfarm Corporation
Authors: Jackie Zhong(zy99120@gmail.com)
Last Modified: 7/24/2020
'''


from PIL import Image
import boto3
import string
import os
from key import s3_access

#downloading images and generate gif
def generate_gif(interval, bucket):

    s3 = s3_access()
    
    #download images based on interval given
    count = -1
    for item in s3.list_objects(Bucket=bucket)['Contents']:
        if(count % int(interval) == 0):
            filename = item['Key'].split('/')  #in case there is a sub folder which will mess up the output url
            output = '/home/ubuntu/flaskapp/static/gif_repo/' + filename[-1]
            s3.download_file(bucket, item['Key'], output)
        count+=1

    images = []
    for image in sorted(os.listdir("/home/ubuntu/flaskapp/static/gif_repo")):
        path = "/home/ubuntu/flaskapp/static/gif_repo/" + image
        images.append(Image.open(path))

    out = []
    for img in images:
        rimg = img.resize([280, 360]) #resize the image
        out.append(rimg)

    gif_name = bucket + "_" + str(interval) + ".gif"
    out[0].save("/home/ubuntu/flaskapp/static/gif/" + gif_name, save_all=True, append_images=out[1:], duration=200, loop=0)

    return gif_name

if __name__ == "__main__":
    generate_gif(24, "dev-jackie-bucket")

'''
The highest level back-end server resposible for calling other python files and serving 
webpages based on users' action.

Owner: MARSfarm Corporation
Authors: Jackie Zhong(zy99120@gmail.com)
Last Modified: 8/17/20
'''
#Python standard library
import string, json

#Third party library
from flask import Flask, render_template, request, send_file

#local library
from s3 import show_latest, get_28_days
from user import verify_usr, retrieve_rec, retrieve_db
from CouchDB import chart_query
from img2gif import generate_gif
from Util import decode_secret

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0




#The starting page
@app.route('/')
def entry_point():
  return render_template("main.html")

#verify if user exist or not and render page accordingly
@app.route('/reception/<secret>', methods = ['GET'])
def usr_main(secret):
  
  email = decode_secret(secret)

  if verify_usr(email) == "new":
    return render_template("new.html")
  else:
    data = retrieve_rec(email)
    latest_object = show_latest(data[1])
    s3_url = data[2]
    link = s3_url + latest_object #generate the complete url to an s3 object
    return render_template("reception.html", secret=secret, link=link)

#serve the humidity dashboard
@app.route('/humidity/<secret>/<time>')
def humidity_main(secret, time):

  email = decode_secret(secret)
  if time == "24":
    return render_template("humidity.html", email=email, secret=secret)
  elif time == "168":
    return render_template("humidity_7days.html", email=email, secret=secret)
  elif time == "all":
    return render_template("humidity_alltime.html", email=email, secret=secret)

#serve the temperature dashboard
@app.route('/temperature/<secret>/<time>')
def temperature(secret, time):

  email = decode_secret(secret)
  if time == "24":
    return render_template("temperature.html", email=email, secret=secret)
  elif time == "168":
    return render_template("temperature_7days.html", email=email, secret=secret)
  elif time == "all":
    return render_template("temperature_alltime.html", email=email, secret=secret)

#serve the co2 dashboard
@app.route('/co2/<secret>/<time>')
def co2(secret, time):

  email = decode_secret(secret)
  if time == "24":
    return render_template("co2.html", email=email, secret=secret)
  elif time == "168":
    return render_template("co2_7days.html", email=email, secret=secret)
  elif time == "all":
    return render_template("co2_alltime.html", email=email, secret=secret)

#Respond to post request and fetch data for charting
@app.route('/chart/<email>/<sensor>', methods=["POST"])
def hum_chart(sensor, email):

  rec = retrieve_rec(email)
  db = rec[0]
  limit = request.get_data() #retrieve query limit sent from chart.js
  data = chart_query(db, int(limit), sensor)
  
  return data

#serve the picture dashboard
@app.route('/picture/<secret>')
def picture(secret):

  email = decode_secret(secret)
  data = retrieve_rec(email)
  imgs_28 = get_28_days(data[1])
  s3_link = data[2]
  
  return render_template("picture.html", s3_link=s3_link, secret=secret,
                          img_28=imgs_28[0], img_27=imgs_28[1], img_26=imgs_28[2], img_25=imgs_28[3],
                          img_24=imgs_28[4], img_23=imgs_28[5], img_22=imgs_28[6], img_21=imgs_28[7],
                          img_20=imgs_28[8], img_19=imgs_28[9], img_18=imgs_28[10], img_17=imgs_28[11],
                          img_16=imgs_28[12], img_15=imgs_28[13], img_14=imgs_28[14], img_13=imgs_28[15],
                          img_12=imgs_28[16], img_11=imgs_28[17], img_10=imgs_28[18], img_9=imgs_28[19],
                          img_8=imgs_28[20], img_7=imgs_28[21], img_6=imgs_28[22], img_5=imgs_28[23],
                          img_4=imgs_28[24], img_3=imgs_28[25], img_2=imgs_28[26], img_1=imgs_28[27],)

#serve the experiment dashboard
@app.route('/experiment/<secret>')
def experiment(secret):
  return render_template("experiment.html", secret=secret)

#serve the setting dashboard
@app.route('/setting/<secret>')
def setting(secret):
  return render_template("setting.html", secret=secret)

#Serve the gif creation page
@app.route('/gif/<secret>')
def gif_entry_point(secret):
  return render_template('gif.html', secret=secret)

#Create gif based on user input
@app.route('/gif/<secret>', methods = ['POST'])
def generate(secret):

  email = decode_secret(secret)
  rec = retrieve_rec(email)
  interval = request.form['interval']
  try:
    gif_name = generate_gif(interval, rec[1])
  except Exception as e:
    gif_name = str(e)

  return render_template('gif.html', gif_name=gif_name)

#Enalb gif downloading
@app.route("/download/<gif>")
def download_temp(gif):

  try :
    return send_file('/home/ubuntu/flaskapp/static/gif/' + gif, as_attachment=True)
  except Exception as e:
    return str(e)



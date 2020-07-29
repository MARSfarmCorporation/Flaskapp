'''
The highest level back-end server resposible for calling other python files and serving 
webpages based on users' action.

Owner: MARSfarm Corporation
Authors: Jackie Zhong(zy99120@gmail.com)
Last Modified: 6/29/2020
'''
#Python standard library
import string, json

#Third party library
from flask import Flask, render_template, request, send_file, jsonify, redirect

#local library
from s3 import count_img, show_latest, download_file, get_28_days
from user import verify_usr, save_rec, retrieve_rec, retrieve_db
from CouchDB import sensor_latest, count_records, get_tmp_json, get_co2_json, get_hum_json, tmp_rec, chart_query
from img2gif import generate_gif
from submit import submit

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0




#The starting page
@app.route('/')
def entry_point():
  return render_template("main.html")

#verify if user exist or not and render page accordingly
@app.route('/reception/<user>/<email>', methods = ['GET'])
def usr_main(user, email):
  
  if verify_usr(email) == "new":
    return render_template("new.html", user=user, email=email)
  else:
    data = retrieve_rec(email)
    latest = show_latest(data[1])
    s3 = data[2]
    link = s3 + latest
    return render_template("reception.html", user=user, email=email, link=link)

#serve the humidity dashboard
@app.route('/humidity/<user>/<email>/<time>')
def humidity_main(user, email, time):
  if time == "24":
    return render_template("humidity.html", user=user, email=email)
  elif time == "168":
    return render_template("humidity_7days.html", user=user, email=email)
  elif time == "all":
    return render_template("humidity_alltime.html", user=user, email=email)


@app.route('/humidity/<email>/chart', methods=["POST"])
def hum_chart(email):

  db = retrieve_db(email)
  limit = request.get_data()
  data = chart_query(db[0], int(limit))
  
  return data

#serve the temperature dashboard
@app.route('/temperature/<user>/<email>')
def temperature(user, email):
  return render_template("temperature.html", user=user, email=email)

@app.route('/temperature/<user>/<email>/<limit>')
def rec_temperature(user, email, limit):
  db = retrieve_db(email)
  
  result = tmp_rec(db[0], limit)
  
  return render_template("temperature.html", user=user, email=email, result=result)

#serve the co2 dashboard
@app.route('/co2/<user>/<email>')
def co2(user, email):
  return render_template("co2.html", user=user, email=email)

@app.route('/co2/<user>/<email>', methods=["POST"])
def co2_chart(user, email):

  limit = request.get_data()
  data = chart_query("jackie_mvp_2", int(limit))
  
  return data

#serve the picture dashboard
@app.route('/picture/<user>/<email>')
def picture(user, email):

  data = retrieve_rec(email)
  imgs_28 = get_28_days(data[1])
  s3_link = data[2]
  
  return render_template("picture.html", user=user, email=email, s3_link=s3_link,
                          img_28=imgs_28[0], img_27=imgs_28[1], img_26=imgs_28[2], img_25=imgs_28[3],
                          img_24=imgs_28[4], img_23=imgs_28[5], img_22=imgs_28[6], img_21=imgs_28[7],
                          img_20=imgs_28[8], img_19=imgs_28[9], img_18=imgs_28[10], img_17=imgs_28[11],
                          img_16=imgs_28[12], img_15=imgs_28[13], img_14=imgs_28[14], img_13=imgs_28[15],
                          img_12=imgs_28[16], img_11=imgs_28[17], img_10=imgs_28[18], img_9=imgs_28[19],
                          img_8=imgs_28[20], img_7=imgs_28[21], img_6=imgs_28[22], img_5=imgs_28[23],
                          img_4=imgs_28[24], img_3=imgs_28[25], img_2=imgs_28[26], img_1=imgs_28[27],)

#serve the temperature dashboard
@app.route('/experiment/<user>/<email>')
def experiment(user, email):
  return render_template("experiment.html", user=user, email=email)

#serve the setting dashboard
@app.route('/setting/<user>/<email>')
def setting(user, email):
  return render_template("setting.html", user=user, email=email)


#registration information page
@app.route("/register/<user>/<email>", methods=['GET', 'POST'])
def usr_register(user, email):

  if request.method == "POST":
    school = request.form['school']
    device = request.form['device']
    try:
      save_rec(user, email, school, device)
      result = "Success"
    except Exception as e:
      result = str(e)
    return render_template("registration.html", user=user, email=email, result=result)
  else:
    return render_template("registration.html", user=user, email=email)


#Page that serves gif
@app.route('/gif/<email>')
def gif_entry_point(email):
  return render_template('gif.html', email=email)

@app.route('/gif/<email>', methods = ['POST'])
def generate(email):

  rec = retrieve_rec(email)
  interval = request.form['interval']
  try:
    gif_name = generate_gif(interval, rec[1])
  except Exception as e:
    gif_name = str(e)

  return render_template('gif.html', gif_name=gif_name)

@app.route("/download/<gif>")
def download_temp(gif):

  try :
    return send_file('/home/ubuntu/flaskapp/static/gif/' + gif, as_attachment=True)
  except Exception as e:
    return str(e)

@app.route("/chart", methods=['POST'])
def get_chart_data():

  limit = request.get_data()
  data = chart_query("jackie_mvp_2", int(limit))
  
  return data


'''
#Pages responsible for retriving
#pictures from Amazon S3
@app.route('/images')
def images_entry_point():
  return render_template('images.html')

@app.route('/images', methods=['POST'])
def get_count_name():

  bucket_name = request.form['bucket']

  try:
    count = str(count_img(bucket_name)) + " images are in the bucket" 
  except Exception as e:
    count = str(e)
    
  try:
    latest = show_latest(bucket_name)
  except Exception as e:
    latest = str(e)

  return render_template('images.html', count=count, latest=latest, bucket_name=bucket_name)

@app.route("/images/retrieve/<bucket>", methods=['GET'])
def get_latest(bucket):

  output="Retrieval Succeeded"

  try:
    latest = show_latest(bucket)
  except Exception as e:
    latest = str(e)

  try: 
    download_file(latest, bucket)
  except Exception as e:
    output = str(e) 
  
  x = latest.split("/")
  img = x[-1]

  return render_template('images.html', latest=latest, output=output, img=img)

@app.route("/download/<img>")
def download_temp(img):

  try :
    return send_file('/home/ubuntu/flaskapp/static/images/' + img, as_attachment=True)
  except Exception as e:
    return str(e)


#Pages responsible for retriving environmental
#observation from CouchDB
@app.route('/sensor')
def sensor_entry_point():
  return render_template('sensor.html')

@app.route('/sensor', methods=['POST'])
def sensor_data():

  db_name = request.form['db_name']

  try:
    count = count_records(db_name)
    
    tmp = sensor_latest(db_name)
    latest_tmp = str(tmp[0]) + " Celcius"
    latest_hum = str(tmp[1]) + "%"
    latest_co2 = str(tmp[2]) + " ppm"
    
    tmp_record = json.dumps(get_tmp_json(db_name))
    co2_record = json.dumps(get_co2_json(db_name))
    hum_record = json.dumps(get_hum_json(db_name))
    
    return render_template("sensor.html", count=count, latest_tmp=latest_tmp,
                            latest_hum=latest_hum, latest_co2=latest_co2,
                            tmp_record=tmp_record, co2_record=co2_record,
                            hum_record=hum_record
                          )
              
  except Exception as e:
    return render_template("sensor.html", latest_tmp=str(e))

#Page that serves gif
@app.route('/gif')
def gif_entry_point():
  return render_template('gif.html')

@app.route('/gif', methods = ['POST'])
def generate():

  interval = request.form['interval']
  try:
    gif_name = generate_gif(interval)
  except Exception as e:
    gif_name = str(e)

  return render_template('gif.html', gif_name=gif_name)


#Pages resposible for creating
#phenotype observation record
@app.route('/submit/<user>')
def submit_entry_point(user):
  return render_template('submit.html', user=user)

@app.route('/submit/<user>', methods=['POST'])
def submit_form(user):
  
  db_name = request.form['db_name']
  usr_name = user
  timestamp = request.form['timestamp']
  plot = request.form['timestamp']
  trial = request.form['trial']
  attribute = request.form['attribute']
  observ_type = request.form['type']
  value = request.form['value']
  unit = request.form['unit']
  uuid = request.form['uuid']
  row = ["Phenotype_Observation", timestamp, usr_name, uuid, trial, plot, attribute, observ_type, value, unit]

  try:
    rec = submit(row, db_name)
  except Exception as e:
    rec = str(e)
    
  return render_template('submit.html', rec=rec)
'''






	
	

   
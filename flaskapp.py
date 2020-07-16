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
from flask import Flask, render_template, request, send_file, jsonify

#local library
from s3 import count_img, show_latest, download_file
from user import verify_usr, save_rec, retrieve_rec
from CouchDB import sensor_latest, count_records, get_tmp_json, get_co2_json, get_hum_json
from img2gif import generate_gif
from submit import submit

app = Flask(__name__)

#The starting page
@app.route('/')
def entry_point():
  return render_template("main.html")

#no sign in page
@app.route('/visitor')
def visitor_page():
  return render_template("visitor.html")

#verify if user exist or not and render page accordingly
@app.route('/reception/<user>/<email>', methods = ['GET'])
def usr_main(user, email):
  
  if verify_usr(email) == "new":
    return render_template("new.html", user=user, email=email)
  else:
    data = retrieve_rec(email)
    school = data[0]
    device = data[1]
    return render_template("reception.html", user=user, email=email, school=school, device=device)


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







	
	

   
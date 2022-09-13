from flask import Flask , jsonify ,request, render_template,redirect,url_for,send_from_directory,flash,make_response
from sqlalchemy import create_engine, MetaData,Table,Column,Integer,String,ForeignKey
import random as r
from werkzeug.utils import secure_filename
import os
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx'}
from sqlalchemy.orm import sessionmaker
from geopy.geocoders import ArcGIS,Nominatim

from geojson import Point, Feature, FeatureCollection, dump
import numpy as np
from flask_talisman import Talisman
# CREATE THE SESSION OBJECT


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = "secret"
# If you’re using middleware or the HTTP server to serve files, you can register the download_file 
# endpoint as build_only so url_for will work without a view function.
app.add_url_rule(
    "/downloadfile/<name>", endpoint="download_file", build_only=True
)

# session_cookie_samesite=app.config["SESSION_COOKIE_SAMESITE"]

# from sqlalchemy.sql import ForeignKey,insert

engine=create_engine ('mysql://root:brainbeam@localhost/campground',echo=True)

meta= MetaData()

campground = Table(

   'campground', meta,

   Column('id', Integer, primary_key = True),
  Column('title', String(100)),
  Column('description', String(100)),
  Column('price', String(100)),
  Column('image', String(100)),
  Column('email', String(100)),
  Column('mobile', String(100)),
  Column('location', String(100)),
  Column('latitude', String(100)),
  Column('longitude', String(100)),

)

# users = Table(
#     'users',meta,
#      Column('id', Integer, primary_key = True),
#      Column('campgroundid',Integer,campground(id)),
#   Column('name', String(100)),
#   Column('password', String(100)),
# )
conn=engine.connect()

Session = sessionmaker(bind=engine)
session = Session()   

def create_table():
    meta.create_all(engine)

# create_table()
@app.route('/')

def welcome():
    return render_template('home.html')
   
@app.route('/allcampgrounds',methods=['GET','POST'])
def home():    
    stmt = campground.select()

    exe=conn.execute(stmt)

    campgroundlist =[dict(row) for row in exe]
    print(campground)
    coord = []
   
    temp = {}
    execute_map_json = session.query(campground) \
    .with_entities(campground.c.latitude, campground.c.longitude,campground.c.id,campground.c.title) \
        .filter(campground.c.id).all()
  

    for r in execute_map_json:
            lat = r.latitude
            long = r.longitude
            id = r.id
            title = r.title
            # temp =[lat,long]
            feature_map={}
            # coord.append([lat,long])
            features = [ {"type": "Feature",
                          "properties" : {
                              "id" : id,
                              "title" : title
                          },
                "geometry": {
                    "type": "Point",
                    "coordinates": [long,lat] }}
                ] 
            feature_map['fmap'] = features
            print("+f----",features)
            temp.update({'feature_map':feature_map})
            coord.append(temp.copy())
            
    feature_collection = FeatureCollection(coord)
    with open('myfile_map.geojson', 'w') as f:
        dump(feature_collection, f)
    
    print("+----",feature_collection)
    

    resp = make_response(render_template('index.html',campgrounds = campgroundlist,geo = feature_collection))
    resp.set_cookie("campground_lax",value="map_lax",samesite='Lax',secure=True)
    resp.set_cookie("campground_Strict",value="map_strict",samesite='Strict',secure=True)
    resp.set_cookie("campground",value="map",samesite=None,secure=True)
    return resp

    
    


@app.get('/newcampgroundload')
def add_campground_load():
    return render_template("new.html")
@app.post('/newcampground')

    # return render_template("adddoctors.html")
def add_new_campground():
    
    print(request.files['file'])
    print(request.url)
    print(app.config['UPLOAD_FOLDER'])
    # use secure_filename If you want to use the filename of the client to store the file on the server
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == ' ':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        uploadedfileurl = url_for('static', filename = filename)
        
        print( uploadedfileurl)
        print( filename)
    id =request.form['id']
    title = request.form['title']
    location = request.form['location']
    description = request.form['description']
    price = request.form['price']
    image =  filename
    email = request.form['email']
    mobile = request.form['mobile']
    # nom = ArcGIS()
    nom = Nominatim(user_agent="MyApp",timeout=100)
    
    data = nom.geocode(location)
    print(data)
    print(data.latitude,data.longitude)
    latitude = data.latitude
    longitude = data.longitude
    campgroundtuple=(id,title,description,price,image,email,mobile,location,latitude,longitude)
    stmt=campground.insert().values(campgroundtuple)
    exe=conn.execute(stmt)
    return render_template("new.html")
    # return "<html><body><h1>its WOrking</h1></body><html>"


           
           
@app.get('/view/<int:id>')
def view_campground(id):
  stmt=campground.select().where(campground.c.id == id)
  resultset = conn.execute(stmt)
  recordcampground = ([dict(row) for row in resultset])
  
  filename = session.query(campground) \
    .with_entities(campground.c.latitude,campground.c.longitude,campground.c.title) \
        .filter(campground.c.id == id)
  for r in filename:
        lat = r.latitude
        long = r.longitude
        title = r.title
#   return render_template('showss.html',campgroundview = recordcampground)

  features = [ {"type": "Feature",
              "geometry": {
                  "type": "Point",
                  "coordinates": [long, lat] }}
              ] 

  feature_collection = FeatureCollection(features)
  with open('myfile1.geojson', 'w') as f:
    dump(feature_collection, f)
#   print("++",latitude,longitude)
  resp = make_response(render_template('show.html',campgroundview = recordcampground, geo = feature_collection))
  resp.set_cookie("campground_lax",value="map_lax",samesite='Lax',secure=True)
  resp.set_cookie("campground_Strict",value="map_strict",samesite='Strict',secure=True)
  resp.set_cookie("campground",value="map",samesite=None,secure=True)
  return resp

# @app.route('/cookies')
# def cookie_detect():
#     resp = make_response("Cookie",200)
#     resp.set_cookie("oreo","chocolate")
#     return resp    


@app.get('/campgrounds/<int:id>/edit')
def update_doctor_load(id):

    stmt = campground.select().where(campground.c.id == id)
    resultset = conn.execute(stmt)
    recordcampground = ([dict(row) for row in resultset])
   
        
    print(recordcampground)
    if recordcampground:
         return render_template('edit.html', recordcampground= recordcampground)
            #  return redirect(url_for('update_doctor',id=id))
    return f"Employee with id ={id} Doenst exist" 


@app.post('/updatecampground/<int:id>/updated')    
def update_doctor(id):
    # id =request.form['id']
    filenames = session.query(campground) \
    .with_entities(campground.c.image) \
        .filter(campground.c.id == id).all()
    for r in filenames:
        filess = r.image
        print(filess)
    print("+++++++++++++")
    os.unlink(os.path.join(app.config['UPLOAD_FOLDER'],filess))
       
    # print("+++++++++++++")
    # print(filess)
    # print(type(filename))
    
    
  
    
    print(request.files['file'])
    print(request.url)
    print(app.config['UPLOAD_FOLDER'])
    # use secure_filename If you want to use the filename of the client to store the file on the server
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == ' ':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        uploadedfileurl = url_for('static', filename = filename)
        
        print( uploadedfileurl)
        print( filename)
    id =request.form['id']
    title = request.form['title']
    location = request.form['location']
    description = request.form['description']
    price = request.form['price']
    image =  filename
    email = request.form['email']
    mobile = request.form['mobile']
    # nom = ArcGIS()
    nom = Nominatim(user_agent="MyApp",timeout=10000)

    data = nom.geocode(location)
    print(data)
    print(data.latitude,data.longitude)
    latitude = data.latitude
    longitude = data.longitude
    campgroundtuple=(id,title,description,price,image,email,mobile,location,latitude,longitude)
    stmt = campground.update().values(campgroundtuple).where(campground.c.id == id)
    results = conn.execute(stmt)
    print(description)
    return redirect(url_for('home'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS  

@app.get('/campgrounds/<int:id>/delete')
def delete_doctor(id):
   
    # s = demoss.select(demoss.c.image).where(demoss.c.id == id)
    # filename = conn.execute(s).fetchall()
    filename = session.query(campground) \
    .with_entities(campground.c.image) \
        .filter(campground.c.id == id).all()
    for r in filename:
        files = r.image
        print(files)
        os.unlink(os.path.join(app.config['UPLOAD_FOLDER'],files))
    print("+++++++++++++")
    # print(files)
    print(type(filename))
    
    
    print("+++++++++++++")
    
    stmt = campground.delete().where(campground.c.id==id)  
    result = conn.execute(stmt)
    
    return redirect(url_for('home'))  
 
# @app.errorhandler(404)
# def page_error(error):
#     return render_template('error.html'), 404
       
if __name__ == '__main__':
    app.run(debug=True)


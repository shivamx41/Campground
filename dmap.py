from flask import Flask , jsonify ,request, render_template,redirect,url_for
import random as r


from sqlalchemy import create_engine, MetaData,Table,Column,Integer,String, Float
from geopy.geocoders import ArcGIS,Nominatim
app = Flask(__name__)
nom = ArcGIS()



engine = create_engine('mysql://root:brainbeam@localhost/demo', echo = True)
meta = MetaData()

campground = Table(
   'campground', meta, 
   Column('id', Integer, primary_key = True), 
   Column('title', String(30)), 
   Column('description', String(60)),
   Column('image', String(60)),
   Column('price', String(20)),
   Column('email', String(20)),
   Column('mobile', String(20)),
   Column('location', String(60)),
   Column('latitude',Float(30)),
   Column('lantitude', Float(30))
)


conn = engine.connect()

def create_table():
    meta.create_all(engine)
    
    
@app.route('/')
def welcome():
    return render_template("demo.html")


@app.get('/campgrounds')
def display_all_campgrounds():
  
 
    return render_template("displayallcampground.html")

@app.post('/newcampground')
def new_campground():
   
        return render_template("newcampground.html")
    
            
    
# create_table()
if __name__ == '__main__':
    app.run(debug=True)
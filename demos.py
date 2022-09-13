from geojson import Point, Feature, FeatureCollection, dump
from geopy.geocoders import ArcGIS,Nominatim

nom = Nominatim(user_agent="MyApp")

data = nom.geocode('ladak,india')
print(data)
print(data.latitude,data.longitude)
lat = data.latitude
lon = data.longitude 
features = [ {"type": "Feature",
              "geometry": {
                  "type": "Point",
                  "coordinates": [lon, lat] }}
              ] 

feature_collection = FeatureCollection(features)
with open('myfile1.geojson', 'w') as f:
   dump(feature_collection, f)
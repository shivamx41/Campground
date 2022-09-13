from geojson import Point, Feature, FeatureCollection, dump
from geopy.geocoders import ArcGIS,Nominatim

nom = Nominatim(user_agent="MyApp")

data = nom.geocode('ladak,india')
print(data)
print(data.latitude,data.longitude)
latitude = data.latitude
longitude = data.longitude
x = list(latitude,longitude)
point = Point(x)

features = []
features.append(Feature(geometry=point, properties={"country": "Spain"}))

# add more features...
# features.append(...)

feature_collection = FeatureCollection(features)
with open('myfile.geojson', 'w') as f:
   dump(feature_collection, f)
<script>

var title = '{{campgroundview.title}}'
var location = '{{campgroundview.location}}'
var latitude = '{{campgroundview.latitude}}'
var longitude = '{{campgroundview.longitude}}'
document.write(title,location,latitude,longitude);
document.write( '{{geo.features[0].geometry.coordinates}}')
// TO MAKE THE MAP APPEAR YOU MUST
// ADD YOUR ACCESS TOKEN FROM
// https://account.mapbox.com


    </script>
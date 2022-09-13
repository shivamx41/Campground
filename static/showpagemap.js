
var title = '{{campgroundview.title}}'
var location = '{{campgroundview.location}}'
var latitude = '{{campgroundview.latitude}}'
var longitude = '{{campgroundview.longitude}}'

// TO MAKE THE MAP APPEAR YOU MUST
// ADD YOUR ACCESS TOKEN FROM
// https://account.mapbox.com

mapboxgl.accessToken = 'pk.eyJ1Ijoic2l2YXNhdGhpdmVsIiwiYSI6ImNsN2VteWlmcTAxeWkzdm1qcWc3OHV2YzUifQ.dm2a4GX3Z_Q73bJL_K-o1g';
const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/light-v10', // stylesheet location
  center: [latitude,longitude],// starting position [lng, lat]
  zoom: 10 // starting zoom
});

map.addControl(new mapboxgl.NavigationControl());


new mapboxgl.Marker()
  .setLngLat([latitude,longitude])
  .setPopup(
      new mapboxgl.Popup({ offset: 25 })
          .setHTML(
              `<h3>{{campground.title}}</h3><p>{{campground.location}}</p>`
          )
  )
  .addTo(map)
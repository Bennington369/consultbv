// Obtén la longitud y latitud de la base de datos
const latitud = document.getElementById('latitud');
const longitud = document.getElementById('longitud');
const savedLat = 18.450132805098548
const savedLng = -96.35559824942904

console.log(`savedLat: ${savedLat}, savedLng: ${savedLng}`);

// Crea un objeto con la longitud y latitud guardada o la ubicación predeterminada
const mylatlng = latitud.value && longitud.value ? { lng: parseFloat(longitud.value), lat: parseFloat(latitud.value) } : { lng: -96.36174562241521, lat: 18.447529051044782 };

console.log(`mylatlng: ${mylatlng.lng}, ${mylatlng.lat}`);

mapboxgl.accessToken = 'pk.eyJ1IjoiYmVubmluZ3RvbiIsImEiOiJjbDI5a3JhaDYwMDVzM2NvNjJzOGt0bGZjIn0.4Yohr0bYdPLqpiekKEuGQw';
const map = new mapboxgl.Map({
  container: 'map', // container ID
  style: 'mapbox://styles/mapbox/streets-v11', // style URL
  center: mylatlng, // starting position [lng, lat]
  zoom: 14 // starting zoom
});

// Crea el marcador y establece su posición en la longitud y latitud guardada o la ubicación predeterminada
const marker = new mapboxgl.Marker({ draggable: true })
  .setLngLat(mylatlng)
  .addTo(map);

// Agrega un event listener al marcador
marker.on('dragend', onDragEnd);

// Crea el control de ubicación
var geolocate = new mapboxgl.GeolocateControl({
  positionOptions: {
    enableHighAccuracy: true
  },
  trackUserLocation: true
});

// Agrega el control de ubicación al mapa
map.addControl(geolocate);

// Función que se ejecuta cuando el usuario arrastra el marcador
function onDragEnd() {
  const lng = marker.getLngLat().lng;
  const lat = marker.getLngLat().lat;
  console.log(`Longitud: ${lng}, Latitud: ${lat}`);
  longitud.value = lng;
  latitud.value = lat;
}



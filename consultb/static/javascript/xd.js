

// Obtiene los elementos de la página
const latitud = document.getElementById('latitud');
const longitud = document.getElementById('longitud');
const mapContainer = document.getElementById('map');
const locateUserBtn = document.getElementById('locateUserBtn');
const MOBILE_BREAKPOINT = 768;
let directionsControl;
var size = window.matchMedia("(max-width: 600px)");

// Define el token de acceso a Mapbox
mapboxgl.accessToken = 'pk.eyJ1IjoiYmVubmluZ3RvbiIsImEiOiJjbDI5a3JhaDYwMDVzM2NvNjJzOGt0bGZjIn0.4Yohr0bYdPLqpiekKEuGQw';

// Crea el mapa con las opciones de configuración
const map = new mapboxgl.Map({
  container: mapContainer,
  style: 'mapbox://styles/mapbox/streets-v11',
  center: [longitud.value, latitud.value],
  zoom: 15
});




// Agrega el marcador de la ubicación guardada
const marker = new mapboxgl.Marker({
  draggable: false
}).setLngLat([longitud.value, latitud.value]).addTo(map);

// Agrega controles de navegación al mapa
const nav = new mapboxgl.NavigationControl({
  visualizePitch: true
});
map.addControl(nav, 'bottom-right');

// Agrega el control de geolocalización al mapa
const geolocate = new mapboxgl.GeolocateControl({
  positionOptions: {
    enableHighAccuracy: true
  },
  trackUserLocation: true
});
map.addControl(geolocate);


// variable global para almacenar la instancia de MapboxDirections
var directions;

function initializeMap() {
  // código para inicializar el mapa

  // crea la instancia de MapboxDirections
  directions = new MapboxDirections({
    accessToken: mapboxgl.accessToken,
    unit: 'metric',
    profile: 'mapbox/driving',
    language: 'es',
    controls: {
      inputs: size.matches ? {} : {
      instructions: true,
      inputs: true,
      profileSwitcher: true
  },
  instructions: !size.matches
},
placeholderOrigin: 'Origen',
placeholderDestination: 'Destino'
  });

  // agrega el control de direcciones al mapa
  map.addControl(directions, 'top-left');

  // código para manejar el evento 'click' del botón
}

function resize() {
  // verifica si el control de direcciones ya existe
  if (directions._container) {
    // redimensiona el mapa para ajustarse a la nueva ventana
    map.resize();

    // actualiza la posición del control de direcciones
    var screenSize = window.innerWidth;
    if (screenSize < 576) {
      directions._container.style.width = '10px';
      directions._container.style.height = '10px';
    } else {
      directions._container.style.width = '10px';
      directions._container.style.height = 'auto';
    }
  }
}

// llama a la función 'initializeMap' cuando se carga la página
initializeMap();

// agrega un evento 'resize' para manejar los cambios de tamaño de la ventana
window.addEventListener('resize', resize);


// Agrega un evento al botón de ubicación del usuario
locateUserBtn.addEventListener('click', () => {
    // Elimina la ruta anterior, si la hubiera
    if (map.getLayer('route') && map.getSource('route')) {
        // Elimina la ruta anterior
        map.removeLayer('route');
        map.removeSource('route');
      }
    
  
    // Obtiene la ubicación actual del usuario
    navigator.geolocation.getCurrentPosition(position => {
      // Obtiene la latitud y longitud de la ubicación actual del usuario
      const { longitude, latitude } = position.coords;
  
      // Muestra la ubicación actual del usuario en el mapa
      const userLocationMarker = new mapboxgl.Marker({
        draggable: false
      }).setLngLat([longitude, latitude]).addTo(map);
  
      // Crea una fuente para la ruta entre la ubicación actual del usuario y el marcador guardado
      directions.setOrigin([longitude, latitude]);
      directions.setDestination([longitud.value, latitud.value]);
      if (!mapboxgl.getControl('directions')) {
        map.addControl(directions, 'top-left');
      }
    });
  });


    



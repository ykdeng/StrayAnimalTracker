import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

interface Location {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
}

interface MapProps {
  locations: Location[];
}

const Map: React.FC<MapProps> = ({ locations }) => {
  const mapRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (mapRef.current) {
      const map = L.map(mapRef.current).setView([0, 0], 13);

      L.tileLayer(`https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=${process.env.REACT_APP_MAPBOX_TOKEN}`, {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: process.env.REACT_APP_MAPBOX_TOKEN,
      }).addTo(map);

      locations.forEach(location => {
        const marker = L.marker([location.latitude, location.longitude]).addTo(map);
        
        marker.bindPopup(`<b>${location.name}</b>`, {closeOnClick: true, autoClose: false});
      });

      const group = new L.featureGroup(locations.map(location => L.marker([location.latitude, location.longitude])));
      map.fitBounds(group.getBounds());
    }
  }, [locations]);

  return <div ref={mapRef} style={{ height: '500px', width: '100%' }}></div>;
};

export default Map;
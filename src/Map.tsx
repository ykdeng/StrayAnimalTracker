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
  const mapInstance = useRef<L.Map | null>(null);
  const markersRef = useRef<L.Marker[]>([]);

  useEffect(() => {
    if (mapRef.current && !mapInstance.current) {
      mapInstance.current = L.map(mapRef.current).setView([0, 0], 13);
      L.tileLayer(`https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=${process.env.REACT_APP_MAPBOX_TOKEN}`, {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: process.env.REACT_APP_MAPBOX_TOKEN,
      }).addTo(mapInstance.current);
    }
  }, []); // Initialize the map only once

  useEffect(() => {
    if (mapInstance.current) {
      // Clear existing markers
      markersRef.current.forEach(marker => marker.remove());
      markersRef.current = [];
      
      // Add new markers and adjust bounds
      const newMarkers: L.Marker[] = locations.map(location => {
        const marker = L.marker([location.latitude, location.longitude]).addTo(mapInstance.current as L.Map);
        marker.bindPopup(`<b>${location.name}</b>`, { closeOnClick: true, autoClose: false });
        return marker;
      });
      markersRef.current = newMarkers;

      const group = new L.featureGroup(newMarkers);
      mapInstance.current.fitBounds(group.getBounds());
    }
  }, [locations]);  // Only re-run if locations change

  return <div ref={mapRef} style={{height: '500px', width: '100%'}}></div>;
};

export default Map;
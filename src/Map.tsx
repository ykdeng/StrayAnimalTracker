import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

interface AnimalLocation {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
}

interface AnimalMapProps {
  locations: AnimalLocation[];
}

const AnimalMap: React.FC<AnimalMapProps> = ({ locations }) => {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const leafletMapRef = useRef<L.Map | null>(null);
  const animalMarkersRef = useRef<L.Marker[]>([]);

  useEffect(() => {
    if (mapContainerRef.current && !leafletMapRef.current) {
      leafletMapRef.current = L.map(mapContainerRef.current).setView([0, 0], 13);
      L.tileLayer(`https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=${process.env.REACT_APP_MAPBOX_TOKEN}`, {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: process.env.REACT_G_APP_MAPBOX_TOKEN,
      }).addTo(leafletMapRef.current);
    }
  }, []);

  useEffect(() => {
    if (leafletMapRef.current) {
      animalMarkersRef.current.forEach(marker => marker.remove());
      animalMarkersRef.current = [];
      
      const newAnimalMarkers: L.Marker[] = locations.map(animalLocation => {
        const marker = L.marker([animalLocation.latitude, animalLocation.longitude])
                          .addTo(leafletMapRef.current as L.Map);
        marker.bindPopup(`<b>${animalLocation.name}</b>`, { closeOnClick: true, autoClose: false });
        return marker;
      });
      animalMarkersRef.current = newAnimalMarkers;

      const markersGroup = new L.featureGroup(newAnimalMarkers);
      leafletMapRef.current.fitBounds(markersGroup.getBounds());
    }
  }, [locations]);

  return <div ref={mapContainerRef} style={{height: '500px', width: '100%'}}></div>;
};

export default AnimalMap;

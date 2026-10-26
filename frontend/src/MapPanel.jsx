import React from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
const places = [
  { name: 'Hyderabad — illustration', at: [17.385, 78.4867] },
  { name: 'Gachibowli — illustration', at: [17.4401, 78.3489] },
  { name: 'Secunderabad — illustration', at: [17.4399, 78.4983] },
];
export default function MapPanel() {
  return (
    <div className="map-frame">
      <MapContainer center={[17.415, 78.45]} zoom={11} scrollWheelZoom={false} className="map">
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {places.map(place => (
          <CircleMarker key={place.name} center={place.at} radius={9}
            pathOptions={{ color: '#3b82f6', fillColor: '#a8c8fc', fillOpacity: 0.8 }}>
            <Popup>{place.name}<br />Not a forecast, alert, or real incident.</Popup>
          </CircleMarker>
        ))}
      </MapContainer>
      <div className="map-overlay">ILLUSTRATIVE LOCATIONS ONLY · NO LIVE HAZARD DATA</div>
    </div>
  );
}

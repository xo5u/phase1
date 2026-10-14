
import { useState } from 'react'
import {
  MapContainer,
  TileLayer,
  Marker,
  useMapEvents,
} from 'react-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Fix the default marker icon paths in Vite
import markerIcon from 'leaflet/dist/images/marker-icon.png'
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png'
import markerShadow from 'leaflet/dist/images/marker-shadow.png'

const defaultIcon = L.icon({
  iconUrl: markerIcon,
  iconRetinaUrl: markerIcon2x,
  shadowUrl: markerShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
})

function LocationSelector({ position, onLocationChange }) {
  useMapEvents({
    click(event) {
      onLocationChange({
        latitude: Number(event.latlng.lat.toFixed(5)),
        longitude: Number(event.latlng.lng.toFixed(5)),
      })
    },
  })

  return <Marker position={position} icon={defaultIcon} />
}

export default function LocationMap({
  latitude,
  longitude,
  onLocationChange,
}) {
  const position = [latitude, longitude]

  return (
    <div className="location-map">
      <MapContainer
        center={position}
        zoom={10}
        scrollWheelZoom={true}
        attributionControl={false}
        style={{ height: '300px', width: '100%' }}
      >
        
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        <LocationSelector
          position={position}
          onLocationChange={onLocationChange}
        />
      </MapContainer>
    </div>
  )
}

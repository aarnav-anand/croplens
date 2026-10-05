import React, { useEffect, useRef } from 'react';
import L from 'leaflet';

interface ReportMapProps {
  onLocationSelect: (lat: number, lng: number) => void;
  selectedLocation: { lat: number; lng: number } | null;
  mapCaption: string;
}

export const ReportMap: React.FC<ReportMapProps> = ({
  onLocationSelect,
  selectedLocation,
  mapCaption,
}) => {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);
  const markerRef = useRef<L.Marker | null>(null);

  useEffect(() => {
    if (!mapContainerRef.current || mapInstanceRef.current) return;

    // Fix default marker icon in Leaflet
    delete (L.Icon.Default.prototype as any)._getIconUrl;
    L.Icon.Default.mergeOptions({
      iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
      iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
      shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
    });

    const initialLat = selectedLocation?.lat || 20.5937;
    const initialLng = selectedLocation?.lng || 78.9629;
    const initialZoom = selectedLocation ? 12 : 5;

    const map = L.map(mapContainerRef.current, {
      center: [initialLat, initialLng],
      zoom: initialZoom,
      zoomControl: true,
    });

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; OpenStreetMap contributors',
    }).addTo(map);

    mapInstanceRef.current = map;

    // Handle clicks to place/move marker
    map.on('click', (e: L.LeafletMouseEvent) => {
      const { lat, lng } = e.latlng;
      if (markerRef.current) {
        markerRef.current.setLatLng([lat, lng]);
      } else {
        markerRef.current = L.marker([lat, lng]).addTo(map);
      }
      onLocationSelect(lat, lng);
    });

    if (selectedLocation) {
      markerRef.current = L.marker([selectedLocation.lat, selectedLocation.lng]).addTo(map);
    }

    return () => {
      map.remove();
      mapInstanceRef.current = null;
    };
  }, []);

  return (
    <div className="w-full space-y-2">
      <div className="flex items-center justify-between">
        <span className="text-xs text-slate-400">{mapCaption}</span>
      </div>

      <div
        ref={mapContainerRef}
        className="w-full h-[320px] rounded-xl overflow-hidden border border-slate-700/60 shadow-inner z-0"
      />

      {selectedLocation && (
        <div className="text-xs text-emerald-400 flex items-center gap-2 bg-emerald-950/40 px-3 py-1.5 rounded-lg border border-emerald-500/20">
          <span>📍 Selected Coordinates:</span>
          <span className="font-mono">{selectedLocation.lat.toFixed(4)}°, {selectedLocation.lng.toFixed(4)}°</span>
        </div>
      )}
    </div>
  );
};

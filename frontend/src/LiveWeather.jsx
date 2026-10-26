import React, { useState } from 'react';
import { CloudRain, MapPin, RefreshCcw, ShieldAlert } from 'lucide-react';
import { api } from './api.js';

const defaultCoordinates = { latitude: 17.38, longitude: 78.48 };

export default function LiveWeather() {
  const [coords, setCoords] = useState(defaultCoordinates);
  const [data, setData] = useState(null);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  async function lookup(e) {
    e.preventDefault();
    setData(null);
    setError('');
    setBusy(true);
    try {
      const query = new URLSearchParams({
        latitude: String(coords.latitude), longitude: String(coords.longitude),
      });
      const result = await api('/api/v1/weather/live?' + query);
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return <div>
    <div className="page-heading">
      <div>
        <div className="eyebrow">EXTERNAL MODELED WEATHER · NON-OFFICIAL</div>
        <h1>Weather data explorer</h1>
        <p>Look up gridded weather from Open-Meteo. Coordinates are rounded before being sent to the provider.</p>
      </div>
    </div>
    <div className="notice notice-warning">
      <ShieldAlert size={18} /> <span>
        Modeled weather is not a station measurement or verified disaster warning.
        This data is separate from the experimental risk estimator and must not be treated as proof of safety.
      </span>
    </div>
    <div className="columns-two">
      <section className="card">
        <div className="card-head"><div><h3><MapPin size={18}/> Location coordinates</h3><p>Hyderabad demo defaults; no device location permission requested</p></div></div>
        <form onSubmit={lookup} className="form-grid">
          <label>Latitude<input aria-label="Latitude" type="number" min="-90" max="90" step="0.0001" required
            value={coords.latitude} onChange={e => setCoords(x => ({...x, latitude: e.target.value}))} /></label>
          <label>Longitude<input aria-label="Longitude" type="number" min="-180" max="180" step="0.0001" required
            value={coords.longitude} onChange={e => setCoords(x => ({...x, longitude: e.target.value}))} /></label>
          <div className="actions full"><button className="primary" type="submit" disabled={busy}>
            <RefreshCcw size={16}/>{busy ? 'Fetching provider data...' : 'Fetch modeled weather'}
          </button></div>
        </form>
        {error && <div className="notice notice-warning" role="alert">
          <ShieldAlert size={16}/><span>{error}. If not enabled, set OPEN_METEO_ENABLED=true in the backend environment.</span>
        </div>}
        <p className="muted">Each click requests a third-party provider through the local API. The free endpoint is intended for non-commercial use; attribution and provider terms apply.</p>
      </section>
      <section className="card" aria-live="polite">
        <div className="card-head"><div><h3><CloudRain size={18}/> Source-backed weather panel</h3><p>Shows provenance and timestamps; never an official alert</p></div></div>
        {!data ? <div className="empty-state"><CloudRain size={36}/><h3>No modeled data loaded</h3><p>Choose coordinates and fetch the provider response.</p></div> : <>
          <div className="weather-facts">
            <div><small>Temperature</small><strong>{data.temperature_c} °C</strong></div>
            <div><small>Humidity</small><strong>{data.humidity_pct}%</strong></div>
            <div><small>24h modeled precipitation</small><strong>{data.modeled_precipitation_24h_mm} mm</strong></div>
            <div><small>Provider report age</small><strong>{data.age_hours} h</strong></div>
          </div>
          <dl className="kv">
            <div><dt>Model timestamp (UTC)</dt><dd>{data.source_timestamp_utc}</dd></div>
            <div><dt>Approximate coordinates</dt><dd>{data.latitude_approx}, {data.longitude_approx}</dd></div>
            <div><dt>Cache</dt><dd>{data.cache_hit ? 'Cached up to 10 min' : 'New provider response'}</dd></div>
            <div><dt>Official warning</dt><dd>No</dd></div>
          </dl>
          <div className="notice notice-warning"><ShieldAlert size={16}/><span>{data.note}</span></div>
          <div className="source-reference"><b>Data attribution</b>
            <a href={data.provider_url} target="_blank" rel="noopener noreferrer">Weather data by Open-Meteo</a>
            <a href={data.license_url} target="_blank" rel="noopener noreferrer">CC BY 4.0 license</a>
          </div>
        </>}
      </section>
    </div>
  </div>;
}

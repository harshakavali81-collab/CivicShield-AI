import React, { useEffect, useState } from 'react';
import { AlertTriangle, BookOpen, ExternalLink, Search, ShieldCheck } from 'lucide-react';
import { api } from './api.js';

export default function OfficialSources() {
  const [id, setId] = useState('573');
  const [status, setStatus] = useState(null);
  const [bulletin, setBulletin] = useState(null);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    api('/api/v1/official/integration-status').then(setStatus).catch(() => {});
  }, []);

  async function fetchBulletin(e) {
    e.preventDefault(); setBusy(true); setError(''); setBulletin(null);
    try {
      const result = await api('/api/v1/official/imd/district-warning?district_id=' + encodeURIComponent(id));
      setBulletin(result);
    } catch (err) { setError(err.message); }
    finally { setBusy(false); }
  }

  return <section>
    <div className="page-heading"><div>
      <div className="eyebrow">GOVERNMENT REFERENCE SYSTEMS</div>
      <h1>Official source connections</h1>
      <p>View connection status and, only when authorized and enabled, retrieve an IMD district bulletin.</p>
    </div></div>
    <div className="notice notice-warning"><AlertTriangle size={18}/><span>
      If a feed is disconnected or unavailable, this means <b>unknown</b>, never safe.
      Refer to government websites for authoritative advisories.
    </span></div>
    <div className="columns-two">
      <div className="card">
        <div className="card-head"><div><h3><ShieldCheck size={18}/> IMD district warning adapter</h3><p>Source: api.imd.gov.in · operator must have permitted access</p></div></div>
        <p className="muted">IMD API connection: {status?.imd?.enabled ? 'Enabled by operator (access not independently verified)' : 'Not enabled / unknown'}</p>
        <form onSubmit={fetchBulletin} className="inline-controls">
          <input aria-label="Official IMD district ID" type="number" min="1" max="999999"
            value={id} onChange={e=>setId(e.target.value)} required />
          <button type="submit" className="secondary" disabled={busy || !status?.imd?.enabled}>
            <Search size={15}/>{busy ? 'Checking...' : 'Request bulletin'}
          </button>
        </form>
        {error && <div className="notice notice-warning" role="alert">{error}. Check original IMD site instead.</div>}
        {bulletin && <div aria-live="polite">
          <h3>{bulletin.district} — direct-source response</h3>
          <p className="muted">Issued (UTC): {bulletin.issued_at_utc}. Age: {bulletin.age_hours} h. NOT an endorsement of this app.</p>
          <div className="report-list">{bulletin.days.map(day=><div className="report" key={day.day}>
            <div className="report-top"><b>Day {day.day}</b><span className="subtle-pill">{day.color} source code</span></div>
            <p>{day.phenomena.join(', ')}</p></div>)}</div>
          <p className="muted">Always compare against the original IMD bulletin and valid issue times.</p>
          <div className="sources"><a href={bulletin.original_source_url} target="_blank" rel="noopener noreferrer">
            Original IMD record <ExternalLink size={13}/></a></div>
        </div>}
        <div className="sources"><a href="https://mausam.imd.gov.in/" target="_blank" rel="noopener noreferrer">IMD official website <ExternalLink size={13}/></a>
        <a href="https://api.imd.gov.in/public/api_reference.html" target="_blank" rel="noopener noreferrer">API reference <ExternalLink size={13}/></a></div>
      </div>
      <div className="card">
        <div className="card-head"><div><h3><BookOpen size={18}/> CWC flood forecast references</h3><p>Official websites only; no CWC machine API connected</p></div></div>
        <div className="notice notice-warning"><AlertTriangle size={16}/><span>
          CWC status: {status?.cwc?.api_connected === false ? 'Not connected' : 'Unverified'}.
          Do not interpret this as an absence of flood alerts.
        </span></div>
        <p className="muted">Visit CWC directly for station-specific flood forecasts and basin advisories.
          This project does not extract, translate, or verify those warnings.</p>
        <div className="sources">
          <a href="https://ffs.india-water.gov.in/" target="_blank" rel="noopener noreferrer">CWC forecasts <ExternalLink size={13}/></a>
          <a href="https://aff.india-water.gov.in/" target="_blank" rel="noopener noreferrer">Advisory forecasts <ExternalLink size={13}/></a>
          <a href="https://cwc.gov.in/" target="_blank" rel="noopener noreferrer">CWC homepage <ExternalLink size={13}/></a>
        </div>
      </div>
    </div>
  </section>;
}

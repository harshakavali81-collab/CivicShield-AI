import React, { useEffect, useState } from 'react';
import {
  Activity, AlertTriangle, BarChart3, BookOpen, CheckCircle2, ChevronRight,
  CloudRain, Database, FileWarning, Globe, LayoutDashboard, LockKeyhole,
  MapPinned, Menu, MessageCircle, PlusCircle, RefreshCcw, Search, ShieldCheck, X,
} from 'lucide-react';
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { api } from './api.js';
import { oidcConfigured, authManager, readOidcUser, loginWithOidc, logoutLocally } from './auth.js';
import MapPanel from './MapPanel.jsx';
import LiveWeather from './LiveWeather.jsx';
import KnowledgeSearch from './KnowledgeSearch.jsx';
import OfficialSources from './OfficialSources.jsx';
import Diagnostics from './Diagnostics.jsx';
import ScenarioLab from './ScenarioLab.jsx';

const riskDefaults = { city: 'Hyderabad', rainfall_24h_mm: 68, temperature_c: 29, humidity_pct: 85, forecast_age_hours: 1 };
const categories = { flooding: 'Flood / waterlogging', fallen_tree: 'Fallen tree', road_block: 'Road block', heat: 'Heat', other: 'Other' };
const languages = { en: 'English', te: 'తెలుగు', hi: 'हिन्दी', ta: 'தமிழ்', kn: 'ಕನ್ನಡ' };
const nav = [
  ['dashboard', LayoutDashboard, 'Overview'],
  ['risk', CloudRain, 'Risk explorer'],
  ['scenario', Activity, 'Scenario lab'],
  ['weather', CloudRain, 'Modeled weather'],
  ['official', ShieldCheck, 'Official sources'],
  ['map', MapPinned, 'Illustrative map'],
  ['assistant', MessageCircle, 'Safety guidance'],
  ['report', FileWarning, 'Report an incident'],
  ['review', ShieldCheck, 'Responder review'],
  ['diagnostics', Activity, 'System diagnostics'],
];

function Notice({ type = 'info', children }) { return <div className={'notice notice-' + type}><AlertTriangle size={17} /> <span>{children}</span></div>; }
function Spinner() { return <span className="spinner" aria-label="Loading" />; }
function Card({ title, subtitle, icon: Icon, children, action, className = '' }) {
  return <section className={'card ' + className}>
    {(title || action) && <div className="card-head"><div><h3>{Icon && <Icon size={18} />} {title}</h3>{subtitle && <p>{subtitle}</p>}</div>{action}</div>}
    {children}
  </section>;
}
function Metric({ label, value, detail, icon: Icon }) { return <div className="metric"><div className="metric-icon"><Icon size={21} /></div><span>{label}</span><strong>{value}</strong><small>{detail}</small></div>; }
function Sources() { return <div className="sources">
  <a target="_blank" rel="noopener noreferrer" href="https://mausam.imd.gov.in/">IMD <ChevronRight size={13} /></a>
  <a target="_blank" rel="noopener noreferrer" href="https://ndma.gov.in/">NDMA <ChevronRight size={13} /></a>
  <a target="_blank" rel="noopener noreferrer" href="https://cwc.gov.in/">CWC <ChevronRight size={13} /></a>
</div>; }
function Dashboard({ onNavigate }) {
  const [summary, setSummary] = useState(null);
  const [trends, setTrends] = useState(null);
  const [error, setError] = useState('');
  useEffect(() => {
    Promise.all([api('/api/v1/analytics/summary'), api('/api/v1/analytics/trends')])
      .then(([a, b]) => { setSummary(a); setTrends(b); }).catch(err => setError(err.message));
  }, []);
  return <>
    <div className="page-heading"><div><div className="eyebrow">PUBLIC SAFETY INTELLIGENCE · RESEARCH DEMO</div><h1>Situation overview</h1><p>Explore experimental indicators and sample visuals. Not a real-time emergency dashboard.</p></div><button className="primary" onClick={() => onNavigate('scenario')}>Explore fictional case study <ChevronRight size={17} /></button></div>
    <Notice type="warning">No live government alert feed is connected. An empty alert list never means an area is safe.</Notice>
    {error && <Notice type="warning">Backend unavailable: {error}. Start the FastAPI server.</Notice>}
    <div className="metrics">
      <Metric label="Stored local reports" value={summary?.report_total ?? '—'} detail="Demo database only" icon={FileWarning} />
      <Metric label="Pending review" value={summary?.by_status?.pending ?? 0} detail="Awaiting human decision" icon={RefreshCcw} />
      <Metric label="Official feed" value="Not linked" detail="No live warnings ingested" icon={Globe} />
      <Metric label="Risk model" value="Demo" detail="Unvalidated heuristic by default" icon={Activity} />
    </div>
    <div className="columns-two">
      <Card title="Locally submitted reports" subtitle="Actual stored report totals — not verified incidents" icon={BarChart3}>
        <div className="chart-wrap">{trends ? <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={trends.data}><defs><linearGradient id="trendGradient" x1="0" x2="0" y1="0" y2="1"><stop offset="0%" stopColor="#367cf5" stopOpacity={0.35}/><stop offset="100%" stopColor="#367cf5" stopOpacity={0.01}/></linearGradient></defs>
          <CartesianGrid stroke="#e9eef6" strokeDasharray="3 3"/><XAxis dataKey="date" tick={{fontSize:10}} tickFormatter={v => v.slice(5)}/><YAxis allowDecimals={false} tick={{fontSize:11}}/><Tooltip/><Area type="monotone" dataKey="reports" stroke="#367cf5" strokeWidth={3} fill="url(#trendGradient)" />
          </AreaChart></ResponsiveContainer> : <Spinner />}</div>
      </Card>
      <Card title="Reference locations" subtitle="Three illustrative Hyderabad points — not risk sites" icon={MapPinned}>
        <MapPanel />
      </Card>
    </div>
    <div className="columns-two">
      <Card title="Research workflow" subtitle="How CivicShield AI separates information from decisions" icon={Database}>
        <div className="steps">{['Validate submitted conditions and source freshness','Generate an explicitly experimental risk indicator','Provide curated educational guidance and reference links','Queue citizen reports for authorized human review'].map((s,i)=><div className="step" key={s}><b>{i+1}</b><span>{s}</span></div>)}</div>
      </Card>
      <Card title="Official information bookmarks" subtitle="Visit original government sources for real warnings" icon={BookOpen}>
        <p className="muted">This application does not republish or confirm the current status of government warnings. Consult authoritative sources directly.</p><Sources />
        <button className="secondary wide" onClick={() => onNavigate('assistant')}>Open multilingual guidance <ChevronRight size={16} /></button>
      </Card>
    </div>
  </>;
}
function RiskExplorer() {
  const [fields, setFields] = useState(riskDefaults), [result, setResult] = useState(null);
  const [busy, setBusy] = useState(false), [error, setError] = useState('');
  function change(name, value) { setFields(old => ({...old, [name]: name === 'city' ? value : Number(value)})); }
  async function submit(e) { e.preventDefault(); setBusy(true); setError(''); setResult(null);
    try { setResult(await api('/api/v1/risk/estimate', { method:'POST', body:JSON.stringify(fields) })); } catch (err) { setError(err.message); } finally { setBusy(false); }
  }
  return <>
    <div className="page-heading"><div><div className="eyebrow">EXPERIMENTAL WEATHER INDICATORS</div><h1>Risk explorer</h1><p>Test a weather-input example. Results are not a forecast or warning.</p></div></div>
    <Notice type="warning">The default example values are invented; even a lower indicator does not establish safety. Conditions are not fetched live.</Notice>
    <div className="columns-two">
      <Card title="Input conditions" subtitle="Synthetic example unless you enter your own observed data" icon={CloudRain}>
        <form onSubmit={submit} className="form-grid">
          <label className="full">City or locality<input value={fields.city} minLength={2} maxLength={80} onChange={e=>change('city',e.target.value)} required /></label>
          {[
            ['rainfall_24h_mm', 'Rainfall (24 hours, mm)', 0, 1000],
            ['temperature_c', 'Temperature (°C)', -40, 65],
            ['humidity_pct', 'Relative humidity (%)', 0, 100],
            ['forecast_age_hours', 'Input age (hours)', 0, 720],
          ].map(([key, label, min, max]) => <label key={key}>{label}<input type="number" required step="any" min={min} max={max} value={fields[key]} onChange={e=>change(key,e.target.value)} /></label>)}
          <div className="actions full"><button type="submit" className="primary" disabled={busy}>{busy ? 'Evaluating...' : 'Evaluate demo input'} <ChevronRight size={16}/></button><button type="button" className="secondary" onClick={()=>{setFields(riskDefaults);setResult(null)}}>Reset example</button></div>
        </form>
        {error && <Notice type="warning">{error}</Notice>}
      </Card>
      <Card title="Experimental result" subtitle="This does not replace an official meteorological advisory" icon={Activity}>
        {!result ? <div className="empty-state"><Activity size={38} /><h3>No estimate yet</h3><p>Enter sample conditions and select “Evaluate demo input”.</p></div> : <>
          <div className="result-label">ILLUSTRATIVE INDICATOR</div><div className="risk-result"><span className={'risk-chip ' + (result.data_stale ? 'risk-stale' : 'risk-active')}>{result.risk_level.replaceAll('_',' ')}</span></div>
          <dl className="kv"><div><dt>Mode</dt><dd>{result.model_mode.replaceAll('_',' ')}</dd></div><div><dt>Data freshness</dt><dd>{result.data_stale ? 'STALE / unavailable' : 'Input age accepted'}</dd></div><div><dt>Official warning</dt><dd>No</dd></div>{result.model_score !== null && <div><dt>Uncalibrated score</dt><dd>{result.model_score}</dd></div>}</dl>
          <ul className="result-notes">{result.explanation.map(s=><li key={s}>{s}</li>)}</ul>
          <Notice type="warning">{result.warning}</Notice>
        </>}
      </Card>
    </div>
  </>;
}
function SafetyAssistant() {
  const [language, setLanguage] = useState('en'), [question, setQuestion] = useState('What should I do during a flood?');
  const [result, setResult] = useState(null), [busy, setBusy] = useState(false), [error, setError] = useState('');
  async function submit(e) {e.preventDefault();setBusy(true);setError('');
    try {setResult(await api('/api/v1/assistant/ask',{method:'POST',body:JSON.stringify({question,language})}));}catch(err){setError(err.message);}finally{setBusy(false);}
  }
  return <>
    <div className="page-heading"><div><div className="eyebrow">FIVE LANGUAGES · EDUCATIONAL GUIDANCE</div><h1>Multilingual safety guide</h1><p>Short, curated preparedness summaries with official-source bookmarks.</p></div></div>
    <Notice>This is a topic-matching guide, not an LLM, live RAG service, or an emergency responder. Always verify local notices.</Notice>
    <div className="columns-two">
      <Card title="Ask about preparedness" icon={MessageCircle}>
        <form onSubmit={submit} className="stack">
          <label>Response language<select value={language} onChange={e=>setLanguage(e.target.value)}>{Object.entries(languages).map(([v,l])=><option value={v} key={v}>{l}</option>)}</select></label>
          <label>Your question<textarea minLength={2} maxLength={300} rows={5} value={question} onChange={e=>setQuestion(e.target.value)} placeholder="Ask about flood preparedness, heat safety or emergencies..." required /></label>
          <button className="primary" disabled={busy} type="submit">{busy ? 'Looking up guidance...' : 'Get educational guidance'} <Search size={17}/></button>
        </form>
        {error && <Notice type="warning">{error}</Notice>}
      </Card>
      <Card title="Preparedness summary" icon={BookOpen}>
        {!result ? <div className="empty-state"><MessageCircle size={36}/><h3>Select a language</h3><p>Ask a question to see a curated safety summary.</p></div> : <>
          <span className="subtle-pill">{languages[result.language]} · {result.topic}</span>
          <p className="guidance-text">{result.answer}</p>
          <Notice type="warning">{result.disclaimer}</Notice>
          <div className="source-reference"><b>Reference bookmark</b>{result.references.map(r=><a key={r.url} target="_blank" rel="noopener noreferrer" href={r.url}>{r.title} <ChevronRight size={13}/></a>)}</div>
        </>}
      </Card>
    </div>
  </>;
}
function ReportIncident() {
  const [fields,setFields] = useState({title:'',description:'',city:'Hyderabad',language:'en'});
  const [done,setDone] = useState(null),[error,setError] = useState(''),[busy,setBusy] = useState(false);
  const [reporterKey,setReporterKey] = useState('');
  const [coords,setCoords] = useState({latitude:'',longitude:''});
  async function submit(e) {e.preventDefault();setError('');setDone(null);setBusy(true);
    try { setDone(await api('/api/v1/incidents',{method:'POST',headers:reporterKey ? {'X-Reporter-Key':reporterKey} : {},body:JSON.stringify({...fields, ...(coords.latitude || coords.longitude ? {latitude:coords.latitude || null, longitude:coords.longitude || null} : {})})})); }
    catch(err){setError(err.message);}finally{setBusy(false);}
  }
  return <>
    <div className="page-heading"><div><div className="eyebrow">HUMAN-REVIEWED REPORTS</div><h1>Citizen incident report</h1><p>Submit a local demo report when submissions are enabled by the operator.</p></div></div>
    <Notice type="warning">NOT an emergency dispatch service. Do not use for urgent help. Avoid names, phone numbers, exact home addresses and other personal information. Public submissions are disabled by default.</Notice>
    <Card title="New report" subtitle="An AI suggestion never verifies or publishes an incident" icon={PlusCircle} className="narrow-card">
      <form className="stack" onSubmit={submit}>
        <label>Incident title<input required minLength={5} maxLength={100} value={fields.title} onChange={e=>setFields({...fields,title:e.target.value})} placeholder="e.g. Tree blocking road" /></label>
        <label>What happened?<textarea required minLength={10} maxLength={1000} rows={5} value={fields.description} onChange={e=>setFields({...fields,description:e.target.value})} placeholder="Describe the hazard without personal details" /></label>
        <div className="form-grid">
          <label>City<input required minLength={2} maxLength={80} value={fields.city} onChange={e=>setFields({...fields,city:e.target.value})}/></label>
          <label>Language<select value={fields.language} onChange={e=>setFields({...fields,language:e.target.value})}>{Object.entries(languages).map(([code,label])=><option key={code} value={code}>{label}</option>)}</select></label>
        </div>
        <p className="muted">Optional geographic coordinates are shown only to authorized demo reviewers. Avoid private home locations.</p>
        <div className="form-grid">
          <label>Latitude (optional)<input type="number" step="any" min="-90" max="90" value={coords.latitude} onChange={e=>setCoords({...coords,latitude:e.target.value})} /></label>
          <label>Longitude (optional)<input type="number" step="any" min="-180" max="180" value={coords.longitude} onChange={e=>setCoords({...coords,longitude:e.target.value})} /></label>
        </div>
        <label>Reporter access key (optional, required if the operator configured one)
          <input type="password" autoComplete="off" value={reporterKey} onChange={e=>setReporterKey(e.target.value)} placeholder="Local demo reporter key" />
        </label>
        <button className="primary" type="submit" disabled={busy}>{busy?'Submitting...':'Submit for review'}</button>
      </form>
      {error && <Notice type="warning">{error}</Notice>}
      {done && <Notice type="success"><CheckCircle2 size={16}/> Received demo report {done.id}. Suggested priority: {done.priority_hint}. Possible duplicate: {done.possible_duplicate ? 'yes':'no'}. No emergency response is initiated.</Notice>}
    </Card>
  </>;
}
function ResponderReview() {
  const [key,setKey] = useState(''),[reports,setReports] = useState([]),[error,setError] = useState(''),[message,setMessage] = useState(''),[busy,setBusy] = useState(false);
  const [accessToken,setAccessToken] = useState('');
  useEffect(() => {
    if (!oidcConfigured) return;
    readOidcUser().then(user => {
      if (user?.expired !== true) setAccessToken(user?.access_token || '');
    }).catch(err => setError('OIDC sign-in failed: ' + err.message));
  }, []);
  const requestHeaders = () => oidcConfigured
    ? (accessToken ? { Authorization: 'Bearer ' + accessToken } : {})
    : { 'X-Responder-Key': key };
  const [audit,setAudit] = useState([]);
  const [geo,setGeo] = useState({latitude:'17.38',longitude:'78.48',radius_km:10});
  const [geoResults,setGeoResults] = useState(null);
  async function load() {setBusy(true);setError('');setMessage('');
    try {const data=await api('/api/v1/incidents/review',{headers:requestHeaders()});setReports(data.incidents);}
    catch(err){setError(err.message);setReports([]);}finally{setBusy(false);}
  }
  async function searchNearby() {setError('');
    try {
      const params = new URLSearchParams(geo);
      const result=await api('/api/v1/incidents/nearby?'+params,{headers:requestHeaders()});
      setGeoResults(result);
    } catch(err) {setError(err.message);}
  }
  async function loadAudit() {setError('');
    try {const data=await api('/api/v1/incidents/audit',{headers:requestHeaders()});setAudit(data.events || []);}
    catch(err){setError(err.message);}
  }
  async function review(id,status) {setError('');setMessage('');
    try {await api('/api/v1/incidents/'+encodeURIComponent(id)+'/review',{method:'PATCH',headers:requestHeaders(),body:JSON.stringify({status,reviewer_note:'Reviewed in demonstration dashboard'})});setMessage('Report updated by reviewer.');await load();}
    catch(err){setError(err.message);}
  }
  return <>
    <div className="page-heading"><div><div className="eyebrow">AUTHORIZED HUMAN DECISION</div><h1>Responder review queue</h1><p>A protected demonstration queue. Automated suggestions never trigger official action.</p></div></div>
    <Notice type="warning">In demo mode, this uses a local shared key. Hosted reviewer mode requires a real OIDC provider and server-enforced responder role. Reports may contain sensitive details.</Notice>
    <Card title="Reviewer access" subtitle="Enter RESPONDER_API_KEY configured on the API server" icon={LockKeyhole}>
      {oidcConfigured ? <div className="inline-controls">
        {accessToken
          ? <button className="secondary" type="button" onClick={async()=>{await logoutLocally();setAccessToken('');setReports([])}}>Clear browser session</button>
          : <button className="primary" type="button" onClick={()=>loginWithOidc().catch(err=>setError(err.message))}>Sign in with organization IDP</button>}
        <button className="primary" disabled={busy || !accessToken} onClick={load}>{busy ? 'Loading...' : 'Load queue'} <RefreshCcw size={16}/></button>
      </div> : <div className="inline-controls"><input aria-label="Responder API key" type="password" autoComplete="off" placeholder="Local responder API key" value={key} onChange={e=>setKey(e.target.value)} /><button className="primary" disabled={busy||!key} onClick={load}>{busy ? 'Loading...' : 'Load queue'} <RefreshCcw size={16}/></button></div>}
      {error && <Notice type="warning">{error}</Notice>}
      {message && <Notice type="success">{message}</Notice>}
    </Card>
    <Card title="Review reports" subtitle="Latest 100; not a dispatch or official verification service" icon={FileWarning}>
      {!reports.length ? <div className="empty-state"><LockKeyhole size={32}/><p>No reports loaded. Authenticate and load the queue.</p></div> :
      <div className="report-list">{reports.map(report=><div className="report" key={report.id}>
        <div className="report-top"><b>{report.title}</b><span className="subtle-pill">{report.status}</span></div>
        <p>{report.description}</p><small>{report.city} · {categories[report.category] || report.category} · Priority suggestion: {report.priority_hint}</small>
        {report.duplicate_of && <small>Possible duplicate: {report.duplicate_of}</small>}
        <div className="actions">{['verified','dismissed','needs_info'].map(status=><button className="secondary small" key={status} onClick={()=>review(report.id,status)}>{status.replace('_',' ')}</button>)}</div>
      </div>)}</div>}
    </Card>
    <Card title="Geographic report filtering" subtitle="Restricted geographic radius search — unverified reports, not rescue routes" icon={MapPinned}>
      <div className="form-grid">
        <label>Latitude<input type="number" min="-90" max="90" step="any" value={geo.latitude} onChange={e=>setGeo({...geo,latitude:e.target.value})}/></label>
        <label>Longitude<input type="number" min="-180" max="180" step="any" value={geo.longitude} onChange={e=>setGeo({...geo,longitude:e.target.value})}/></label>
        <label>Search radius (km)<input type="number" min="0.1" max="50" step="0.1" value={geo.radius_km} onChange={e=>setGeo({...geo,radius_km:e.target.value})}/></label>
        <div className="actions"><button className="secondary" onClick={searchNearby} disabled={oidcConfigured ? !accessToken : !key}>Find nearby reports</button></div>
      </div>
      {geoResults && <div className="report-list" style={{marginTop:15}}>
        <p className="muted">{geoResults.total_matches_in_scan} matching local reports. Results limited to 100; search is not authoritative. {geoResults.possibly_incomplete ? "The result set was truncated." : "No truncation detected."} Backend: {geoResults.search_backend}.</p>
        {geoResults.incidents.map(r=><div className="report" key={r.id}>
          <b>{r.title}</b><p>{r.city} · {r.distance_km} km · {r.status}</p>
        </div>)}
      </div>}
    </Card>
    <Card title="Reviewer change history" subtitle="Local audit of review status changes; not verified actor identities" icon={Activity}>
      <button className="secondary" onClick={loadAudit} disabled={oidcConfigured ? !accessToken : !key}>Load audit history</button>
      {audit.length > 0 && <div className="report-list" style={{marginTop:14}}>
        {audit.map(event=><div className="report" key={event.id}>
          <small>{event.changed_at}</small>
          <p>Report {event.incident_id}: <b>{event.previous_status}</b> → <b>{event.new_status}</b></p>
        </div>)}
      </div>}
    </Card>
  </>;
}
export default function App() {
  const [tab,setTab] = useState('dashboard'),[mobileOpen,setMobileOpen] = useState(false);
  const ActiveIcon = nav.find(([id])=>id===tab)?.[1] || LayoutDashboard;
  function navigate(next){setTab(next);setMobileOpen(false);window.scrollTo({top:0,behavior:'smooth'});}
  return <div className="shell">
    <aside className={'sidebar ' + (mobileOpen ? 'sidebar-open':'')}>
      <div className="brand"><div className="brand-mark"><ShieldCheck size={25}/></div><div><b>CivicShield <span>AI</span></b><small>PUBLIC SAFETY RESEARCH</small></div><button className="close-mobile" aria-label="Close menu" onClick={()=>setMobileOpen(false)}><X size={20}/></button></div>
      <div className="nav-group-label">WORKSPACE</div>
      <nav aria-label="Application pages">{nav.map(([id, Icon, label])=><button key={id} className={'nav-item '+(tab===id?'active':'')} onClick={()=>navigate(id)}><Icon size={19}/><span>{label}</span>{tab===id&&<ChevronRight size={15}/>}</button>)}</nav>
      <div className="sidebar-bottom"><div className="simulation-label"><span className="pulse-dot"/> DEMONSTRATION MODE</div><p>Educational prototype<br/>No live alert connection</p><a target="_blank" rel="noopener noreferrer" href="https://github.com/harshakavali81-collab/CivicShield-AI">View source on GitHub <ChevronRight size={14}/></a></div>
    </aside>
    {mobileOpen && <button className="mobile-scrim" aria-label="Close navigation" onClick={()=>setMobileOpen(false)}/>}
    <div className="workspace">
      <header className="topbar"><button className="mobile-toggle" aria-label="Open menu" onClick={()=>setMobileOpen(true)}><Menu size={22}/></button><div className="topbar-current"><ActiveIcon size={18}/><span>{nav.find(([id])=>id===tab)?.[2]}</span></div><div className="topbar-right"><span className="simulation-label"><span className="pulse-dot"/> NOT LIVE</span><a href="https://ndma.gov.in/" rel="noopener noreferrer" target="_blank">Official guidance <ChevronRight size={15}/></a></div></header>
      <main id="main-content" className="main-content">
        {tab==='dashboard'&&<Dashboard onNavigate={navigate}/>}
        {tab==='risk'&&<RiskExplorer/>}
        {tab==='scenario'&&<ScenarioLab/>}
        {tab==='weather'&&<LiveWeather/>}
        {tab==='official'&&<OfficialSources/>}
        {tab==='diagnostics'&&<Diagnostics/>}
        {tab==='map'&&<><div className="page-heading"><div><div className="eyebrow">LOCATION VIEW</div><h1>Illustrative map</h1><p>Demonstration landmarks only; not risk estimates, emergencies, or verified events.</p></div></div><Notice type="warning">Map pins are synthetic placeholders. Consult official sources for current advisories.</Notice><Card title="Hyderabad area — demonstration pins" icon={MapPinned}><div className="large-map"><MapPanel/></div></Card></>}
        {tab==='assistant'&&<><SafetyAssistant/><KnowledgeSearch/></>}
        {tab==='report'&&<ReportIncident/>}
        {tab==='review'&&<ResponderReview/>}
      </main>
      <footer className="footer"><span>© 2026 CivicShield AI · Research prototype</span><span>Not a government service · Never rely on demo outputs for emergency decisions</span></footer>
    </div>
  </div>;
}

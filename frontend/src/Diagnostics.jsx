import React, { useEffect, useState } from 'react';
import { Activity, AlertTriangle, CheckCircle2, CloudRain, Database, RefreshCcw, ShieldCheck } from 'lucide-react';
import { api } from './api.js';

const paths = [
  ['/api/health', 'API process', 'Checks that the API process responds; does not test emergency-feed availability.'],
  ['/api/ready', 'Database and schema', 'Checks database connectivity and required schema. Does not measure hazard readiness.'],
  ['/api/v1/official/integration-status', 'Source connection configuration', 'Shows operator flags and source links only, not actual government warnings.'],
];

export default function Diagnostics() {
  const [items, setItems] = useState([]);
  const [busy, setBusy] = useState(false);
  async function refresh() {
    setBusy(true);
    const responses = await Promise.all(
      paths.map(async ([path,title,note]) => {
        try {
          const body = await api(path);
          return {path,title,note,status:'reachable',body};
        } catch(err) {
          return {path,title,note,status:'unavailable',error:String(err.message)};
        }
      }),
    );
    setItems(responses);
    setBusy(false);
  }
  useEffect(() => { refresh(); }, []);
  return <section>
    <div className="page-heading">
      <div><div className="eyebrow">ENGINEERING OPERATIONS · RESEARCH DEMO</div>
        <h1>System diagnostics</h1>
        <p>Read-only health checks, database readiness and data-provider configuration.</p>
      </div>
      <button className="secondary" onClick={refresh} disabled={busy}>
        <RefreshCcw size={17}/> {busy ? 'Checking...' : 'Refresh'}
      </button>
    </div>
    <div className="notice notice-warning">
      <AlertTriangle size={18}/><span>
        These checks are for <b>software diagnostics only</b>.
        A working API, database or configured provider never indicates a safe location,
        live monitoring, an official alert, or emergency-response readiness.
      </span>
    </div>
    <div className="diagnostic-grid">
      {items.map(item=><section className="card" key={item.path}>
        <div className="card-head"><div><h3>
          {item.status==='reachable'?<CheckCircle2 size={18}/>:<AlertTriangle size={18}/>}
          {' '}{item.title}</h3><p>{item.note}</p>
        </div></div>
        <div className={'diag-status '+(item.status==='reachable'?'diag-ok':'diag-error')}>
          {item.status==='reachable' ? 'Responding' : 'Unavailable'}
        </div>
        {item.error && <p className="muted">{item.error}</p>}
        {item.path==='/api/ready' && item.body && <p className="muted">Database: {item.body.database}; official emergency service: no</p>}
        {item.path==='/api/v1/official/integration-status' && item.body && <div className="diag-data">
          <p><b>IMD adapter:</b> {item.body.imd?.enabled ? 'Operator flag enabled — actual feed not verified' : 'Disabled'}</p>
          <p><b>CWC machine API:</b> {item.body.cwc?.api_connected ? 'Connected' : 'Not connected'}</p>
          <p><b>Official hazard status:</b> Unknown. Consult original authorities.</p>
        </div>}
        <code className="diag-path">{item.path}</code>
      </section>)}
    </div>
    <p className="muted">A failed health check should prompt software troubleshooting, not conclusions about current weather or public safety.</p>
  </section>;
}

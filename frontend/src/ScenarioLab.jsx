import React, { useEffect, useState } from 'react';
import {
  AlertTriangle, BookOpenCheck, Clock3, Database, FileCode2,
  ShieldAlert, Workflow,
} from 'lucide-react';
import {
  Area, AreaChart, CartesianGrid, Legend, ResponsiveContainer,
  Tooltip, XAxis, YAxis,
} from 'recharts';
import { api } from './api.js';

export default function ScenarioLab() {
  const [scenario, setScenario] = useState(null);
  const [active, setActive] = useState(0);
  const [error, setError] = useState('');
  useEffect(() => {
    api('/api/v1/demo/scenario').then(setScenario).catch(e => setError(e.message));
  }, []);

  const chapter = scenario?.chapters?.[active];
  return <section>
    <div className="page-heading"><div>
      <div className="eyebrow">CASE STUDY · 100% FABRICATED · OFFLINE</div>
      <h1>Scenario lab</h1>
      <p>Explore how the software handles source provenance, stale data, report review and model governance.</p>
    </div></div>

    <div className="notice notice-warning">
      <ShieldAlert size={18}/><span>
        <b>Fictional portfolio exercise.</b> This is not a forecast, observed rainfall,
        a real disaster, an official warning, or an emergency-response exercise.
        All chart values are invented and no report is created.
      </span>
    </div>
    {error && <div className="notice notice-warning" role="alert">{error}. Start the API to load the case study.</div>}
    {!scenario ? (!error && <p className="muted" role="status">Loading the synthetic exercise…</p>) : <>
      <div className="scenario-metrics">
        <div><span>Exercise duration</span><strong>{scenario.summary.hours} hours</strong><small>Fixed fictional times</small></div>
        <div><span>Invented rainfall total</span><strong>{scenario.summary.invented_precipitation_total_mm} mm</strong><small>Not a measurement</small></div>
        <div><span>Invented report count</span><strong>{scenario.summary.invented_report_total}</strong><small>Never stored as incidents</small></div>
        <div><span>Official warnings ingested</span><strong>None</strong><small>Not connected</small></div>
      </div>
      <div className="columns-two">
        <section className="card">
          <div className="card-head"><div><h3><Clock3 size={18}/> Fictional 24-hour timeline</h3>
            <p>Two series with independent axes and units; neither represents real events</p></div></div>
          <div className="scenario-chart" role="img" aria-label="Invented hourly rainfall and fictional report counts over 24 hours">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={scenario.samples}>
                <defs>
                  <linearGradient id="rainArea" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#317bdb" stopOpacity={0.3}/><stop offset="100%" stopColor="#317bdb" stopOpacity={0}/></linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5eaf2"/>
                <XAxis dataKey="hour" tick={{fontSize:11}} label={{value:'Fictional hour',position:'insideBottom',offset:-4}}/>
                <YAxis yAxisId="rain" tick={{fontSize:11}} width={35} label={{value:'mm/h',angle:-90,position:'insideLeft'}}/>
                <YAxis yAxisId="reports" orientation="right" tick={{fontSize:11}} width={35}/>
                <Tooltip formatter={(value,name)=>[value,name==='Invented rainfall'?'Rain (mm/h)':'Invented reports']}/>
                <Legend verticalAlign="top" height={35}/>
                <Area yAxisId="rain" name="Invented rainfall" dataKey="invented_hourly_precipitation_mm" type="monotone" stroke="#397bd6" fill="url(#rainArea)" strokeWidth={2}/>
                <Area yAxisId="reports" name="Invented reports" dataKey="invented_report_count" type="monotone" stroke="#d18a48" fill="none" strokeWidth={2} strokeDasharray="5 4"/>
              </AreaChart>
            </ResponsiveContainer>
          </div>
          <p className="muted"><Database size={13}/> Fixed arrays generated in Python, not fetched from IMD, CWC, Open-Meteo or the incident database.</p>
        </section>
        <section className="card">
          <div className="card-head"><div><h3><Workflow size={18}/> Engineering walkthrough</h3>
            <p>Pick a stage to see the corresponding design decision</p></div></div>
          <div className="scenario-steps" role="group" aria-label="Fictional case study stages">
            {scenario.chapters.map((step,i)=><button type="button" key={step.id}
                aria-pressed={i===active} className={'scenario-step '+(i===active?'selected':'')}
                onClick={()=>setActive(i)}>{step.title}</button>)}
          </div>
          {chapter && <div className="scenario-explainer" aria-live="polite">
            <span className="subtle-pill">Hour {chapter.hour} · {chapter.action_type.replaceAll('_',' ')}</span>
            <h3>{chapter.title}</h3>
            <p>{chapter.explanation}</p>
            <div className="notice notice-warning"><AlertTriangle size={16}/><span>{chapter.operator_takeaway}</span></div>
          </div>}
        </section>
      </div>
      <div className="card scenario-bottom">
        <h3><BookOpenCheck size={18}/> What this case study actually demonstrates</h3>
        <p>Reproducible source code, stable charts, UI state management, backend contracts, provenance labels, a data-freshness rule, role separation, and automated testing. It does <b>not</b> demonstrate validated flood forecasting or government alert integration.</p>
        <a href="https://github.com/harshakavali81-collab/CivicShield-AI/blob/main/docs/CASE_STUDY.md" target="_blank" rel="noopener noreferrer">
          <FileCode2 size={15}/> Read the full case study and tests
        </a>
      </div>
    </>}
  </section>;
}

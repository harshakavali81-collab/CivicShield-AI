import React, { useState } from 'react';
import { BookOpen, ExternalLink, Search } from 'lucide-react';
import { api } from './api.js';

export default function KnowledgeSearch() {
  const [query, setQuery] = useState('flood preparedness');
  const [items, setItems] = useState([]);
  const [searched, setSearched] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  async function submit(e) {
    e.preventDefault();
    setBusy(true);
    setError('');
    setSearched(false);
    try {
      const result = await api('/api/v1/assistant/knowledge?q=' + encodeURIComponent(query));
      setItems(result.items || []);
      setSearched(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }
  return <section className="card knowledge-card">
    <div className="card-head"><div><h3><BookOpen size={18}/> Search the safety source library</h3>
      <p>Manual curated summaries with linked organizations; no live retrieval, no official advisories</p></div></div>
    <form onSubmit={submit} className="inline-controls">
      <input value={query} minLength={2} maxLength={200} onChange={e => setQuery(e.target.value)}
        aria-label="Safety library query" placeholder="Flood, heatwave, weather notices..." required />
      <button className="secondary" disabled={busy}><Search size={16}/> {busy ? 'Searching...' : 'Search'}</button>
    </form>
    {error && <div className="notice notice-warning" role="alert">{error}</div>}
    {searched && !items.length && <p className="muted">No matching curated topics. Check verified authorities for current information.</p>}
    {!!items.length && <div className="knowledge-results">
      {items.map(item => <article className="knowledge-result" key={item.id}>
        <span className="subtle-pill">{item.topic} · curated {item.curated_date}</span>
        <h4>{item.title}</h4><p>{item.body}</p>
        <a href={item.source_url} target="_blank" rel="noopener noreferrer">
          Reference: {item.source_title} <ExternalLink size={12}/>
        </a>
      </article>)}
    </div>}
  </section>;
}

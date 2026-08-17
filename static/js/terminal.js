(() => {
  const root = document.querySelector('#terminal');
  if (!root) return;
  const endpoint = root.dataset.endpoint;
  const watchKey = 't90.watchlist';
  const alertsKey = 't90.alerts';
  const only = document.querySelector('#watchlist-only');
  const threshold = document.querySelector('#alert-threshold');
  const alertBox = document.querySelector('#terminal-alerts');
  const preferenceStatus = document.querySelector('#terminal-preference-status');
  let latestPayload = null;
  const read = (key, fallback) => { try { return JSON.parse(localStorage.getItem(key)) ?? fallback; } catch (_) { return fallback; } };
  const normalizedWatchlist = () => {
    const value = read(watchKey, []);
    return Array.isArray(value) ? [...new Set(value.filter((item) => typeof item === 'string'))] : [];
  };
  const alertPreferences = () => {
    const value = read(alertsKey, {});
    return value && typeof value === 'object' && !Array.isArray(value) ? value : {};
  };
  const escapeHtml = (value) => String(value ?? '').replace(/[&<>'"]/g, (char) => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[char]));
  const savePreferences = () => {
    localStorage.setItem(alertsKey, JSON.stringify({...alertPreferences(), enabled: true, threshold: Number(threshold.value), watchlist_only: only.checked}));
    preferenceStatus.textContent = 'Saved on this device';
    window.setTimeout(() => { preferenceStatus.textContent = ''; }, 1800);
  };
  // A price quoted off a futures or composite feed does not equal a spot broker
  // quote, so the basis is shown beside the number rather than buried in the payload.
  const basisTag = (p) => {
    const basis = p.price_basis;
    return basis && basis !== 'Spot' ? `<span class="price-basis">${escapeHtml(basis)}</span>` : '';
  };
  const priceNote = (p) => {
    const note = p.price_note ?? p.model?.price_note;
    return note && p.price_basis && p.price_basis !== 'Spot' ? `<p class="price-note">${escapeHtml(note)}</p>` : '';
  };
  const pct = (value) => (typeof value === 'number' ? `${value.toFixed(1)}%` : '—');
  // Positioning is a crowding read, not a direction call, so the percentile is
  // shown next to the label that names which CFTC trader group it describes.
  const positioningLine = (p) => {
    const view = p.positioning?.base;
    if (!p.positioning?.available || !view?.available) return '';
    const percentile = Math.round((view.percentile_3y ?? 0) * 100);
    return `<small class="market-line">${escapeHtml(view.speculative_label ?? 'Speculative')}: ${escapeHtml(view.crowding ?? '—')} · ${percentile}th pct · ${view.age_days}d old</small>`;
  };
  const newsLine = (p) => {
    const item = Array.isArray(p.news) ? p.news[0] : null;
    if (!item) return '';
    const headline = escapeHtml(item.headline);
    const label = `${escapeHtml(item.source)}: ${headline}`;
    return item.url
      ? `<small class="market-line"><a href="${escapeHtml(item.url)}" target="_blank" rel="noopener noreferrer">${label}</a></small>`
      : `<small class="market-line">${label}</small>`;
  };
  const renderPolicy = (payload) => {
    const panel = document.querySelector('#policy-panel');
    if (!panel) return;
    const policy = payload?.policy_expectations;
    const outlook = Array.isArray(policy?.outlook) ? policy.outlook : [];
    if (!outlook.length) { panel.innerHTML = ''; panel.hidden = true; return; }
    panel.hidden = false;
    panel.innerHTML = `<div class="policy-heading"><strong>Fed policy priced by the market</strong>`
      + `<span>Target range ${escapeHtml(policy.target_range || '—')} · ${escapeHtml(policy.next_meeting_bias || '')} · as of ${escapeHtml(policy.observed || '')}</span></div>`
      + `<table class="policy-table"><thead><tr><th scope="col">Window from</th><th scope="col">Cut</th><th scope="col">Hold</th><th scope="col">Hike</th><th scope="col">Expected rate</th></tr></thead><tbody>`
      + outlook.map((w) => `<tr><th scope="row">${escapeHtml(w.reference_start)}</th><td>${pct(w.cut_probability)}</td><td>${pct(w.hold_probability)}</td><td>${pct(w.hike_probability)}</td><td>${typeof w.expected_rate_bps === 'number' ? `${w.expected_rate_bps.toFixed(0)}bps` : '—'}</td></tr>`).join('')
      + `</tbody></table><p class="policy-source">Atlanta Fed Market Probability Tracker, derived from CME three-month SOFR options. Probabilities are market pricing, not forecasts.</p>`;
  };
  // A feed that dies quietly is worse than one that is visibly missing, so every
  // configured source reports its own health rather than just vanishing.
  const renderSourceHealth = (payload) => {
    const panel = document.querySelector('#source-health');
    if (!panel) return;
    const sources = payload?.sources;
    if (!sources || typeof sources !== 'object') { panel.innerHTML = ''; panel.hidden = true; return; }
    const items = Object.entries(sources).map(([name, meta]) => {
      const down = Boolean(meta?.message);
      const label = escapeHtml(name.replace(/_/g, ' '));
      const detail = down ? escapeHtml(meta.message) : `${escapeHtml(meta?.provider ?? '')}`;
      return `<li class="${down ? 'source-down' : 'source-ok'}"><strong>${label}</strong> ${detail}</li>`;
    });
    const down = Object.values(sources).filter((meta) => meta?.message).length;
    panel.hidden = false;
    panel.innerHTML = `<details${down ? ' open' : ''}><summary>${down ? `${down} data ${down === 1 ? 'source is' : 'sources are'} unavailable` : 'All data sources reporting'}</summary><ul>${items.join('')}</ul></details>`;
  };
  const render = (payload) => {
    latestPayload = payload;
    renderPolicy(payload);
    renderSourceHealth(payload);
    const pairs = Array.isArray(payload?.pairs) ? payload.pairs : [];
    if (!pairs.length) return;
    const watched = normalizedWatchlist();
    const shown = only.checked ? pairs.filter((p) => watched.includes(p.symbol)) : pairs;
    root.innerHTML = shown.length ? `<div class="terminal-grid">${shown.map((p) => `<article class="market"><div class="market-heading"><h2>${escapeHtml(p.symbol)}</h2><button class="watch-button${watched.includes(p.symbol) ? ' watched' : ''}" data-symbol="${escapeHtml(p.symbol)}" aria-pressed="${watched.includes(p.symbol)}">${watched.includes(p.symbol) ? '★ Watching' : '☆ Watch'}</button></div><div class="price">${Number(p.price).toFixed(p.decimals ?? 2)}${basisTag(p)}</div><strong class="${p.score > 18 ? 'positive' : p.score < -18 ? 'negative' : ''}">${p.score >= 0 ? '+' : ''}${p.score} · ${escapeHtml(p.bias)}</strong><br><small>Grade ${escapeHtml(p.quality?.grade ?? '—')} · ${escapeHtml(p.market?.regime ?? 'Unknown')}</small>${positioningLine(p)}${newsLine(p)}${priceNote(p)}</article>`).join('')}</div>` : '<div class="terminal-empty"><strong>Your watchlist is empty.</strong><p>Turn off “Watchlist only” and add the markets you want to follow.</p></div>';
    const level = Number(threshold.value);
    const candidates = pairs.filter((p) => watched.includes(p.symbol) && Math.abs(Number(p.score)) >= level);
    alertBox.innerHTML = candidates.length ? `<strong>${candidates.length} watchlist ${candidates.length === 1 ? 'market meets' : 'markets meet'} your ±${level} evidence threshold:</strong> ${candidates.map((p) => `${escapeHtml(p.symbol)} (${Number(p.score) >= 0 ? '+' : ''}${escapeHtml(p.score)})`).join(' · ')}` : '';
    alertBox.hidden = !candidates.length;
  };
  const preferences = alertPreferences();
  threshold.value = ['10','18','25'].includes(String(preferences.threshold)) ? String(preferences.threshold) : '18';
  only.checked = Boolean(preferences.watchlist_only);
  root.addEventListener('click', (event) => {
    const button = event.target.closest('[data-symbol]');
    if (!button) return;
    const watched = normalizedWatchlist();
    const symbol = button.dataset.symbol;
    localStorage.setItem(watchKey, JSON.stringify(watched.includes(symbol) ? watched.filter((item) => item !== symbol) : [...watched, symbol]));
    render(latestPayload);
  });
  only.addEventListener('change', () => { savePreferences(); if (latestPayload) render(latestPayload); });
  threshold.addEventListener('change', () => { savePreferences(); if (latestPayload) render(latestPayload); });
  const embedded = document.querySelector('#snapshot-data');
  if (embedded) { try { render(JSON.parse(embedded.textContent)); } catch (_) {} }
  fetch(endpoint, {cache:'no-store'}).then((r) => { if (!r.ok) throw new Error(); return r.json(); }).then(render).catch(() => {});
})();

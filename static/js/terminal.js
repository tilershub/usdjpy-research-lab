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
  const render = (payload) => {
    latestPayload = payload;
    const pairs = Array.isArray(payload?.pairs) ? payload.pairs : [];
    if (!pairs.length) return;
    const watched = normalizedWatchlist();
    const shown = only.checked ? pairs.filter((p) => watched.includes(p.symbol)) : pairs;
    root.innerHTML = shown.length ? `<div class="terminal-grid">${shown.map((p) => `<article class="market"><div class="market-heading"><h2>${escapeHtml(p.symbol)}</h2><button class="watch-button${watched.includes(p.symbol) ? ' watched' : ''}" data-symbol="${escapeHtml(p.symbol)}" aria-pressed="${watched.includes(p.symbol)}">${watched.includes(p.symbol) ? '★ Watching' : '☆ Watch'}</button></div><div class="price">${Number(p.price).toFixed(p.decimals ?? 2)}</div><strong class="${p.score > 18 ? 'positive' : p.score < -18 ? 'negative' : ''}">${p.score >= 0 ? '+' : ''}${p.score} · ${escapeHtml(p.bias)}</strong><br><small>Grade ${escapeHtml(p.quality?.grade ?? '—')} · ${escapeHtml(p.market?.regime ?? 'Unknown')}</small></article>`).join('')}</div>` : '<div class="terminal-empty"><strong>Your watchlist is empty.</strong><p>Turn off “Watchlist only” and add the markets you want to follow.</p></div>';
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

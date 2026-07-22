(() => {
  const root = document.querySelector('#terminal');
  if (!root) return;
  const endpoint = root.dataset.endpoint;
  const render = (payload) => {
    const pairs = Array.isArray(payload?.pairs) ? payload.pairs : [];
    if (!pairs.length) return;
    root.innerHTML = `<div class="terminal-grid">${pairs.map((p) => `<article class="market"><h2>${p.symbol}</h2><div class="price">${Number(p.price).toFixed(p.decimals ?? 2)}</div><strong class="${p.score > 18 ? 'positive' : p.score < -18 ? 'negative' : ''}">${p.score >= 0 ? '+' : ''}${p.score} · ${p.bias}</strong><br><small>Grade ${p.quality?.grade ?? '—'} · ${p.market?.regime ?? 'Unknown'}</small></article>`).join('')}</div>`;
  };
  const embedded = document.querySelector('#snapshot-data');
  if (embedded) { try { render(JSON.parse(embedded.textContent)); } catch (_) {} }
  fetch(endpoint, {cache:'no-store'}).then((r) => { if (!r.ok) throw new Error(); return r.json(); }).then(render).catch(() => {});
})();

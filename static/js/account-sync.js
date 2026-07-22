(() => {
  const status = document.getElementById('sync-status');
  if (!status) return;
  const api = '/account/api/workspace/';
  const read = (key, fallback) => { try { const value = JSON.parse(localStorage.getItem(key)); return value ?? fallback; } catch { return fallback; } };
  const csrf = () => document.cookie.split('; ').find(x => x.startsWith('csrftoken='))?.split('=')[1] || '';
  const localPayload = () => {
    const daily = {};
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key && key.startsWith('t90.checklist.')) daily[key.slice(14)] = read(key, []);
    }
    return {journal: read('t90.journal', []), plan: read('t90.plan', {}), daily_checklists: daily, watchlist: read('t90.watchlist', []), alert_preferences: read('t90.alerts', {})};
  };
  const setStatus = (message, error=false) => { status.textContent = message; status.classList.toggle('error', error); };
  const fetchRemote = async () => { const response = await fetch(api, {credentials:'same-origin'}); if (!response.ok) throw new Error('Could not load account data.'); return response.json(); };
  document.getElementById('sync-upload').onclick = async () => {
    setStatus('Saving this device…');
    try { const response = await fetch(api, {method:'PUT', credentials:'same-origin', headers:{'Content-Type':'application/json','X-CSRFToken':csrf()}, body:JSON.stringify(localPayload())}); if (!response.ok) throw new Error((await response.json()).error || 'Sync failed.'); const data=await response.json(); setStatus('Saved securely · '+new Date(data.updated_at).toLocaleString()); } catch (error) { setStatus(error.message, true); }
  };
  document.getElementById('sync-download').onclick = async () => {
    if (!confirm('Replace TRADE90 data on this device with the saved account copy?')) return;
    setStatus('Restoring account data…');
    try { const data=await fetchRemote(); localStorage.setItem('t90.journal',JSON.stringify(data.journal)); localStorage.setItem('t90.plan',JSON.stringify(data.plan)); localStorage.setItem('t90.watchlist',JSON.stringify(data.watchlist)); localStorage.setItem('t90.alerts',JSON.stringify(data.alert_preferences)); Object.entries(data.daily_checklists).forEach(([day,value])=>localStorage.setItem('t90.checklist.'+day,JSON.stringify(value))); setStatus('Restored · reload an open tool to see the saved data.'); } catch(error) { setStatus(error.message,true); }
  };
  fetchRemote().then(data=>setStatus('Account copy last updated · '+new Date(data.updated_at).toLocaleString())).catch(error=>setStatus(error.message,true));
})();

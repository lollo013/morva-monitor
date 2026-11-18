/* =====================================================================
   Dai tempi dei caratteri restituiti da ElevenLabs:
   - le parole con inizio e fine        -> sottotitoli
   - le forme della bocca nel tempo     -> animazione del Professore
   ===================================================================== */

/* Parole pronunciate, saltando le indicazioni [tra parentesi quadre]. */
export function parole(allineamento) {
  const { characters: c, character_start_times_seconds: ini, character_end_times_seconds: fin } = allineamento;
  const out = [];
  let parola = null, dentroTag = false;
  const chiudi = () => { if (parola && parola.testo.trim()) out.push(parola); parola = null; };
  for (let i = 0; i < c.length; i++) {
    const ch = c[i];
    if (ch === '[') { chiudi(); dentroTag = true; continue; }
    if (dentroTag) { if (ch === ']') dentroTag = false; continue; }
    if (/\s/.test(ch)) { chiudi(); continue; }
    if (!parola) parola = { testo: '', inizio: ini[i], fine: fin[i] };
    parola.testo += ch;
    parola.fine = fin[i];
  }
  chiudi();
  return out;
}

/* Raggruppa le parole in sottotitoli brevi, leggibili su TikTok. */
export function sottotitoli(listaParole, { maxCaratteri = 32, maxSecondi = 2.6 } = {}) {
  const blocchi = [];
  let corrente = [];
  const lunghezza = ws => ws.map(w => w.testo).join(' ').length;
  for (const w of listaParole) {
    if (corrente.length) {
      const troppoLungo = lunghezza([...corrente, w]) > maxCaratteri;
      const troppoTempo = w.fine - corrente[0].inizio > maxSecondi;
      if (troppoLungo || troppoTempo) { blocchi.push(corrente); corrente = []; }
    }
    corrente.push(w);
    if (/[.?!…]["»”]?$/.test(w.testo)) { blocchi.push(corrente); corrente = []; }
  }
  if (corrente.length) blocchi.push(corrente);
  return blocchi.map(ws => ({
    inizio: ws[0].inizio,
    fine: ws[ws.length - 1].fine,
    testo: ws.map(w => w.testo).join(' ')
  }));
}

export function srt(blocchi) {
  const t = s => {
    const ms = Math.max(0, Math.round(s * 1000));
    const p = (n, l = 2) => String(n).padStart(l, '0');
    return `${p(Math.floor(ms / 3600000))}:${p(Math.floor(ms / 60000) % 60)}:${p(Math.floor(ms / 1000) % 60)},${p(ms % 1000, 3)}`;
  };
  return blocchi.map((b, i) => `${i + 1}\n${t(b.inizio)} --> ${t(b.fine)}\n${b.testo}\n`).join('\n');
}

/* ---------------------------------------------------------------------
   Forme della bocca. Poche e riconoscibili, come in un cartone:
     riposo  bocca chiusa e rilassata (pause, silenzi)
     MBP     labbra chiuse (m, b, p)
     FV      labbro sotto i denti (f, v)
     A E I O U  le cinque vocali
     aperta  qualunque altra consonante: bocca socchiusa
   --------------------------------------------------------------------- */
const VOCALI = { a: 'A', à: 'A', e: 'E', è: 'E', é: 'E', i: 'I', ì: 'I', í: 'I', o: 'O', ò: 'O', ó: 'O', u: 'U', ù: 'U', ú: 'U' };

function forma(ch) {
  const l = ch.toLowerCase();
  if (VOCALI[l]) return VOCALI[l];
  if ('mbp'.includes(l)) return 'MBP';
  if ('fv'.includes(l)) return 'FV';
  if (/\p{L}/u.test(l)) return 'aperta';
  return null; // spazi e punteggiatura
}

export function bocca(allineamento, { pausaMinima = 0.15, durataMinima = 0.06 } = {}) {
  const { characters: c, character_start_times_seconds: ini, character_end_times_seconds: fin } = allineamento;
  const chiavi = [];
  let dentroTag = false, ultimaFine = 0;
  const aggiungi = (f, t) => {
    const prec = chiavi[chiavi.length - 1];
    if (prec && prec.forma === f) return;
    if (prec && t - prec.t < durataMinima && f !== 'riposo') { prec.forma = f; return; }
    chiavi.push({ t: Math.round(t * 1000) / 1000, forma: f });
  };
  for (let i = 0; i < c.length; i++) {
    if (c[i] === '[') { dentroTag = true; continue; }
    if (dentroTag) { if (c[i] === ']') dentroTag = false; continue; }
    const f = forma(c[i]);
    if (!f) continue;
    if (ini[i] - ultimaFine >= pausaMinima) aggiungi('riposo', ultimaFine);
    aggiungi(f, ini[i]);
    ultimaFine = fin[i];
  }
  aggiungi('riposo', ultimaFine);
  return chiavi;
}

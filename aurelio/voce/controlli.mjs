/* =====================================================================
   Controlli sulla narrazione prima che entri nel montaggio.
   ===================================================================== */

/* Parole normalizzate: minuscole, senza punteggiatura, accenti tenuti. */
export function normalizza(testo) {
  return testo
    .toLowerCase()
    .replace(/[’']/g, ' ')
    .replace(/[^\p{L}\p{N}\s]/gu, ' ')
    .split(/\s+/)
    .filter(Boolean);
}

/* Quota di parole sbagliate fra copione e trascrizione (WER). */
export function erroreParole(atteso, sentito) {
  const a = normalizza(atteso), b = normalizza(sentito);
  if (a.length === 0) return b.length ? 1 : 0;
  let prec = Array.from({ length: b.length + 1 }, (_, j) => j);
  for (let i = 1; i <= a.length; i++) {
    const riga = [i];
    for (let j = 1; j <= b.length; j++) {
      riga[j] = Math.min(prec[j] + 1, riga[j - 1] + 1, prec[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
    }
    prec = riga;
  }
  return prec[b.length] / a.length;
}

/* Ritmo in parole al minuto: un professore riflessivo sta fra 110 e 170. */
export function ritmo(numeroParole, secondi) {
  return secondi > 0 ? (numeroParole / secondi) * 60 : 0;
}

export function verifica({ durata, numeroParole, errore, config }) {
  const problemi = [];
  if (durata > config.durata_massima_secondi) {
    problemi.push(`Durata ${durata.toFixed(1)} s oltre il massimo di ${config.durata_massima_secondi} s.`);
  }
  const ppm = ritmo(numeroParole, durata);
  if (ppm < 110) problemi.push(`Ritmo troppo lento: ${Math.round(ppm)} parole al minuto.`);
  if (ppm > 170) problemi.push(`Ritmo troppo veloce: ${Math.round(ppm)} parole al minuto.`);
  if (errore !== null && errore > config.soglia_errore_pronuncia) {
    problemi.push(`Pronuncia da ricontrollare: ${(errore * 100).toFixed(1)}% di parole non riconosciute.`);
  }
  return { ok: problemi.length === 0, problemi, paroleAlMinuto: Math.round(ppm) };
}

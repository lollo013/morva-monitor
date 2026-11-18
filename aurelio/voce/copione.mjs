/* =====================================================================
   Dal copione verificato al testo da far leggere.

   Un copione e' una lista di parti, ognuna con la sua fase:
     domanda      tono pensieroso, curioso, leggermente misterioso
     spiegazione  chiaro, autorevole, coinvolgente
     scoperta     leggera enfasi sulla notizia sorprendente
     conclusione  rassicurante, soddisfatto, riflessivo

   Con eleven_v3 l'intonazione si guida con un'indicazione tra parentesi
   quadre all'inizio di ogni parte. Le indicazioni sono volutamente
   sobrie: il Professore non recita, racconta.
   ===================================================================== */
import { ErroreVoce } from './errori.mjs';

export const FASI = {
  domanda: '[thoughtful]',
  spiegazione: '[calm]',
  scoperta: '[intrigued]',
  conclusione: '[warmly]'
};

export function validaCopione(copione) {
  if (!Array.isArray(copione?.parti) || copione.parti.length === 0) {
    throw new ErroreVoce('COPIONE_NON_VALIDO', 'Il copione non ha parti.');
  }
  if (copione.verificato !== true) {
    throw new ErroreVoce('COPIONE_NON_VERIFICATO',
      'Il copione non e\' segnato come verificato: la voce non lo legge.');
  }
  for (const [i, p] of copione.parti.entries()) {
    if (!FASI[p.fase]) {
      throw new ErroreVoce('COPIONE_NON_VALIDO',
        `Parte ${i + 1}: fase "${p.fase}" sconosciuta (usa ${Object.keys(FASI).join(', ')}).`);
    }
    if (!p.testo || !p.testo.trim()) {
      throw new ErroreVoce('COPIONE_NON_VALIDO', `Parte ${i + 1}: testo vuoto.`);
    }
  }
  return copione;
}

/* Testo da inviare a ElevenLabs. */
export function testoDaLeggere(copione, modello) {
  const conIndicazioni = modello === 'eleven_v3';
  return copione.parti
    .map(p => (conIndicazioni ? FASI[p.fase] + ' ' : '') + pulisci(p.testo))
    .join('\n\n');
}

/* Testo come lo legge una persona: per sottotitoli e controllo pronuncia. */
export function testoPulito(copione) {
  return copione.parti.map(p => pulisci(p.testo)).join(' ');
}

function pulisci(t) {
  return t
    .replace(/\s+/g, ' ')
    .replace(/\s+([,.;:!?])/g, '$1')
    .replace(/\[[^\]]*\]/g, '')     // nessuna indicazione scritta a mano
    .trim();
}

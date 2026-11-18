/* =====================================================================
   Dal copione verificato al testo da far interpretare.

   Un copione e' una lista di parti, ognuna con la sua fase:
     apertura     0-5 s: energica, intrigante, curiosa. Parte subito,
                  intonazione crescente sulla domanda ("Ti sei mai
                  chiesto perche'...?")
     spiegazione  dinamica, espressiva, sicura; mai una lettura uniforme
     scoperta     enfasi sulla notizia sorprendente
     conclusione  chiara, incisiva, soddisfacente: una piccola
                  rivelazione, senza esagerare

   Con eleven_v3 l'interpretazione si guida con un'indicazione tra
   parentesi quadre all'inizio di ogni parte. Niente toni da trailer o da
   pubblicita': il Professore racconta, non vende.
   ===================================================================== */
import { ErroreVoce } from './errori.mjs';

export const FASI = {
  apertura: '[curious]',
  spiegazione: '[engaged]',
  scoperta: '[intrigued]',
  conclusione: '[satisfied]'
};
/* nomi usati nei primi copioni */
const SINONIMI = { domanda: 'apertura' };
const fase = p => SINONIMI[p.fase] || p.fase;

export function validaCopione(copione) {
  if (!Array.isArray(copione?.parti) || copione.parti.length === 0) {
    throw new ErroreVoce('COPIONE_NON_VALIDO', 'Il copione non ha parti.');
  }
  if (copione.verificato !== true) {
    throw new ErroreVoce('COPIONE_NON_VERIFICATO',
      'Il copione non e\' segnato come verificato: la voce non lo legge.');
  }
  for (const [i, p] of copione.parti.entries()) {
    if (!FASI[fase(p)]) {
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
    .map(p => (conIndicazioni ? FASI[fase(p)] + ' ' : '') + pulisci(p.testo))
    .join(' ');   // nessuna pausa inutile fra le parti
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

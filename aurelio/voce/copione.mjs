/* =====================================================================
   Dal copione verificato al testo da far interpretare.

   Un copione e' una lista di parti, ognuna con la sua fase:
     apertura     0-5 s: curiosita' intensa, parte dalla prima parola
     spiegazione  energica, dinamica, sicura; mai una lettura uniforme
     scoperta     sorpresa autentica sulla notizia
     conclusione  calda e incisiva: una piccola rivelazione
     invito       chiusura da amico: like e segui per altri video

   Con eleven_v3 l'interpretazione si guida con le indicazioni tra
   parentesi quadre documentate da ElevenLabs ([curious], [excited],
   [surprised], [warmly]). Il modello non ha un parametro di velocita':
   il ritmo nasce da indicazioni, punteggiatura e frasi brevi.

   Enfasi: nel copione si scrive *parola*; con eleven_v3 diventa
   PAROLA (le maiuscole sono il modo indicato da ElevenLabs per
   sottolineare), nei sottotitoli resta "parola".
   ===================================================================== */
import { ErroreVoce } from './errori.mjs';

export const FASI = {
  apertura: '[warmly] [curious]',
  spiegazione: '[excited]',
  scoperta: '[surprised]',
  conclusione: '[warmly]',
  invito: '[warmly]'
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
    .map(p => conIndicazioni
      ? FASI[fase(p)] + ' ' + enfasi(pulisci(p.testo), s => s.toUpperCase())
      : enfasi(pulisci(p.testo), s => s))
    .join(' ');   // nessuna pausa inutile fra le parti
}

/* Testo come lo legge una persona: per sottotitoli e controllo pronuncia. */
export function testoPulito(copione) {
  return copione.parti.map(p => enfasi(pulisci(p.testo), s => s)).join(' ');
}

const enfasi = (t, f) => t.replace(/\*([^*]+)\*/g, (_, s) => f(s));

function pulisci(t) {
  return t
    .replace(/\s+/g, ' ')
    .replace(/\s+([,.;:!?])/g, '$1')
    .replace(/\[[^\]]*\]/g, '')     // nessuna indicazione scritta a mano
    .trim();
}

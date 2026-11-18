/* =====================================================================
   Client ElevenLabs, solo lato server.

   La chiave arriva esclusivamente dalla variabile d'ambiente
   ELEVENLABS_API_KEY (in GitHub: un "secret" del repository). Non va mai
   scritta nel codice, nei file di configurazione o in una pagina web.

   Se ElevenLabs non risponde, si ferma tutto con un errore: non si prova
   mai un'altra voce al posto di quella approvata.
   ===================================================================== */
import { ErroreVoce } from './errori.mjs';

const BASE = 'https://api.elevenlabs.io/v1';
const TENTATIVI = 3;

function chiave() {
  const k = process.env.ELEVENLABS_API_KEY;
  if (!k) {
    throw new ErroreVoce(
      'CHIAVE_MANCANTE',
      'Manca ELEVENLABS_API_KEY nell\'ambiente del server.'
    );
  }
  return k;
}

async function chiama(percorso, opzioni, fetchImpl = fetch) {
  let ultimo;
  for (let i = 1; i <= TENTATIVI; i++) {
    let risposta;
    try {
      risposta = await fetchImpl(BASE + percorso, {
        ...opzioni,
        headers: { 'xi-api-key': chiave(), ...(opzioni.headers || {}) }
      });
    } catch (e) {
      if (e instanceof ErroreVoce) throw e;
      ultimo = new ErroreVoce('ELEVENLABS_NON_DISPONIBILE',
        `ElevenLabs non raggiungibile: ${e.message}`);
      await attesa(i);
      continue;
    }
    if (risposta.ok) return risposta;

    const corpo = await risposta.text().catch(() => '');
    if (risposta.status === 401 || risposta.status === 403) {
      throw new ErroreVoce('CHIAVE_RIFIUTATA',
        `ElevenLabs ha rifiutato la chiave (HTTP ${risposta.status}).`, { corpo });
    }
    if (risposta.status === 404) {
      throw new ErroreVoce('VOCE_NON_TROVATA',
        'La voce approvata non esiste piu\' su ElevenLabs. Nessuna voce sostitutiva e\' stata usata.',
        { corpo });
    }
    ultimo = new ErroreVoce('ELEVENLABS_NON_DISPONIBILE',
      `ElevenLabs ha risposto HTTP ${risposta.status}.`, { corpo });
    // 429 e 5xx: si riprova con la stessa voce, poi ci si arrende
    if (risposta.status !== 429 && risposta.status < 500) throw ultimo;
    await attesa(i);
  }
  throw ultimo;
}

const attesa = i => new Promise(r => setTimeout(r, 1000 * 2 ** i));

/* Testo -> audio, con i tempi di ogni carattere (per sottotitoli e bocca). */
export async function sintetizza(testo, config, fetchImpl) {
  const query = new URLSearchParams({ output_format: config.formato_audio });
  const risposta = await chiama(
    `/text-to-speech/${encodeURIComponent(config.voice_id)}/with-timestamps?${query}`,
    {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({
        text: testo,
        model_id: config.modello_tts,
        language_code: config.lingua,
        voice_settings: config.impostazioni_voce
      })
    },
    fetchImpl
  );
  const dati = await risposta.json();
  if (!dati.audio_base64 || !dati.alignment) {
    throw new ErroreVoce('RISPOSTA_INCOMPLETA',
      'ElevenLabs non ha restituito audio e tempi.');
  }
  return {
    audio: Buffer.from(dati.audio_base64, 'base64'),
    allineamento: dati.alignment
  };
}

/* Audio -> testo, per controllare la pronuncia. */
export async function trascrivi(audio, config, fetchImpl) {
  const modulo = new FormData();
  modulo.append('model_id', config.modello_trascrizione || 'scribe_v1');
  modulo.append('language_code', config.lingua);
  modulo.append('file', new Blob([audio], { type: 'audio/mpeg' }), 'narrazione.mp3');
  const risposta = await chiama('/speech-to-text', { method: 'POST', body: modulo }, fetchImpl);
  const dati = await risposta.json();
  return dati.text || '';
}

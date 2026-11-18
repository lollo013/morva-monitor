import { test } from 'node:test';
import assert from 'node:assert/strict';
import { voceApprovata } from './config.mjs';
import { validaCopione, testoDaLeggere, testoPulito } from './copione.mjs';
import { parole, sottotitoli, srt, bocca } from './tempi.mjs';
import { erroreParole, verifica } from './controlli.mjs';
import { sintetizza } from './elevenlabs.mjs';

/* allineamento finto: un carattere ogni 0,1 s */
function allinea(testo) {
  const c = [...testo];
  return {
    characters: c,
    character_start_times_seconds: c.map((_, i) => i * 0.1),
    character_end_times_seconds: c.map((_, i) => i * 0.1 + 0.1)
  };
}

const copione = {
  verificato: true,
  parti: [
    { fase: 'domanda', testo: 'Perché il cielo è azzurro?' },
    { fase: 'conclusione', testo: 'La natura è semplice.' }
  ]
};

test('senza approvazione la voce non parte', () => {
  assert.throws(() => voceApprovata({ stato: 'in_attesa_di_approvazione', voice_id: null }),
    e => e.codice === 'VOCE_NON_APPROVATA');
  assert.throws(() => voceApprovata({ stato: 'approvata', voice_id: null }),
    e => e.codice === 'VOCE_NON_APPROVATA');
});

test('un copione non verificato viene rifiutato', () => {
  assert.throws(() => validaCopione({ ...copione, verificato: false }),
    e => e.codice === 'COPIONE_NON_VERIFICATO');
  assert.throws(() => validaCopione({ verificato: true, parti: [{ fase: 'urlo', testo: 'x' }] }),
    e => e.codice === 'COPIONE_NON_VALIDO');
});

test('le fasi diventano indicazioni solo con eleven_v3', () => {
  assert.match(testoDaLeggere(copione, 'eleven_v3'), /^\[thoughtful\] Perché/);
  assert.doesNotMatch(testoDaLeggere(copione, 'eleven_multilingual_v2'), /\[/);
  assert.equal(testoPulito(copione), 'Perché il cielo è azzurro? La natura è semplice.');
});

test('le parole saltano le indicazioni tra parentesi', () => {
  const w = parole(allinea('[thoughtful] Perché il cielo?'));
  assert.deepEqual(w.map(x => x.testo), ['Perché', 'il', 'cielo?']);
  assert.equal(w[0].inizio, 1.3);
});

test('i sottotitoli si spezzano a fine frase e restano brevi', () => {
  const w = parole(allinea('Vi siete mai chiesti perché il cielo è azzurro? Ebbene, la luce.'));
  const s = sottotitoli(w);
  assert.ok(s.every(b => b.testo.length <= 32));
  assert.ok(s.some(b => b.testo.endsWith('azzurro?')));
  assert.match(srt(s), /^1\n00:00:00,000 --> 00:00:0\d,\d{3}\n/);
});

test('la bocca si chiude su m, b, p e riposa nelle pause', () => {
  const k = bocca(allinea('mamma'));
  assert.equal(k[0].forma, 'MBP');
  assert.equal(k.at(-1).forma, 'riposo');
  assert.ok(k.some(x => x.forma === 'A'));
});

test('controllo pronuncia e ritmo', () => {
  assert.equal(erroreParole('Il cielo è azzurro.', 'il cielo è azzurro'), 0);
  assert.equal(erroreParole('il cielo è azzurro', 'il cielo e azzurro'), 0.25);
  const config = { durata_massima_secondi: 90, soglia_errore_pronuncia: 0.12 };
  assert.equal(verifica({ durata: 20, numeroParole: 48, errore: 0.02, config }).ok, true);
  assert.equal(verifica({ durata: 20, numeroParole: 80, errore: 0.02, config }).ok, false);
  assert.equal(verifica({ durata: 20, numeroParole: 48, errore: 0.3, config }).ok, false);
});

test('se ElevenLabs non trova la voce si ferma, senza ripiego', async () => {
  process.env.ELEVENLABS_API_KEY = 'prova';
  const chiamate = [];
  const finto = async (url) => { chiamate.push(url); return new Response('no', { status: 404 }); };
  await assert.rejects(
    sintetizza('ciao', { voice_id: 'VOCE', formato_audio: 'mp3_44100_128', modello_tts: 'eleven_v3', lingua: 'it' }, finto),
    e => e.codice === 'VOCE_NON_TROVATA'
  );
  assert.equal(chiamate.length, 1);
  assert.match(chiamate[0], /text-to-speech\/VOCE\/with-timestamps/);
});

test('senza chiave non parte nessuna richiesta', async () => {
  delete process.env.ELEVENLABS_API_KEY;
  let chiamato = false;
  await assert.rejects(
    sintetizza('ciao', { voice_id: 'V', formato_audio: 'mp3_44100_128' }, async () => { chiamato = true; }),
    e => e.codice === 'CHIAVE_MANCANTE'
  );
  assert.equal(chiamato, false);
});

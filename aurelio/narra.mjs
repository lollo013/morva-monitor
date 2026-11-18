/* =====================================================================
   Professor Aurelio: dal copione verificato alla narrazione pronta.

   Uso:  node aurelio/narra.mjs <copione.json> <cartella-di-uscita>

   Produce nella cartella:
     narrazione.mp3    la voce ufficiale approvata
     sottotitoli.srt   sincronizzati parola per parola
     bocca.json        forme della bocca nel tempo, per l'animazione
     rapporto.json     durata, ritmo, controllo della pronuncia
     stato.json        esito per la dashboard (anche in caso di errore)

   Se qualcosa non va, il lavoro si ferma con codice d'uscita 1 e
   stato.json spiega perche'. Non viene mai usata una voce diversa da
   quella approvata.
   ===================================================================== */
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import path from 'node:path';
import { leggiConfig, voceApprovata } from './voce/config.mjs';
import { validaCopione, testoDaLeggere, testoPulito } from './voce/copione.mjs';
import { sintetizza, trascrivi } from './voce/elevenlabs.mjs';
import { parole, sottotitoli, srt, bocca } from './voce/tempi.mjs';
import { erroreParole, verifica } from './voce/controlli.mjs';

const [fileCopione, cartella] = process.argv.slice(2);
if (!fileCopione || !cartella) {
  console.error('Uso: node aurelio/narra.mjs <copione.json> <cartella-di-uscita>');
  process.exit(2);
}

const stato = { quando: new Date().toISOString(), copione: fileCopione };
await mkdir(cartella, { recursive: true });
const scrivi = (nome, dati) => writeFile(path.join(cartella, nome),
  typeof dati === 'string' || Buffer.isBuffer(dati) ? dati : JSON.stringify(dati, null, 2) + '\n');

try {
  const config = voceApprovata(await leggiConfig());
  const copione = validaCopione(JSON.parse(await readFile(fileCopione, 'utf8')));

  // 2. testo -> audio, sempre con la voce approvata
  console.log(`· voce ${config.personaggio} (${config.voice_id}), modello ${config.modello_tts}`);
  const { audio, allineamento } = await sintetizza(testoDaLeggere(copione, config.modello_tts), config);
  await scrivi('narrazione.mp3', audio);

  // 3. controlli: avvio immediato, durata, ritmo, pronuncia
  const listaParole = parole(allineamento);
  const durata = allineamento.character_end_times_seconds.at(-1) || 0;
  const atteso = testoPulito(copione);
  const sentito = await trascrivi(audio, config);
  const errore = erroreParole(atteso, sentito);
  const avvio = listaParole[0]?.inizio ?? 0;
  const pausaMassima = listaParole.slice(1).reduce((m, w, i) => Math.max(m, w.inizio - listaParole[i].fine), 0);
  const esito = verifica({ durata, numeroParole: listaParole.length, errore, avvio, pausaMassima, config });
  await scrivi('rapporto.json', {
    durataSecondi: Math.round(durata * 100) / 100,
    parole: listaParole.length,
    paroleAlMinuto: esito.paroleAlMinuto,
    avvioSecondi: Math.round(avvio * 100) / 100,
    pausaMassimaSecondi: Math.round(pausaMassima * 100) / 100,
    erroreParole: Math.round(errore * 1000) / 1000,
    trascrizione: sentito,
    problemi: esito.problemi
  });

  // 4. sottotitoli  5. bocca
  await scrivi('sottotitoli.srt', srt(sottotitoli(listaParole)));
  await scrivi('bocca.json', { voice_id: config.voice_id, chiavi: bocca(allineamento) });

  if (!esito.ok) {
    Object.assign(stato, { esito: 'da_ricontrollare', problemi: esito.problemi });
    await scrivi('stato.json', stato);
    esito.problemi.forEach(p => console.log(`  ! ${p}`));
    process.exit(1);
  }
  Object.assign(stato, { esito: 'pronta', durataSecondi: durata });
  await scrivi('stato.json', stato);
  console.log(`· narrazione pronta: ${durata.toFixed(1)} s, ${esito.paroleAlMinuto} parole/min`);
} catch (e) {
  Object.assign(stato, { esito: 'errore', codice: e.codice || 'ERRORE_IMPREVISTO', messaggio: e.message });
  await scrivi('stato.json', stato);
  console.error(`! [${stato.codice}] ${e.message}`);
  process.exit(1);
}

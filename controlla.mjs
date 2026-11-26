/* =====================================================================
   MORVA — controllo automatico del sito.
   Percorre il sito come farebbe una persona e registra tutto quello che
   non funziona. Gira fuori dal sito, su un calendario, non come una
   finestra lasciata aperta.

   Si annuncia come MORVA-MONITOR e visita con ?monitor=true: il sito lo
   riconosce e non lo conta fra i visitatori.

   Uso:  node monitor/controlla.mjs [indirizzo]
   ===================================================================== */
import { chromium, devices } from 'playwright';
import { mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';

const SITO = process.argv[2] || process.env.MORVA_URL || 'https://morva-studios.netlify.app';
const NOME_AGENTE = 'MORVA-MONITOR';
const CARTELLA = 'rapporti';
const LENTO_MS = 6000;          // oltre questo il caricamento e' anomalo

/* i tre dispositivi su cui controlliamo */
const DISPOSITIVI = [
  { nome: 'desktop', viewport: { width: 1440, height: 900 }, isMobile: false },
  { nome: 'tablet', ...devices['iPad (gen 7)'] },
  { nome: 'telefono', ...devices['iPhone 13'] }
];

const problemi = [];
const ora = () => new Date().toISOString();

function segnala(p) {
  problemi.push({ quando: ora(), ...p });
  const gravita = p.tipo === 'lentezza' ? '~' : '!';
  console.log(`  ${gravita} [${p.tipo}] ${p.dettaglio}`);
}

/* ---------------------------------------------------------------------
   Un passaggio del percorso: fa qualcosa e verifica che sia successo.
   --------------------------------------------------------------------- */
async function passo(pagina, nome, azione, verifica) {
  const inizio = Date.now();
  try {
    await azione();
    const ok = await verifica();
    const durata = Date.now() - inizio;
    if (!ok) {
      segnala({
        tipo: 'passo fallito', passo: nome, url: pagina.url(),
        dettaglio: `${nome}: l'azione non ha prodotto l'effetto atteso`,
        durataMs: durata
      });
      return false;
    }
    if (durata > LENTO_MS) {
      segnala({
        tipo: 'lentezza', passo: nome, url: pagina.url(),
        dettaglio: `${nome}: ${durata} ms`, durataMs: durata
      });
    }
    console.log(`  · ${nome} (${durata} ms)`);
    return true;
  } catch (e) {
    segnala({
      tipo: 'passo fallito', passo: nome, url: pagina.url(),
      dettaglio: `${nome}: ${e.message}`, durataMs: Date.now() - inizio
    });
    return false;
  }
}

/* ---------------------------------------------------------------------
   Il giro completo su un dispositivo.
   --------------------------------------------------------------------- */
async function giro(browser, dispositivo) {
  console.log(`\n── ${dispositivo.nome} ──`);
  const contesto = await browser.newContext({
    ...dispositivo,
    userAgent: (dispositivo.userAgent || 'Mozilla/5.0') + ' ' + NOME_AGENTE,
    ignoreHTTPSErrors: false
  });
  const pagina = await contesto.newPage();
  /* Alcuni errori li provochiamo noi apposta: entrare con una password
     sbagliata DEVE rispondere 400. Mentre lo facciamo alziamo questa
     bandiera, se no l'agent segnala come guasto il proprio controllo
     riuscito — e un allarme che suona a vuoto ogni ora smette di essere
     letto dopo una settimana. */
  let attesoErrore = null;

  const viewport = () => {
    const v = pagina.viewportSize();
    return v ? `${v.width}x${v.height}` : '?';
  };

  /* --- tutto quello che il browser lamenta, lo raccogliamo --- */
  pagina.on('console', m => {
    if (m.type() !== 'error') return;
    const t = m.text();
    // il rumore di terze parti non e' un problema del sito
    if (/favicon|Download the React|chrome-extension/i.test(t)) return;
    // il browser fa anche l'eco in console dello stesso errore voluto,
    // ma nel messaggio non c'e' l'indirizzo: si riconosce dal codice
    if (attesoErrore && /status of 4\d\d/.test(t)) return;
    segnala({ tipo: 'errore javascript', url: pagina.url(), dettaglio: t, viewport: viewport() });
  });
  pagina.on('pageerror', e => {
    segnala({ tipo: 'eccezione', url: pagina.url(), dettaglio: e.message, viewport: viewport() });
  });
  pagina.on('requestfailed', r => {
    const motivo = r.failure()?.errorText || 'sconosciuto';
    if (/ERR_ABORTED/.test(motivo)) return;   // navigazioni interrotte: normale
    segnala({
      tipo: 'richiesta fallita', url: pagina.url(), risorsa: r.url(),
      dettaglio: `${r.url()} — ${motivo}`, viewport: viewport()
    });
  });
  pagina.on('response', r => {
    const stato = r.status();
    if (stato < 400) return;
    if (attesoErrore && attesoErrore.test(r.url())) return;
    segnala({
      tipo: stato >= 500 ? 'errore server' : 'errore ' + stato,
      url: pagina.url(), risorsa: r.url(), stato,
      dettaglio: `${stato} su ${r.url()}`, viewport: viewport()
    });
  });

  /* --- 1. la schermata iniziale --- */
  const partenza = Date.now();
  const risposta = await pagina.goto(SITO + '/?monitor=true', {
    waitUntil: 'domcontentloaded', timeout: 30000
  });
  const caricamento = Date.now() - partenza;

  if (!risposta || !risposta.ok()) {
    segnala({
      tipo: 'pagina non caricata', url: SITO, stato: risposta ? risposta.status() : 0,
      dettaglio: `la home ha risposto ${risposta ? risposta.status() : 'niente'}`,
      durataMs: caricamento, viewport: viewport()
    });
    await scatta(pagina, dispositivo.nome, 'home-non-caricata');
    await contesto.close();
    return;
  }
  if (caricamento > LENTO_MS) {
    segnala({
      tipo: 'lentezza', url: SITO, dettaglio: `la home ha impiegato ${caricamento} ms`,
      durataMs: caricamento, viewport: viewport()
    });
  }

  /* --- 2. la pagina non e' bianca --- */
  await passo(pagina, 'la home mostra il marchio', async () => {
    await pagina.waitForSelector('.wordmark', { timeout: 10000 });
  }, async () => {
    const testo = await pagina.textContent('.wordmark');
    return !!testo && testo.replace(/\s/g, '').toUpperCase().includes('MORVA');
  });

  /* --- 3. i caratteri sono arrivati --- */
  await passo(pagina, 'i caratteri sono caricati', async () => {
    await pagina.evaluate(() => document.fonts.ready);
  }, async () => {
    const mancanti = await pagina.evaluate(() =>
      ['Anton', 'Archivo'].filter(f => !document.fonts.check('16px "' + f + '"')));
    if (mancanti.length) {
      segnala({
        tipo: 'font non caricato', url: pagina.url(),
        dettaglio: 'caratteri mancanti: ' + mancanti.join(', '), viewport: viewport()
      });
    }
    return true;
  });

  /* --- 4. il menu si apre --- */
  await passo(pagina, 'il menu si apre', async () => {
    await pagina.click('#menu', { timeout: 8000 });
  }, async () => pagina.getAttribute('#index', 'data-open').then(v => v === 'true'));

  /* --- 5. le voci del menu ci sono e sono cliccabili --- */
  await passo(pagina, 'le voci del menu sono cliccabili', async () => {
    await pagina.waitForSelector('#index button:not([hidden])', { timeout: 6000 });
  }, async () => {
    const voci = await pagina.$$('#index button:not([hidden])');
    for (const v of voci) {
      if (!(await v.isEnabled()) || !(await v.isVisible())) {
        segnala({
          tipo: 'elemento non cliccabile', url: pagina.url(),
          dettaglio: 'voce di menu inerte: ' + (await v.textContent()).trim(),
          viewport: viewport()
        });
        return false;
      }
    }
    return voci.length >= 3;
  });

  /* --- 6. si arriva ad Accesso --- */
  await passo(pagina, 'si apre la pagina Accesso', async () => {
    await pagina.click('#voce-accesso', { timeout: 8000 });
    await pagina.waitForTimeout(600);
  }, async () => pagina.getAttribute('#view-accesso', 'data-open').then(v => v === 'true'));

  /* --- 7. il modulo d'accesso e' utilizzabile --- */
  await passo(pagina, 'il modulo d\'accesso risponde', async () => {
    await pagina.fill('#e-email', 'controllo@morva.test');
    await pagina.fill('#e-pw', 'password-di-prova');
  }, async () => {
    const v = await pagina.inputValue('#e-email');
    return v === 'controllo@morva.test';
  });

  /* --- 8. una password sbagliata produce un messaggio, non il silenzio --- */
  attesoErrore = /\/auth\/v1\/token/;
  await passo(pagina, 'l\'accesso sbagliato viene spiegato', async () => {
    await pagina.click('#btn-entra', { timeout: 8000 });
    await pagina.waitForTimeout(2600);
  }, async () => {
    const err = (await pagina.textContent('#err-entra')) || '';
    if (!err.trim()) {
      segnala({
        tipo: 'autenticazione muta', url: pagina.url(),
        dettaglio: 'credenziali sbagliate senza nessun messaggio',
        viewport: viewport()
      });
      return false;
    }
    return true;
  });

  attesoErrore = null;

  /* --- 9. le sezioni pubbliche si aprono --- */
  for (const sezione of ['opere', 'studio', 'tessera']) {
    await passo(pagina, `si apre la sezione ${sezione}`, async () => {
      await pagina.goto(`${SITO}/?monitor=true#${sezione}`, { waitUntil: 'domcontentloaded' });
      await pagina.waitForTimeout(900);
    }, async () => pagina.getAttribute(`#view-${sezione}`, 'data-open').then(v => v === 'true'));
  }

  /* --- 10. le immagini ci sono tutte --- */
  await passo(pagina, 'le immagini sono caricate', async () => {}, async () => {
    const rotte = await pagina.evaluate(() =>
      [...document.images]
        .filter(i => i.complete && i.naturalWidth === 0)
        .map(i => i.currentSrc || i.src));
    rotte.forEach(src => segnala({
      tipo: 'immagine non caricata', url: pagina.url(), risorsa: src,
      dettaglio: src, viewport: viewport()
    }));
    return rotte.length === 0;
  });

  /* --- 11. i collegamenti verso fuori rispondono --- */
  await passo(pagina, 'i collegamenti esterni rispondono', async () => {}, async () => {
    const link = await pagina.evaluate(() =>
      [...document.querySelectorAll('a[href^="http"]')].map(a => a.href));
    for (const l of [...new Set(link)]) {
      try {
        const r = await fetch(l, { method: 'HEAD', redirect: 'follow' });
        if (r.status >= 400) {
          segnala({
            tipo: 'link rotto', url: pagina.url(), risorsa: l, stato: r.status,
            dettaglio: `${r.status} su ${l}`, viewport: viewport()
          });
        }
      } catch (e) {
        segnala({
          tipo: 'link irraggiungibile', url: pagina.url(), risorsa: l,
          dettaglio: `${l} — ${e.message}`, viewport: viewport()
        });
      }
    }
    return true;
  });

  /* --- 12. un indirizzo inventato non deve lasciare la pagina bianca --- */
  await passo(pagina, 'un indirizzo inesistente riporta alla home', async () => {
    await pagina.goto(`${SITO}/?monitor=true#questa-sezione-non-esiste`, { waitUntil: 'domcontentloaded' });
    await pagina.waitForTimeout(800);
  }, async () => {
    const aperte = await pagina.$$('.view[data-open="true"]');
    return aperte.length === 0;   // nessuna vista aperta: siamo tornati alla home
  });

  /* --- 13. il conteggio non ci ha visti --- */
  await passo(pagina, 'il controllo non risulta fra le visite', async () => {}, async () => {
    const escluso = await pagina.evaluate(() =>
      /MORVA-MONITOR/i.test(navigator.userAgent) ||
      new URLSearchParams(location.search).get('monitor') === 'true');
    if (!escluso) {
      segnala({
        tipo: 'monitoraggio contato', url: pagina.url(),
        dettaglio: 'il sito non ha riconosciuto il controllo: rischia di finire nelle statistiche',
        viewport: viewport()
      });
    }
    return escluso;
  });

  if (problemi.length) await scatta(pagina, dispositivo.nome, 'stato-finale');
  await contesto.close();
}

async function scatta(pagina, dispositivo, nome) {
  try {
    await mkdir(CARTELLA, { recursive: true });
    const file = path.join(CARTELLA, `${stampaData()}-${dispositivo}-${nome}.png`);
    await pagina.screenshot({ path: file, fullPage: false });
    console.log(`  → immagine salvata: ${file}`);
  } catch (e) {
    console.log(`  → non sono riuscito a salvare l'immagine: ${e.message}`);
  }
}

const stampaData = () => new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);

/* ---------------------------------------------------------------------
   Prima di tutto: il sito esiste ancora? Se l'indirizzo non porta più
   da nessuna parte, i tre giri producono solo decine di errori confusi.
   Meglio una riga sola che dica cosa è successo davvero.
   --------------------------------------------------------------------- */
async function esiste() {
  let r;
  try {
    r = await fetch(SITO + '/?monitor=true', {
      headers: { 'user-agent': 'Mozilla/5.0 ' + NOME_AGENTE },
      redirect: 'follow',
      signal: AbortSignal.timeout(30000)
    });
  } catch (e) {
    const causa = e.cause?.code || e.name || e.message;
    const dettaglio = /ENOTFOUND|EAI_AGAIN/.test(causa)
      ? `l'indirizzo ${SITO} non esiste più: nessun server lo trova (${causa})`
      : `${SITO} non risponde (${causa})`;
    return { tipo: 'sito irraggiungibile', url: SITO, stato: 0, dettaglio };
  }
  if (r.ok) return null;

  const testo = await r.text().catch(() => '');
  // la pagina di Netlify per un sito che non c'è: "Not Found - Request ID"
  if (r.status === 404 && /netlify/i.test(r.headers.get('server') || '') &&
      /Not Found - Request ID/i.test(testo)) {
    return {
      tipo: 'sito sparito', url: SITO, stato: 404,
      dettaglio: `su Netlify non c'è più nessun sito a ${SITO}: ` +
        'è stato rinominato, eliminato, o l\'account ha un problema. ' +
        'Controlla su app.netlify.com.'
    };
  }
  return {
    tipo: 'sito non disponibile', url: SITO, stato: r.status,
    dettaglio: `la home di ${SITO} risponde ${r.status}`
  };
}

/* nel riepilogo della pagina di GitHub e come avviso in cima al lavoro */
async function avvisaGitHub(p) {
  console.log(`::error title=MORVA: ${p.tipo}::${p.dettaglio}`);
  if (!process.env.GITHUB_STEP_SUMMARY) return;
  await writeFile(process.env.GITHUB_STEP_SUMMARY,
    `## ⚠ MORVA: ${p.tipo}\n\n${p.dettaglio}\n`, { flag: 'a' });
}

/* --------------------------------------------------------------------- */
(async () => {
  console.log(`MORVA — controllo di ${SITO}`);
  console.log(`${ora()}\n`);

  const assenza = await esiste();
  if (assenza) {
    segnala(assenza);
    await avvisaGitHub(assenza);
    await chiudi();
  }

  const browser = await chromium.launch();
  for (const d of DISPOSITIVI) {
    try {
      await giro(browser, d);
    } catch (e) {
      segnala({ tipo: 'controllo interrotto', url: SITO, dettaglio: `${d.nome}: ${e.message}` });
    }
  }
  await browser.close();
  await chiudi();
})();

/* scrive il rapporto e termina: 1 se c'è qualcosa che non va */
async function chiudi() {
  await mkdir(CARTELLA, { recursive: true });
  const rapporto = {
    quando: ora(),
    sito: SITO,
    dispositivi: DISPOSITIVI.map(d => d.nome),
    problemi: problemi.length,
    dettagli: problemi
  };
  const file = path.join(CARTELLA, `${stampaData()}.json`);
  await writeFile(file, JSON.stringify(rapporto, null, 2), 'utf8');

  console.log('\n────────────────────────────');
  if (!problemi.length) {
    console.log('Nessun problema. Il sito risponde su tutti e tre i dispositivi.');
  } else {
    const perTipo = {};
    problemi.forEach(p => { perTipo[p.tipo] = (perTipo[p.tipo] || 0) + 1; });
    console.log(`${problemi.length} problemi:`);
    Object.entries(perTipo).forEach(([t, n]) => console.log(`  ${String(n).padStart(3)}  ${t}`));
  }
  console.log(`rapporto: ${file}`);

  process.exit(problemi.length ? 1 : 0);
}

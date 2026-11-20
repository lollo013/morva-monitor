# Stile di montaggio del Professor Aurelio — ritmo visivo alto

Stato: **approvato** il 18 novembre 2026 dalla dashboard privata (demo «Perché il cielo è azzurro?»).
Vale per tutti i video successivi.

## Regole
1. **Un cambio visivo significativo ogni 2–3 secondi**, sempre con uno scopo narrativo:
   taglio di inquadratura, zoom sul dettaglio nominato, evento nella scena (es. il prisma che si apre).
2. **Primi 3 secondi**: si apre con il fenomeno, non con il Professore fermo. **Mai iniziare con «Ehi»**:
   la prima frase nomina subito l'argomento e aggancia (es. «Token di Fortnite: sicuramente ne hai
   sentito parlare. Ora ti spiego bene che cos'è.»). La domanda è scritta
   grande dal primo fotogramma. La voce parte subito (controllo: silenzio iniziale ≤ 0,15 s).
3. **Il Professore è sempre in scena ed è il protagonista.** Non esistono inquadrature senza di lui.
   Cambia solo il punto di vista, sempre con l'immagine originale: `sfondo` (la scena dietro di lui,
   lui davanti a mezzo busto), `mezzo_busto` (lui grande, scena accanto), `affiancati` (lui intero),
   `angolo_dx` / `angolo_sx` (lui in basso, scena sopra), `primo_piano`. Lo sfondo bianco attorno
   alla figura viene tolto; occhi e riflessi restano pieni. Gesti: l'avambraccio si solleva dal
   gomito (0–6°, di più sulle parole chiave) e la mano gesticola dal polso.
4. **Scene animate**: si anima il fenomeno spiegato (luce che si scompone, onde, molecole, percorso
   nell'atmosfera), non immagini ferme.
5. **Formato e area sicura TikTok**: sempre 9:16, 1080×1920 (il formato nativo: niente bande).
   Testi, scene e volto del Professore restano dentro x 60–900 e y 230–1480: sopra c'è «Seguiti / Per
   te», a destra i pulsanti, in basso nome e descrizione. Nessuna barra di avanzamento nostra.
   Controllo: `python3 aurelio/video/interfaccia.py <cartella> <secondi>` sovrappone l'interfaccia.
   Pronuncia: i nomi stranieri si scrivono in alfabeto fonetico tra barre nel testo per la voce
   (es. Fortnite → `/ˈfɔːrtnaɪt/`).
6. **Sottotitoli**: 1–3 parole per volta, agganciati alle pause vere della voce; evidenziate solo
   le parole chiave; comparsa leggera; mai sul volto o sugli elementi principali; dentro l'area
   sicura 9:16.
6. **Montaggio**: tagli netti con breve zoom di ingresso; spinta lenta di camera; piccolo colpo di
   zoom sulle parole chiave. Niente dissolvenze lunghe, niente zoom senza motivo.
7. **Durata**: 20–35 secondi. 0–3 s gancio · 3–10 s fenomeno · 10–25 s spiegazione · fine: risposta
   e invito (commenta, like, segui).

## Controllo qualità prima della consegna
Primi 3 s interessanti · nessuna inquadratura oltre ~4 s senza un evento visivo · immagini pertinenti ·
sottotitoli sincronizzati · animazioni fluide · Professore coerente · ritmo dinamico ma leggibile ·
spiegazione comprensibile.

## Come si fa un episodio
`python3 aurelio/video/regia.py <cartella> aurelio/video/episodi/<nome>.regia.json`
Il file di regia contiene le frasi, le parole chiave e le inquadrature, ognuna agganciata alla
parola che la fa partire (`"da": "luce#2"` = seconda volta che dice «luce»).

## Video in inglese (YouTube)
- Voce: **Professor Aurelio (US English)**, voice_id `AF9AzE9ZXIFZ89nea5pS` (config/voce-en.json), pronuncia americana standard.
  Scelta dall'utente (US1) il 19/11/2026. Per l'italiano resta A2.
- Formato 16:9, 1920×1080; il Professore resta in scena in ogni inquadratura (primo piano, accanto alla lavagna, figura intera).
- Cifre in dollari e dati internazionali; mai «not financial advice» omesso nei video di finanza.
- Sottotitoli YouTube: **frasi intere** (1-2 righe, banda chiara in basso), tempi presi parola per parola dalla
  trascrizione ElevenLabs dell'audio (`tempi_parole` nella regia), parole chiave solo in rosso. Si allega anche il file .srt.

## Pubblico (dati dell'utente, 20/11/2026)
- I video che sono piaciuti di più: **«La scuola assomiglia a una prigione?»** e **«Duemila euro e la regola 50-30-20»**.
- Fascia d'età: **14-26 anni** (studenti delle superiori, universitari, primi lavori).
- Temi che funzionano: scuola e studio, soldi e primo stipendio, vita da ragazzi; tono da amico che sta dalla loro parte,
  critica ai sistemi (scuola, app) senza colpevolizzare chi guarda, poi un consiglio concreto e subito applicabile.
- Esempi e cifre devono parlare a quell'età: compiti, verifiche, paghetta, primo stipendio, telefono, social.

## Sincronia voce-sottotitoli (obbligatoria)
- I tempi di ogni parola vengono dalla trascrizione ElevenLabs dell'audio vero (`tempi_parole`), mai stimati, tranne
  nelle anteprime mute.
- Le parole scritte in un modo e pronunciate in un altro vanno nelle `equivalenze` della regia
  (es. "machine" → "mascìn", "73" → "settantatré"), così anche loro hanno il tempo esatto.
- Il sottotitolo nuovo compare appena inizia la sua prima parola; il precedente non resta mai sovrapposto.
- Prima di consegnare: `python3 video/verifica_sync.py <cartella> <regia.json>` deve dare **0 non allineati**.

## Anteprima muta prima (regola fissa)
- Per ogni nuovo video si manda **prima l'anteprima senza voce**: scene, inquadrature e sottotitoli con tempi stimati,
  il Professore che muove la bocca sulle parole. La voce ElevenLabs si genera **solo dopo il «Vai»** dell'utente.

## Invito a commentare a metà video
- Dopo il dato più forte, il Professore fa una domanda diretta in primo piano («Tu come studi?») e dice
  «Scrivilo nei commenti. Ti do due secondi.»; poi appare la scheda grande con la domanda e il **conto alla rovescia 2, 1**
  (scena `commenta`). La voce fa una pausa vera di 2 secondi (`pausa_dopo` nella scheda).

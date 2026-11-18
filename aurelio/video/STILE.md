# Stile di montaggio del Professor Aurelio — ritmo visivo alto

Stato: **in attesa di approvazione** (demo «Perché il cielo è azzurro?» nella dashboard privata).
Quando viene approvato, vale per tutti i video successivi; fino ad allora resta lo stile precedente.

## Regole
1. **Un cambio visivo significativo ogni 2–3 secondi**, sempre con uno scopo narrativo:
   taglio di inquadratura, zoom sul dettaglio nominato, evento nella scena (es. il prisma che si apre).
2. **Primi 3 secondi**: si apre con il fenomeno, non con il Professore fermo. La domanda è scritta
   grande dal primo fotogramma. La voce parte subito (controllo: silenzio iniziale ≤ 0,15 s).
3. **Il Professore è sempre in scena ed è il protagonista.** Non esistono inquadrature senza di lui.
   Cambia solo il punto di vista, sempre con l'immagine originale: `sfondo` (la scena dietro di lui,
   lui davanti a mezzo busto), `mezzo_busto` (lui grande, scena accanto), `affiancati` (lui intero),
   `angolo_dx` / `angolo_sx` (lui in basso, scena sopra), `primo_piano`. Lo sfondo bianco attorno
   alla figura viene tolto; occhi e riflessi restano pieni. Gesti: l'avambraccio si solleva dal
   gomito (0–6°, di più sulle parole chiave) e la mano gesticola dal polso.
4. **Scene animate**: si anima il fenomeno spiegato (luce che si scompone, onde, molecole, percorso
   nell'atmosfera), non immagini ferme.
5. **Sottotitoli**: 1–3 parole per volta, agganciati alle pause vere della voce; evidenziate solo
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

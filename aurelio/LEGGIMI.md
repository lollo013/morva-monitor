# La voce del Professor Aurelio

Il Professor Aurelio ha due identità fisse: l'**immagine** originale e la
**voce**. La voce è stata creata con ElevenLabs Voice Design e si usa
sempre la stessa, in ogni video.

## Stato attuale

`config/voce.json` → `"stato": "approvata"`, voce **A2** (terzo giro),
salvata nella libreria ElevenLabs come «Professor Aurelio»
(`voice_id` `Urn0f9O0p74gbKH8ERH3`). È l'unica voce che `narra.mjs`
usa. Le voci degli altri giri sono scartate.

Primo video pronto da narrare: `esempi/sogni.json` («Perché
dimentichiamo i sogni?»), con le fonti nel file.

## Come nasce la narrazione di un video

```bash
node aurelio/narra.mjs aurelio/esempi/cielo-azzurro.json uscita/
```

1. **Copione verificato**: un JSON con `"verificato": true` e le parti
   divise per fase (`apertura`, `spiegazione`, `scoperta`, `conclusione`).
2. **Audio**: ElevenLabs interpreta il copione con la voce approvata.
   Ogni fase riceve un'indicazione di tono fra quelle documentate da
   ElevenLabs: `[curious]` in apertura, `[excited]` nella spiegazione,
   `[surprised]` sulla scoperta, `[warmly]` nella conclusione. Le parole
   da sottolineare si scrivono `*così*` e la voce le enfatizza. Il
   modello non ha un comando di velocità: il ritmo si costruisce con
   frasi brevi e punteggiatura.
3. **Controlli**: la voce deve partire entro 0,15 s, nessuna pausa oltre
   0,5 s, ritmo fra 155 e 195 parole al minuto (obiettivo 160–185),
   durata massima 60 s, e pronuncia: l'audio viene
   ritrascritto e confrontato col copione.
4. **Sottotitoli**: `sottotitoli.srt`, sincronizzati sui tempi reali di
   ogni parola.
5. **Bocca**: `bocca.json`, le forme della bocca nel tempo (labbra
   chiuse su m/b/p, vocali, riposo nelle pause) per animare il
   Professore.
6. **Montaggio**: `narrazione.mp3`, `sottotitoli.srt` e `bocca.json`
   sono i tre ingredienti che il montaggio finale riceve.

## Quando qualcosa va storto

Il lavoro si ferma con codice d'uscita 1 e `stato.json` dice perché
(`VOCE_NON_APPROVATA`, `CHIAVE_MANCANTE`, `ELEVENLABS_NON_DISPONIBILE`,
`VOCE_NON_TROVATA`…). Non viene **mai** usata una voce diversa da quella
approvata, nemmeno come ripiego.

## La chiave di ElevenLabs

Solo sul server, nella variabile d'ambiente `ELEVENLABS_API_KEY`. Su
GitHub: *Settings → Secrets and variables → Actions → New repository
secret*. Mai nel codice, nei file JSON o in una pagina web: questo
repository è pubblico.

## Prove

```bash
npm test
```

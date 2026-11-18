# La voce del Professor Aurelio

Il Professor Aurelio ha due identità fisse: l'**immagine** originale e la
**voce**. La voce è stata creata con ElevenLabs Voice Design e si usa
sempre la stessa, in ogni video.

## Stato attuale

`config/voce.json` → `"stato": "in_attesa_di_approvazione"`.

Le tre voci candidate (A, B, C) si ascoltano nella dashboard privata.
Finché una non viene approvata lì, `narra.mjs` si rifiuta di partire.

Dopo l'approvazione la voce scelta viene salvata nella libreria
ElevenLabs come «Professor Aurelio», e il suo `voice_id` va in
`config/voce.json` con `"stato": "approvata"`. Da quel momento non si
cambia senza una nuova approvazione.

## Come nasce la narrazione di un video

```bash
node aurelio/narra.mjs aurelio/esempi/cielo-azzurro.json uscita/
```

1. **Copione verificato**: un JSON con `"verificato": true` e le parti
   divise per fase (`domanda`, `spiegazione`, `scoperta`, `conclusione`).
2. **Audio**: ElevenLabs legge il copione con la voce approvata. Ogni
   fase riceve un'indicazione sobria di tono (pensieroso, calmo,
   incuriosito, caloroso).
3. **Controlli**: durata massima, ritmo fra 110 e 170 parole al minuto,
   e pronuncia: l'audio viene ritrascritto e confrontato col copione.
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

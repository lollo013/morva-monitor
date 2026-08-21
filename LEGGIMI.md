# Controllo del sito MORVA

Percorre [morva-studios.netlify.app](https://morva-studios.netlify.app) come farebbe
una persona e registra tutto quello che non funziona.

Gira **ogni ora** sui computer di GitHub. Non serve lasciare niente acceso.

## Cosa controlla

Su **desktop, tablet e telefono**, quattordici verifiche per dispositivo:

- la home si carica e mostra il marchio — non una schermata bianca
- i caratteri Anton e Archivo arrivano davvero
- il menu si apre
- ogni voce del menu è cliccabile e non inerte
- si arriva alla pagina Accesso
- il modulo d'accesso risponde
- una password sbagliata produce un messaggio, non il silenzio
- le sezioni Opere, Studio e Tessera si aprono
- nessuna immagine è rotta
- i collegamenti verso l'esterno rispondono
- un indirizzo inesistente riporta alla home invece di lasciare il vuoto
- il sito riconosce il controllo e non lo conta fra i visitatori

In parallelo raccoglie tutto quello che il browser lamenta: errori JavaScript,
eccezioni, richieste fallite, 404, 500, e ogni caricamento oltre i sei secondi.

## Cosa non fa

**Non risulta fra le visite.** Si presenta come `MORVA-MONITOR` e naviga con
`?monitor=true`. Il sito riconosce entrambe le cose e non registra niente:
visitatori, sessioni e statistiche restano quelle delle persone vere.

## Quando trova qualcosa

Il lavoro fallisce, GitHub manda un'email, e negli allegati trovi:

- un rapporto JSON con data, indirizzo, tipo di errore, codice HTTP,
  risorsa coinvolta, durata, viewport e dispositivo
- uno screenshot del momento in cui si è rotto

Gli allegati restano trenta giorni.

## Lanciarlo a mano

Dal sito di GitHub: scheda **Actions** → *Controllo del sito* → **Run workflow**.

Sul proprio computer:

```bash
npm install
npx playwright install chromium
node controlla.mjs
```

Si può puntare a un altro indirizzo passandolo come argomento:

```bash
node controlla.mjs https://qualche-altro-sito.example
```

## Perché non è un browser lasciato aperto

Una finestra aperta smette di controllare appena il computer si spegne, e
nessuno se ne accorge. Un lavoro su calendario parte da solo, gira su una
macchina che non è la tua, e quando fallisce te lo dice.

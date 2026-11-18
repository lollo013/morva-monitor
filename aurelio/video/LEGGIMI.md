# Montaggio 2D del Professor Aurelio

- `anima.py`: anima l'immagine originale (respiro, ondeggio, mano che gesticola,
  battito di ciglia, «Sorriso», «Scoperta», bocca che segue il volume della voce).
- `disegni.py`: illustrazioni 2D dello scenario, nello stile del personaggio.
- `monta.py`: compone il video verticale 1080x1920 con sottotitoli, schede e scene.

Uso: `python3 aurelio/video/monta.py <cartella>`. La cartella deve contenere
`figura_pulita.png` (la figura intera ritagliata dalla scheda originale) e
l'audio della voce approvata. L'immagine non è nel repository, che è pubblico.

`monta.py` legge `narrazione.mp3` (la voce A2) e ancora ogni fine frase a una
pausa vera della voce: sottotitoli, scene ed espressioni seguono il parlato.
Alla fine del video c'è solo il titolo: le fonti restano nel copione.

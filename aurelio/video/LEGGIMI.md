# Montaggio 2D del Professor Aurelio

- `anima.py`: anima l'immagine originale (respiro, ondeggio, mano che gesticola,
  battito di ciglia, «Sorriso», «Scoperta», bocca che segue il volume della voce).
- `disegni.py`: illustrazioni 2D dello scenario, nello stile del personaggio.
- `monta.py`: compone il video verticale 1080x1920 con sottotitoli, schede e scene.

Uso: `python3 aurelio/video/monta.py <cartella>`. La cartella deve contenere
`figura_pulita.png` (la figura intera ritagliata dalla scheda originale) e
l'audio della voce approvata. L'immagine non è nel repository, che è pubblico.

Per ora `monta.py` è tarato sull'anteprima «Perché dimentichiamo i sogni?».
Quando la narrazione completa sarà disponibile, i tempi verranno dai tempi
reali della voce invece che dalla stima.

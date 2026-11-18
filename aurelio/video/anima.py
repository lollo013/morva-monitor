"""Animazione 2D del Professor Aurelio a partire dall'immagine originale.

Tutto e' ottenuto dall'immagine approvata, senza ridisegnare il personaggio:
- respiro e leggero ondeggiare del corpo
- la mano alzata che gesticola (ruota attorno al polso)
- occhi: battito di ciglia e occhi chiusi sorridenti (espressione «Sorriso» della scheda)
- bocca: si apre mentre parla; «o» di stupore (espressione «Scoperta» della scheda)
Coordinate in pixel dell'immagine sorgente (figura_pulita.png, 600x1312).
"""
import math
from PIL import Image, ImageDraw

BG = (253, 252, 251)
PELLE = (252, 186, 122)
LINEA = (30, 20, 16)
BOCCA = (92, 34, 28)

OCCHI = [  # (cx, cy, rx, ry)
    (230, 190, 22, 25),
    (309, 179, 17, 25),
]
BOCCA_C = (287, 268)
PERNO_MANO = (452, 440)
# poligono della sola mano, tagliato appena sopra il polsino della manica
POLIGONO_MANO = [(420, 300), (600, 300), (600, 452), (470, 452), (452, 430), (420, 420)]
ZONA_MANO = (418, 300, 600, 470)  # x0, y0, x1, y1


class Figura:
    def __init__(self, percorso, scala=4):
        self.base = Image.open(percorso).convert('RGB')
        self.s = scala  # sovracampionamento per i tratti disegnati
        x0, y0, x1, y1 = ZONA_MANO
        mano = self.base.crop((x0, y0, x1, y1)).convert('RGBA')
        dentro = Image.new('L', mano.size, 0)
        ImageDraw.Draw(dentro).polygon([(x - x0, y - y0) for x, y in POLIGONO_MANO], fill=255)
        px = mano.load(); pd = dentro.load()
        for y in range(mano.height):
            for x in range(mano.width):
                r, g, b, _ = px[x, y]
                if pd[x, y] == 0 or (r > 244 and g > 240 and b > 236):
                    px[x, y] = (r, g, b, 0)
        self.mano = mano
        # base senza la mano: al suo posto lo sfondo
        self.senza_mano = self.base.copy()
        d = ImageDraw.Draw(self.senza_mano)
        # si cancella solo la mano lontana dal taglio: vicino al polso restano i pixel
        # originali, cosi' la mano ruotata li copre senza lasciare fessure
        m = mano.split()[3].copy()
        ImageDraw.Draw(m).polygon([(x - x0, y - y0) for x, y in
                                   [(420, 408), (452, 416), (466, 432), (478, 444), (478, 470), (418, 470)]], fill=0)
        sfondo = Image.new('RGB', mano.size, BG)
        self.senza_mano.paste(sfondo, (x0, y0), m)

    def _occhio_chiuso(self, d, cx, cy, rx, ry, felice):
        s = self.s
        d.ellipse(((cx - rx) * s, (cy - ry) * s, (cx + rx) * s, (cy + ry) * s), fill=PELLE)
        w = 4 * s
        if felice:   # arco verso l'alto, come nell'espressione «Sorriso»
            d.arc(((cx - rx + 3) * s, (cy - 4) * s, (cx + rx - 3) * s, (cy + 18) * s), 200, 340, fill=LINEA, width=w)
        else:        # palpebra chiusa
            d.arc(((cx - rx + 2) * s, (cy - 14) * s, (cx + rx - 2) * s, (cy + 8) * s), 20, 160, fill=LINEA, width=w)

    def quadro(self, angolo_mano=0.0, ondeggio=0.0, respiro=0.0, occhi='aperti', bocca=0.0, stupore=False):
        """occhi: 'aperti' | 'chiusi' | 'felici'; bocca: 0..1 apertura mentre parla."""
        im = self.senza_mano.copy()
        # mano che gesticola
        mano = self.mano.rotate(angolo_mano, resample=Image.BICUBIC, expand=False,
                                center=(PERNO_MANO[0] - ZONA_MANO[0], PERNO_MANO[1] - ZONA_MANO[1]))
        im.paste(mano, (ZONA_MANO[0], ZONA_MANO[1]), mano)
        # viso, disegnato in sovracampionamento e riportato alla scala originale
        if occhi != 'aperti' or bocca > 0.02 or stupore:
            x0, y0, x1, y1 = 190, 140, 345, 300
            s = self.s
            viso = im.crop((x0, y0, x1, y1)).resize(((x1 - x0) * s, (y1 - y0) * s), Image.BICUBIC)
            d = ImageDraw.Draw(viso)
            sposta = lambda c: (c[0] - x0, c[1] - y0)
            if occhi != 'aperti':
                for cx, cy, rx, ry in OCCHI:
                    cx, cy = sposta((cx, cy))
                    self._occhio_chiuso(d, cx, cy, rx, ry, occhi == 'felici')
            if stupore or bocca > 0.02:
                bx, by = sposta(BOCCA_C)
                if stupore:
                    w, h = 9, 11
                else:
                    w, h = 12 + 3 * bocca, 2 + 9 * bocca
                d.ellipse(((bx - w) * s, (by - h * 0.4) * s, (bx + w) * s, (by + h) * s),
                          fill=BOCCA, outline=LINEA, width=3 * s)
            im.paste(viso.resize((x1 - x0, y1 - y0), Image.LANCZOS), (x0, y0))
        # respiro: la parte alta del corpo si allunga appena
        if respiro:
            h = im.height
            alto = im.crop((0, 0, im.width, 760))
            nuova = round(760 * (1 + 0.008 * respiro))
            alto = alto.resize((im.width, nuova), Image.BICUBIC)
            tela = Image.new('RGB', im.size, BG)
            tela.paste(im.crop((0, 760, im.width, h)), (0, 760))
            tela.paste(alto, (0, 760 - nuova))
            im = tela
        # ondeggio attorno ai piedi
        if ondeggio:
            im = im.rotate(ondeggio, resample=Image.BICUBIC, center=(260, 1270), fillcolor=BG)
        return im


if __name__ == '__main__':
    import sys
    S = sys.argv[1]
    f = Figura(f'{S}/figura_pulita.png')
    pose = [
        dict(angolo_mano=-9, occhi='aperti', bocca=1.0),
        dict(angolo_mano=9, occhi='chiusi'),
        dict(angolo_mano=0, occhi='felici'),
        dict(angolo_mano=4, stupore=True, ondeggio=1.0, respiro=1.0),
    ]
    tavola = Image.new('RGB', (4 * 610, 1312), (90, 90, 90))
    for i, p in enumerate(pose):
        tavola.paste(f.quadro(**p), (i * 610, 0))
    tavola.crop((0, 100, 4 * 610, 700)).save(f'{S}/pose.png')

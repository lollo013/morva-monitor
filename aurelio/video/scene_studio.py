"""Illustrazioni originali per «Rileggere non basta». f(p, t, w, h, **extra) -> RGB."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import ImageDraw
from scene_cielo import tela, fine, font, LINEA, CREMA, ORO, ROSSO, ARANCIO, BLU, SS
from scene_inception import VERDE
from scene_procrastinazione import testo_c, SCURO, CARTA, scala
from scene_scuola import GRIGIO, omino

VIOLA = (140, 84, 200, 255)


def tc(d, x, y, s, n, col=SCURO, bordo=True):
    testo_c(d, x, y, s, font(n), col, bordo)


def e(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3


def libro(d, cx, cy, w_, h_, col=BLU):
    d.polygon([(cx - w_ / 2, cy - h_ / 2), (cx, cy - h_ / 2 + h_ * 0.06), (cx, cy + h_ / 2), (cx - w_ / 2, cy + h_ / 2 - h_ * 0.06)], fill=CARTA, outline=LINEA)
    d.polygon([(cx + w_ / 2, cy - h_ / 2), (cx, cy - h_ / 2 + h_ * 0.06), (cx, cy + h_ / 2), (cx + w_ / 2, cy + h_ / 2 - h_ * 0.06)], fill=CARTA, outline=LINEA)
    for i in range(5):
        y = cy - h_ * 0.3 + i * h_ * 0.13
        d.line((cx - w_ * 0.42, y, cx - w_ * 0.08, y + h_ * 0.03), fill=GRIGIO, width=3 * SS)
        d.line((cx + w_ * 0.08, y + h_ * 0.03, cx + w_ * 0.42, y), fill=GRIGIO, width=3 * SS)


def rilettura(p, t, w, h):
    """Apertura: il libro riletto tre volte (x1, x2, x3) e il fumetto vuoto del giorno dopo."""
    im, d = tela(w, h, (246, 242, 236, 255)); W, H = w * SS, h * SS; k = scala(w)
    libro(d, W * 0.4, H * 0.52, W * 0.66, H * 0.5)
    n = min(3, int(t * 2) + 1)
    for i in range(n):
        tc(d, W * (0.18 + 0.22 * i), H * 0.08, f'×{i + 1}', int(90 * k), BLU)
    if t > 1.6:
        d.rounded_rectangle((W * 0.7, H * 0.24, W * 0.98, H * 0.5), radius=26 * SS, fill=(255, 255, 255, 255), outline=LINEA, width=5 * SS)
        tc(d, W * 0.84, H * 0.27, '?', int(120 * k), ROSSO, bordo=False)
        tc(d, W * 0.5, H * 0.84, 'il giorno dopo: ?', int(48 * k), ROSSO)
    return fine(im, w, h)


def classifica(p, t, w, h):
    """Dieci tecniche messe a confronto (Dunlosky 2013): piu' efficaci interrogarsi e studio distribuito; meno efficaci rileggere e sottolineare."""
    im, d = tela(w, h); W, H = w * SS, h * SS; k = scala(w)
    tc(d, W / 2, H * 0.03, '10 tecniche a confronto', int(46 * k))
    gruppi = [('più efficaci', VERDE, ['interrogarti', 'studio distribuito']),
              ('così così', GRIGIO, ['…', '…', '…']),
              ('meno efficaci', ROSSO, ['rileggere', 'sottolineare', '…'])]
    y = H * 0.12; i = 0
    for nome, col, voci in gruppi:
        if t * 1.6 < i: break
        tc(d, W * 0.5, y, nome, int(34 * k), col if col != GRIGIO else GRIGIO, bordo=False)
        y += H * 0.06
        for v in voci:
            d.rounded_rectangle((W * 0.12, y, W * 0.88, y + H * 0.06), radius=12 * SS, fill=col if col != GRIGIO else (225, 222, 216, 255), outline=LINEA, width=3 * SS)
            tc(d, W * 0.5, y + H * 0.008, v, int(32 * k), CREMA if col != GRIGIO else GRIGIO, bordo=False)
            y += H * 0.07
        y += H * 0.02; i += 1
    return fine(im, w, h)


def swahili(p, t, w, h):
    """L'esperimento: carte con parole in swahili («rafiki = amico») e due gruppi di studenti."""
    im, d = tela(w, h, (244, 240, 252, 255)); W, H = w * SS, h * SS; k = scala(w)
    for i, (sw, it) in enumerate((('rafiki', 'amico'), ('maji', 'acqua'), ('kitabu', 'libro'))):
        y = H * (0.08 + 0.15 * i)
        a = e(t * 2 - i * 0.4)
        if a <= 0: continue
        d.rounded_rectangle((W * 0.12, y, W * 0.88, y + H * 0.12), radius=18 * SS, fill=(255, 255, 255, 255), outline=LINEA, width=4 * SS)
        tc(d, W * 0.32, y + H * 0.025, sw, int(46 * k), VIOLA, bordo=False)
        tc(d, W * 0.5, y + H * 0.025, '=', int(46 * k), SCURO, bordo=False)
        tc(d, W * 0.68, y + H * 0.025, it, int(46 * k), SCURO, bordo=False)
    if t > 1.2:
        omino(d, W * 0.3, H * 0.92, H * 0.2, BLU)
        libro(d, W * 0.3, H * 0.62, W * 0.2, H * 0.1)
        tc(d, W * 0.3, H * 0.92, 'rilegge', int(34 * k), BLU, bordo=False)
        omino(d, W * 0.7, H * 0.92, H * 0.2, VERDE)
        tc(d, W * 0.78, H * 0.56, '?', int(70 * k), VERDE, bordo=False)
        tc(d, W * 0.7, H * 0.92, 'si interroga', int(34 * k), VERDE, bordo=False)
    return fine(im, w, h)


def settimana_dopo(p, t, w, h):
    """Dopo una settimana: chi rileggeva ricorda circa 1/3, chi si interrogava circa l'80%."""
    im, d = tela(w, h); W, H = w * SS, h * SS; k = scala(w)
    tc(d, W / 2, H * 0.03, 'una settimana dopo', int(48 * k))
    base = H * 0.8
    for i, (nome, v, col, et) in enumerate((('rilegge', 0.35, BLU, '1/3'), ('si interroga', 0.8, VERDE, '80%'))):
        f = e(t * 1.1 - i * 0.5)
        x0 = W * (0.14 + 0.42 * i); x1 = x0 + W * 0.3
        y = base - H * 0.6 * v * f
        d.rounded_rectangle((x0, y, x1, base), radius=18 * SS, fill=col, outline=LINEA, width=5 * SS)
        if f > 0.3: tc(d, (x0 + x1) / 2, y - 70 * SS * k, et, int(64 * k), col)
        tc(d, (x0 + x1) / 2, base + 14 * SS, nome, int(38 * k), SCURO, bordo=False)
    d.line((W * 0.08, base, W * 0.92, base), fill=LINEA, width=6 * SS)
    return fine(im, w, h)


def fatica(p, t, w, h):
    """Ricordare fa fatica, ed e' quella fatica che fissa i ricordi: il cervello che solleva un peso."""
    im, d = tela(w, h, (252, 244, 238, 255)); W, H = w * SS, h * SS; k = scala(w)
    cx, cy = W * 0.5, H * 0.55
    su = 0.5 + 0.5 * math.sin(t * 4)
    by = cy - H * (0.18 + 0.06 * su)
    d.line((W * 0.18, by, W * 0.82, by), fill=LINEA, width=14 * SS)
    for x in (0.18, 0.82):
        d.rounded_rectangle((W * x - 28 * SS, by - 70 * SS, W * x + 28 * SS, by + 70 * SS), radius=10 * SS, fill=(80, 80, 90, 255))
    r = W * 0.22
    d.ellipse((cx - r, cy - r * 0.8, cx + r, cy + r * 0.8), fill=(240, 160, 180, 255), outline=LINEA, width=6 * SS)
    for i in range(4):
        d.arc((cx - r * 0.8 + i * r * 0.4, cy - r * 0.5, cx - r * 0.3 + i * r * 0.4, cy + r * 0.3), 200, 340, fill=LINEA, width=4 * SS)
    tc(d, W / 2, H * 0.84, 'la fatica fissa i ricordi', int(42 * k), ROSSO)
    return fine(im, w, h)


def metodo(p, t, w, h):
    """Il metodo in tre passi: chiudi il libro, scrivi quello che ricordi (o 3 domande), riapri e controlla."""
    im, d = tela(w, h, (238, 246, 240, 255)); W, H = w * SS, h * SS; k = scala(w)
    passi = [('1', 'chiudi il libro', BLU), ('2', 'scrivi ciò che ricordi', VIOLA), ('3', 'riapri e controlla', VERDE)]
    for i, (n_, testo, col) in enumerate(passi):
        if t * 1.8 < i: continue
        y = H * (0.1 + 0.28 * i)
        d.ellipse((W * 0.08, y, W * 0.08 + H * 0.16, y + H * 0.16), fill=col, outline=LINEA, width=5 * SS)
        tc(d, W * 0.08 + H * 0.08, y + H * 0.03, n_, int(70 * k), CREMA, bordo=False)
        d.text((W * 0.08 + H * 0.2, y + H * 0.05), testo, font=font(int(42 * k)), fill=SCURO)
    return fine(im, w, h)


SCENE = {'rilettura': rilettura, 'classifica': classifica, 'swahili': swahili, 'settimana_dopo': settimana_dopo,
         'fatica': fatica, 'metodo': metodo}

if __name__ == '__main__':
    from PIL import Image
    tav = Image.new('RGB', (3 * 420, 2 * 500), 'white')
    for i, n in enumerate(SCENE):
        tav.paste(SCENE[n](1.0, 3.0, 420, 500), ((i % 3) * 420, (i // 3) * 500))
    tav.save(sys.argv[1])

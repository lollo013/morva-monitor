"""Illustrazioni originali per «I voti misurano davvero l'intelligenza?». f(p, t, w, h, **extra) -> RGB."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import ImageDraw
from scene_cielo import tela, fine, font, gradiente, LINEA, CREMA, ORO, ROSSO, ARANCIO, BLU, SS
from scene_inception import etichetta, VERDE
from scene_procrastinazione import testo_c, SCURO, CARTA, scala
from scene_scuola import GRIGIO, omino

PENNA = (200, 40, 40, 255)
VIOLA = (140, 84, 200, 255)


def tc(d, x, y, s, n, col=SCURO, bordo=True):
    testo_c(d, x, y, s, font(n), col, bordo)


def e(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3


def foglio(d, cx, cy, w_, h_, voto=None, k=1.0, ang=0):
    d.rounded_rectangle((cx - w_ / 2, cy - h_ / 2, cx + w_ / 2, cy + h_ / 2), radius=10 * SS, fill=CARTA, outline=LINEA, width=4 * SS)
    for i in range(6):
        y = cy - h_ / 2 + h_ * (0.22 + 0.11 * i)
        d.line((cx - w_ * 0.38, y, cx + w_ * (0.38 if i % 3 else 0.2), y), fill=(150, 160, 190, 255), width=3 * SS)
    if voto:
        r = w_ * 0.2
        d.ellipse((cx + w_ * 0.18 - r, cy - h_ / 2 + h_ * 0.08 - r * 0.3, cx + w_ * 0.18 + r, cy - h_ / 2 + h_ * 0.08 + r * 1.7), outline=PENNA, width=4 * SS)
        tc(d, cx + w_ * 0.18, cy - h_ / 2 + h_ * 0.1, voto, int(46 * k * w_ / (200 * SS)), PENNA, bordo=False)


VOTI = ['5', '9½', '7', '6', '8', '6½', '9', '5½', '7½', '8½', '6', '7']


def compito_voti(p, t, w, h):
    """Apertura: lo stesso compito al centro e intorno i voti di tanti professori, dal 5 al 9 e mezzo."""
    im, d = tela(w, h, (246, 242, 236, 255)); W, H = w * SS, h * SS; k = scala(w)
    foglio(d, W * 0.5, H * 0.5, W * 0.34, H * 0.36, k=k)
    n = min(len(VOTI), int(t * 7))
    for i in range(n):
        a = math.radians(-90 + i * 30)
        x, y = W * 0.5 + math.cos(a) * W * 0.36, H * 0.5 + math.sin(a) * H * 0.33
        s = 1 + 0.2 * max(0, 1 - (t * 7 - i))
        tc(d, x, y - 40 * SS * k, VOTI[i], int(70 * k * s), PENNA)
    cont = min(73, int(t * 40))
    tc(d, W / 2, H * 0.05, f'{cont} professori', int(54 * k), SCURO)
    return fine(im, w, h)


def scala_voti(p, t, w, h):
    """I voti dati allo stesso compito messi in fila: da 5 a 9 e mezzo, un pallino per professore."""
    im, d = tela(w, h); W, H = w * SS, h * SS; k = scala(w)
    tc(d, W / 2, H * 0.05, 'stesso compito', int(56 * k))
    x0, x1, y = W * 0.1, W * 0.9, H * 0.66
    d.line((x0, y, x1, y), fill=LINEA, width=6 * SS)
    for v in range(4, 11):
        x = x0 + (x1 - x0) * (v - 4) / 6
        d.line((x, y - 14 * SS, x, y + 14 * SS), fill=LINEA, width=4 * SS)
        tc(d, x, y + 22 * SS, str(v), int(40 * k), SCURO, bordo=False)
    import random
    rnd = random.Random(7)
    tutti = [round(max(5.0, min(9.5, rnd.gauss(7.3, 1.1))) * 2) / 2 for _ in range(73)]
    tutti[5] = 9.5; tutti[20] = 9.5
    massimo = max(tutti.count(c) for c in set(tutti))
    passo = min(22 * SS, (y - H * 0.2) / (massimo + 1))
    n = min(73, int(t * 45))
    cont = {}
    for i in range(n):
        col = tutti[i]
        cont[col] = cont.get(col, 0) + 1
        x = x0 + (x1 - x0) * (col - 4) / 6
        yy = y - 20 * SS - cont[col] * passo
        rr = passo * 0.42
        d.ellipse((x - rr, yy - rr, x + rr, yy + rr), fill=PENNA if col in (5.0, 9.5) else BLU)
    if t > 1.6:
        tc(d, W / 2, H * 0.82, 'dal 5 al 9½', int(64 * k), PENNA)
    return fine(im, w, h)


def anno1912(p, t, w, h):
    """1912: lo stesso tema dato a più di cento insegnanti; pila di fogli con voti diversissimi."""
    im, d = tela(w, h, (244, 236, 220, 255)); W, H = w * SS, h * SS; k = scala(w)
    tc(d, W / 2, H * 0.04, '1912', int(130 * k), ARANCIO)
    for i in range(min(7, int(t * 4) + 1)):
        foglio(d, W * (0.3 + 0.07 * i), H * (0.52 + 0.025 * i), W * 0.3, H * 0.34, VOTI[i], k=k)
    tc(d, W / 2, H * 0.88, 'più di 100 insegnanti', int(44 * k), SCURO)
    return fine(im, w, h)


def stesso_prof(p, t, w, h):
    """Lo stesso professore ricorregge lo stesso compito settimane dopo e dà un voto diverso."""
    im, d = tela(w, h, (238, 244, 252, 255)); W, H = w * SS, h * SS; k = scala(w)
    omino(d, W * 0.5, H * 0.92, H * 0.22, BLU)
    foglio(d, W * 0.24, H * 0.36, W * 0.3, H * 0.32, '7', k=k)
    tc(d, W * 0.24, H * 0.06, 'oggi', int(44 * k), SCURO, bordo=False)
    if t > 0.9:
        foglio(d, W * 0.76, H * 0.36, W * 0.3, H * 0.32, '5½', k=k)
        tc(d, W * 0.76, H * 0.06, 'settimane dopo', int(40 * k), SCURO, bordo=False)
        tc(d, W * 0.5, H * 0.3, '≠', int(90 * k), PENNA, bordo=False)
    return fine(im, w, h)


def chi_lo_da(p, t, w, h):
    """Il voto dipende anche da chi lo da': VOTO = il tuo compito + chi corregge."""
    im, d = tela(w, h, (252, 246, 236, 255)); W, H = w * SS, h * SS; k = scala(w)
    tc(d, W / 2, H * 0.12, 'VOTO', int(110 * k), PENNA)
    tc(d, W / 2, H * 0.3, '=', int(80 * k), SCURO, bordo=False)
    foglio(d, W * 0.25, H * 0.56, W * 0.28, H * 0.28, k=k)
    tc(d, W * 0.25, H * 0.74, 'il tuo compito', int(34 * k), SCURO, bordo=False)
    tc(d, W * 0.5, H * 0.5, '+', int(80 * k), SCURO, bordo=False)
    if t > 0.6:
        omino(d, W * 0.75, H * 0.7, H * 0.15, VIOLA)
        tc(d, W * 0.75, H * 0.74, 'chi lo corregge', int(34 * k), VIOLA, bordo=False)
    return fine(im, w, h)


def costanza_qi(p, t, w, h):
    """Studio sui ragazzi di terza media: per prevedere i voti, la costanza pesa più del QI."""
    im, d = tela(w, h); W, H = w * SS, h * SS; k = scala(w)
    tc(d, W / 2, H * 0.04, 'cosa prevede i voti?', int(48 * k))
    base = H * 0.78
    for i, (nome, liv, col) in enumerate((('QI', 0.42, GRIGIO), ('costanza', 0.9, VERDE))):
        f = e(t * 1.2 - i * 0.4)
        x0 = W * (0.16 + 0.4 * i); x1 = x0 + W * 0.28
        y = base - H * 0.5 * liv * f
        d.rounded_rectangle((x0, y, x1, base), radius=16 * SS, fill=col, outline=LINEA, width=5 * SS)
        tc(d, (x0 + x1) / 2, base + 16 * SS, nome, int(46 * k), SCURO, bordo=False)
    d.line((W * 0.08, base, W * 0.92, base), fill=LINEA, width=6 * SS)
    tc(d, W / 2, H * 0.12, 'ragazzi di terza media', int(32 * k), GRIGIO, bordo=False)
    return fine(im, w, h)


def cosa_misura(p, t, w, h):
    """Il voto misura anche: organizzato, puntuale, costante. Non quanto vali (sbarrato)."""
    im, d = tela(w, h, (240, 246, 238, 255)); W, H = w * SS, h * SS; k = scala(w)
    tc(d, W / 2, H * 0.04, 'il voto misura anche...', int(46 * k))
    for i, v in enumerate(['organizzato', 'puntuale', 'costante']):
        if t * 2 > i:
            y = H * (0.2 + 0.15 * i)
            d.line((W * 0.14, y + 30 * SS, W * 0.18, y + 50 * SS, W * 0.25, y + 10 * SS), fill=VERDE, width=10 * SS)
            d.text((W * 0.3, y), v, font=font(int(56 * k)), fill=SCURO)
    if t > 1.6:
        y = H * 0.72
        d.text((W * 0.3, y), 'quanto vali', font=font(int(56 * k)), fill=GRIGIO)
        bb = d.textbbox((W * 0.3, y), 'quanto vali', font=font(int(56 * k)))
        ym = (bb[1] + bb[3]) / 2
        d.line((W * 0.27, ym, W * 0.86, ym), fill=PENNA, width=5 * SS)
    return fine(im, w, h)


def brutto_voto(p, t, w, h):
    """Un brutto voto non dice che sei stupido: dice su cosa lavorare (freccia verso la lista)."""
    im, d = tela(w, h, (252, 240, 236, 255)); W, H = w * SS, h * SS; k = scala(w)
    foglio(d, W * 0.32, H * 0.42, W * 0.42, H * 0.46, '4', k=k)
    if t > 0.9:
        d.line((W * 0.56, H * 0.42, W * 0.7, H * 0.42), fill=LINEA, width=10 * SS)
        d.polygon([(W * 0.74, H * 0.42), (W * 0.69, H * 0.38), (W * 0.69, H * 0.46)], fill=LINEA)
        d.rounded_rectangle((W * 0.75, H * 0.28, W * 0.97, H * 0.56), radius=16 * SS, fill=(255, 255, 255, 255), outline=LINEA, width=4 * SS)
        for i, v in enumerate(['ripassa', 'esercizi', 'chiedi']):
            tc(d, W * 0.86, H * (0.31 + 0.08 * i), v, int(30 * k), BLU, bordo=False)
    tc(d, W / 2, H * 0.8, 'non sei stupido', int(52 * k), PENNA)
    return fine(im, w, h)


def allena(p, t, w, h):
    """La costanza si allena: 20 minuti al giorno per due settimane, 14 caselle e il voto che sale."""
    im, d = tela(w, h, (244, 240, 252, 255)); W, H = w * SS, h * SS; k = scala(w)
    tc(d, W / 2, H * 0.04, '20 min al giorno', int(56 * k), VIOLA)
    n = min(14, int(t * 7))
    for i in range(14):
        c, r = i % 7, i // 7
        x = W * (0.1 + 0.115 * c); y = H * (0.2 + 0.13 * r)
        d.rounded_rectangle((x, y, x + W * 0.09, y + H * 0.1), radius=10 * SS, fill=VERDE if i < n else CARTA, outline=LINEA, width=3 * SS)
        if i < n:
            d.line((x + W * 0.02, y + H * 0.05, x + W * 0.04, y + H * 0.075, x + W * 0.07, y + H * 0.025), fill=CREMA, width=6 * SS)
    tc(d, W / 2, H * 0.46, '2 settimane', int(40 * k), SCURO, bordo=False)
    # voto che sale
    pts = [(W * (0.15 + 0.7 * i / 13), H * (0.86 - 0.22 * (i / 13) ** 1.3)) for i in range(max(1, n))]
    if len(pts) > 1: d.line(pts, fill=PENNA, width=10 * SS, joint='curve')
    if n >= 14:
        tc(d, W * 0.88, H * 0.58, '↑', int(70 * k), PENNA, bordo=False)
    return fine(im, w, h)


SCENE = {'compito_voti': compito_voti, 'scala_voti': scala_voti, 'anno1912': anno1912, 'stesso_prof': stesso_prof,
         'chi_lo_da': chi_lo_da, 'costanza_qi': costanza_qi, 'cosa_misura': cosa_misura, 'brutto_voto': brutto_voto, 'allena': allena}

if __name__ == '__main__':
    from PIL import Image
    tav = Image.new('RGB', (5 * 420, 2 * 500), 'white')
    for i, n in enumerate(SCENE):
        tav.paste(SCENE[n](1.0, 2.2, 420, 500), ((i % 5) * 420, (i // 5) * 500))
    tav.save(sys.argv[1])

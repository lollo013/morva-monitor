"""Illustrazioni originali per «Migliora dell'1% al giorno» e «Il tempo che ci rimane». f(p, t, w, h, **extra) -> RGB."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import ImageDraw
from scene_cielo import tela, fine, font, gradiente, LINEA, CREMA, ORO, ROSSO, ARANCIO, BLU, SS
from scene_inception import etichetta, VERDE
from scene_procrastinazione import testo_c, SCURO, CARTA, scala
from scene_scuola import GRIGIO, omino

VIOLA = (140, 84, 200, 255)
ROSA = (232, 110, 140, 255)


def tc(d, x, y, s, n, col=SCURO, bordo=True):
    testo_c(d, x, y, s, font(n), col, bordo)


def e(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3


# ============================================================ 1% al giorno
def curva37(p, t, w, h):
    """Apertura: 1,01^giorni sale fino a 37,8; 0,99^giorni scende fino a 0,03. Curve vere."""
    im, d = tela(w, h, (244, 248, 240, 255)); W, H = w * SS, h * SS; k = scala(w)
    x0, x1, y0, y1 = W * 0.1, W * 0.8, H * 0.12, H * 0.84
    d.line((x0, y1, x1, y1), fill=LINEA, width=6 * SS); d.line((x0, y0, x0, y1), fill=LINEA, width=6 * SS)
    f = min(1, t * 0.6)
    giorni = int(365 * f)
    for base, col in ((1.01, VERDE), (0.99, ROSSO)):
        pts = [(x0 + (x1 - x0) * g / 365, y1 - (y1 - y0) * (base ** g) / 38) for g in range(0, giorni + 1, 3)]
        if len(pts) > 1: d.line(pts, fill=col, width=12 * SS, joint='curve')
    d.line((x0, y1 - (y1 - y0) / 38, x1, y1 - (y1 - y0) / 38), fill=(150, 150, 160, 255), width=3 * SS)
    tc(d, (x0 + x1) / 2, y1 + 12 * SS, f'giorno {giorni}', int(36 * k), GRIGIO, bordo=False)
    if f >= 1:
        tc(d, W * 0.89, H * 0.1, '×37', int(76 * k), VERDE)
        tc(d, W * 0.89, H * 0.76, '3%', int(52 * k), ROSSO)
    return fine(im, w, h)


def moltiplica(p, t, w, h):
    """1,01 x 1,01 x ... per 365 volte: il contatore dei giorni e il risultato che cresce."""
    im, d = tela(w, h, (250, 246, 236, 255)); W, H = w * SS, h * SS; k = scala(w)
    g = min(365, int(t * 160) + 1)
    tc(d, W / 2, H * 0.08, '1,01 × 1,01 × 1,01 …', int(50 * k), SCURO)
    tc(d, W / 2, H * 0.26, f'{g} volte', int(56 * k), BLU)
    v = 1.01 ** g
    tc(d, W / 2, H * 0.44, f'= {v:.1f}'.replace('.', ','), int(130 * k), VERDE)
    # barra
    d.rounded_rectangle((W * 0.1, H * 0.78, W * 0.9, H * 0.84), radius=14 * SS, fill=(225, 220, 210, 255), outline=LINEA, width=4 * SS)
    d.rounded_rectangle((W * 0.1, H * 0.78, W * (0.1 + 0.8 * g / 365), H * 0.84), radius=14 * SS, fill=VERDE)
    tc(d, W / 2, H * 0.86, '1 anno', int(34 * k), GRIGIO, bordo=False)
    return fine(im, w, h)


def peggiora(p, t, w, h):
    """0,99 alla 365: la batteria che si scarica fino al 3%."""
    im, d = tela(w, h, (252, 240, 238, 255)); W, H = w * SS, h * SS; k = scala(w)
    tc(d, W / 2, H * 0.06, '0,99 ogni giorno', int(52 * k), ROSSO)
    g = min(365, int(t * 160))
    v = 0.99 ** g
    x0, y0, x1, y1 = W * 0.22, H * 0.26, W * 0.78, H * 0.78
    d.rounded_rectangle((x0, y0, x1, y1), radius=30 * SS, fill=(255, 255, 255, 255), outline=LINEA, width=8 * SS)
    d.rounded_rectangle(((x0 + x1) / 2 - W * 0.08, y0 - H * 0.04, (x0 + x1) / 2 + W * 0.08, y0), radius=8 * SS, fill=LINEA)
    hh = (y1 - y0 - 24 * SS) * v
    col = VERDE if v > 0.5 else (ARANCIO if v > 0.15 else ROSSO)
    d.rounded_rectangle((x0 + 12 * SS, y1 - 12 * SS - hh, x1 - 12 * SS, y1 - 12 * SS), radius=20 * SS, fill=col)
    tc(d, W / 2, H * 0.44, f'{round(v * 100)}%', int(110 * k), SCURO)
    tc(d, W / 2, H * 0.84, f'giorno {g}', int(40 * k), GRIGIO, bordo=False)
    return fine(im, w, h)


def piccolo(p, t, w, h):
    """L'1% e' pochissimo: 10 minuti, una pagina, un esercizio in piu'."""
    im, d = tela(w, h, (240, 246, 252, 255)); W, H = w * SS, h * SS; k = scala(w)
    tc(d, W / 2, H * 0.04, "l'1% è...", int(58 * k), BLU)
    voci = [('10 min', 'di studio'), ('1 pagina', 'di un libro'), ('+1', 'esercizio')]
    for i, (a, b) in enumerate(voci):
        if t * 2.2 > i:
            y = H * (0.2 + 0.24 * i)
            d.rounded_rectangle((W * 0.1, y, W * 0.9, y + H * 0.19), radius=24 * SS, fill=CARTA, outline=LINEA, width=5 * SS)
            tc(d, W * 0.32, y + H * 0.04, a, int(64 * k), VERDE, bordo=False)
            tc(d, W * 0.68, y + H * 0.06, b, int(38 * k), SCURO, bordo=False)
    return fine(im, w, h)


def plateau(p, t, w, h):
    """Cosa ti aspetti (linea dritta) e cosa succede (piatto per settimane, poi su): 'qui quasi tutti mollano'."""
    im, d = tela(w, h); W, H = w * SS, h * SS; k = scala(w)
    x0, x1, y0, y1 = W * 0.1, W * 0.9, H * 0.14, H * 0.8
    d.line((x0, y1, x1, y1), fill=LINEA, width=6 * SS); d.line((x0, y0, x0, y1), fill=LINEA, width=6 * SS)
    f = min(1, t * 0.7)
    att = [(x0 + (x1 - x0) * u, y1 - (y1 - y0) * u * 0.8) for u in [i / 40 * f for i in range(41)]]
    d.line(att, fill=(160, 160, 170, 255), width=6 * SS)
    real = [(x0 + (x1 - x0) * u, y1 - (y1 - y0) * 0.9 * (u ** 3.2)) for u in [i / 40 * f for i in range(41)]]
    d.line(real, fill=VERDE, width=12 * SS, joint='curve')
    tc(d, W * 0.3, H * 0.04, 'quello che ti aspetti', int(30 * k), GRIGIO, bordo=False)
    tc(d, W * 0.75, H * 0.88, 'quello che succede', int(30 * k), VERDE, bordo=False)
    if f > 0.5:
        cx, cy = x0 + (x1 - x0) * 0.45, y1 - (y1 - y0) * 0.9 * 0.45 ** 3.2
        d.ellipse((cx - 22 * SS, cy - 22 * SS, cx + 22 * SS, cy + 22 * SS), outline=ROSSO, width=7 * SS)
        tc(d, cx, cy - H * 0.2, 'qui quasi', int(38 * k), ROSSO)
        tc(d, cx, cy - H * 0.13, 'tutti mollano', int(38 * k), ROSSO)
    return fine(im, w, h)


def somma(p, t, w, h):
    """I piccoli progressi si sommano: mattoncini che si impilano in una torre che cresce sempre piu' in fretta."""
    im, d = tela(w, h, (252, 246, 236, 255)); W, H = w * SS, h * SS; k = scala(w)
    n = min(12, int(t * 6) + 1)
    y = H * 0.86; larg = W * 0.12
    for i in range(n):
        hgt = H * 0.015 * (1.25 ** i)
        if y - hgt < H * 0.15: break
        cols = [VERDE, BLU, ORO, ARANCIO, VIOLA, ROSA]
        d.rounded_rectangle((W / 2 - larg, y - hgt, W / 2 + larg, y), radius=6 * SS, fill=cols[i % 6], outline=LINEA, width=3 * SS)
        y -= hgt
    tc(d, W / 2, H * 0.04, 'si sommano', int(60 * k), VERDE)
    return fine(im, w, h)


def catena(p, t, w, h):
    """Segna una X sul calendario ogni giorno: non spezzare la catena."""
    im, d = tela(w, h, (255, 248, 238, 255)); W, H = w * SS, h * SS; k = scala(w)
    tc(d, W / 2, H * 0.04, 'non spezzare la catena', int(44 * k), ROSSO)
    n = min(28, int(t * 12))
    for i in range(28):
        c, r = i % 7, i // 7
        x = W * (0.08 + 0.125 * c); y = H * (0.2 + 0.15 * r)
        d.rounded_rectangle((x, y, x + W * 0.11, y + H * 0.13), radius=10 * SS, fill=CARTA, outline=LINEA, width=3 * SS)
        tc(d, x + W * 0.055, y + 4 * SS, str(i + 1), int(22 * k), GRIGIO, bordo=False)
        if i < n:
            d.line((x + W * 0.02, y + H * 0.045, x + W * 0.09, y + H * 0.115), fill=ROSSO, width=8 * SS)
            d.line((x + W * 0.09, y + H * 0.045, x + W * 0.02, y + H * 0.115), fill=ROSSO, width=8 * SS)
    return fine(im, w, h)


# ============================================================ Il tempo che ci rimane
def pensione(p, t, w, h):
    """Apertura: la linea della vita (dati ISTAT): in buona salute fino a 58 in media, pensione a 67."""
    im, d = tela(w, h, (240, 246, 252, 255)); W, H = w * SS, h * SS; k = scala(w)
    x0, x1, y = W * 0.08, W * 0.92, H * 0.5
    eta = lambda a: x0 + (x1 - x0) * a / 85
    f = e(t * 0.9)
    d.rounded_rectangle((x0, y - 30 * SS, eta(58 * f), y + 30 * SS), radius=16 * SS, fill=VERDE)
    if f >= 1:
        d.rounded_rectangle((eta(58), y - 30 * SS, eta(83), y + 30 * SS), radius=16 * SS, fill=(200, 196, 190, 255))
    d.rounded_rectangle((x0, y - 30 * SS, x1, y + 30 * SS), radius=16 * SS, outline=LINEA, width=5 * SS)
    for a in (0, 20, 40, 60, 80):
        tc(d, eta(a), y + 44 * SS, str(a), int(30 * k), GRIGIO, bordo=False)
    tc(d, eta(29), y - 90 * SS * k - 30 * SS, 'in buona salute', int(34 * k), VERDE, bordo=False)
    if t > 1.0:
        tc(d, eta(58), y - H * 0.24, '58', int(80 * k), VERDE)
        d.line((eta(58), y - H * 0.13, eta(58), y - 30 * SS), fill=VERDE, width=6 * SS)
    if t > 1.6:
        d.line((eta(67), y + 30 * SS, eta(67), y + H * 0.16), fill=ROSSO, width=6 * SS)
        tc(d, eta(67), y + H * 0.17, 'pensione 67', int(48 * k), ROSSO)
    return fine(im, w, h)


def esame(p, t, w, h):
    """Una settimana di studio per un esame di 20 minuti."""
    im, d = tela(w, h, (250, 246, 236, 255)); W, H = w * SS, h * SS; k = scala(w)
    giorni = ['L', 'M', 'M', 'G', 'V', 'S', 'D']
    n = min(7, int(t * 4) + 1)
    for i in range(7):
        x = W * (0.08 + 0.12 * i)
        d.rounded_rectangle((x, H * 0.18, x + W * 0.1, H * 0.6), radius=10 * SS, fill=BLU if i < n else CARTA, outline=LINEA, width=3 * SS)
        tc(d, x + W * 0.05, H * 0.62, giorni[i], int(34 * k), SCURO, bordo=False)
    tc(d, W / 2, H * 0.05, '1 settimana di studio', int(46 * k), BLU)
    if t > 1.6:
        d.rounded_rectangle((W * 0.3, H * 0.74, W * 0.7, H * 0.9), radius=20 * SS, fill=ROSSO, outline=LINEA, width=4 * SS)
        tc(d, W / 2, H * 0.77, 'esame: 20 min', int(40 * k), CREMA, bordo=False)
    return fine(im, w, h)


def weekend(p, t, w, h):
    """Cinque giorni di lavoro per due di weekend."""
    im, d = tela(w, h, (244, 244, 248, 255)); W, H = w * SS, h * SS; k = scala(w)
    nomi = ['lun', 'mar', 'mer', 'gio', 'ven', 'sab', 'dom']
    for i in range(7):
        y = H * (0.08 + 0.12 * i)
        wk = i >= 5
        a = e(t * 2.5 - i * 0.25)
        d.rounded_rectangle((W * 0.06, y, W * (0.06 + 0.58 * a), y + H * 0.1), radius=14 * SS, fill=(VERDE if wk else (150, 150, 160, 255)), outline=LINEA, width=3 * SS)
        tc(d, W * 0.16, y + H * 0.022, nomi[i], int(36 * k), CREMA, bordo=False)
    tc(d, W * 0.82, H * 0.24, '5', int(130 * k), GRIGIO, bordo=False)
    tc(d, W * 0.82, H * 0.66, '2', int(130 * k), VERDE, bordo=False)
    return fine(im, w, h)


def ore_lavoro(p, t, w, h):
    """Al lavoro piu' di 70.000 ore in una vita: piu' di 8 anni giorno e notte. Clessidra e contatore."""
    im, d = tela(w, h, (250, 244, 232, 255)); W, H = w * SS, h * SS; k = scala(w)
    cx, cy = W * 0.3, H * 0.5
    a, b = W * 0.17, H * 0.32
    d.polygon([(cx - a, cy - b), (cx + a, cy - b), (cx, cy), (cx + a, cy + b), (cx - a, cy + b), (cx, cy)], outline=LINEA, width=6 * SS)
    f = min(1, t * 0.5)
    sab = (1 - f)
    d.polygon([(cx - a * sab, cy - b * sab), (cx + a * sab, cy - b * sab), (cx, cy)], fill=ORO)
    d.polygon([(cx - a * f, cy + b), (cx + a * f, cy + b), (cx, cy + b * (1 - f))], fill=ORO)
    d.line((cx, cy, cx, cy + b), fill=ORO, width=4 * SS)
    ore = int(72000 * f)
    tc(d, W * 0.72, H * 0.24, f'{ore:,}'.replace(',', '.'), int(64 * k), SCURO)
    tc(d, W * 0.72, H * 0.36, 'ore di lavoro', int(34 * k), GRIGIO, bordo=False)
    if f >= 1:
        tc(d, W * 0.72, H * 0.54, '= 8 anni', int(62 * k), ROSSO)
        tc(d, W * 0.72, H * 0.66, 'giorno e notte', int(32 * k), ROSSO, bordo=False)
    return fine(im, w, h)


def torta_vita(p, t, w, h):
    """La vita in fette: sonno quasi un terzo, lavoro, scuola, telefono... e la fetta che resta davvero tua."""
    im, d = tela(w, h); W, H = w * SS, h * SS; k = scala(w)
    cx, cy, r = W * 0.5, H * 0.46, min(W, H) * 0.34
    fette = [('sonno', 0.33, (90, 110, 170, 255)), ('lavoro/scuola', 0.2, (150, 150, 160, 255)), ('telefono', 0.12, VIOLA),
             ('doveri', 0.22, (200, 160, 100, 255)), ('tuo', 0.13, VERDE)]
    a = -90; n = min(len(fette), int(t * 2.4) + 1)
    for i, (nome, q, col) in enumerate(fette[:n]):
        b = a + 360 * q
        d.pieslice((cx - r, cy - r, cx + r, cy + r), a, b, fill=col, outline=LINEA, width=4 * SS)
        m = math.radians((a + b) / 2)
        tc(d, cx + math.cos(m) * r * 0.62, cy + math.sin(m) * r * 0.62 - 18 * SS, nome, int(28 * k), CREMA, bordo=False)
        a = b
    tc(d, W / 2, H * 0.86, 'il tempo davvero nostro', int(40 * k), VERDE)
    return fine(im, w, h)


def telefono45(p, t, w, h):
    """3 ore al giorno di telefono = 45 giorni all'anno: i giorni del calendario che si colorano."""
    im, d = tela(w, h, (246, 240, 252, 255)); W, H = w * SS, h * SS; k = scala(w)
    tc(d, W / 2, H * 0.03, '3 ore al giorno', int(52 * k), VIOLA)
    n = min(45, int(t * 26))
    for i in range(60):
        c, r = i % 10, i // 10
        x = W * (0.07 + 0.088 * c); y = H * (0.16 + 0.1 * r)
        d.rounded_rectangle((x, y, x + W * 0.075, y + H * 0.08), radius=6 * SS, fill=VIOLA if i < n else CARTA, outline=LINEA, width=2 * SS)
    tc(d, W / 2, H * 0.8, f'= {n} giorni', int(70 * k), VIOLA)
    tc(d, W / 2, H * 0.91, "all'anno", int(36 * k), SCURO, bordo=False)
    return fine(im, w, h)


def ruota(p, t, w, h):
    """Occupati a prepararci per vivere: l'omino che corre nella ruota del criceto."""
    im, d = tela(w, h, (252, 246, 236, 255)); W, H = w * SS, h * SS; k = scala(w)
    cx, cy, r = W * 0.5, H * 0.48, min(W, H) * 0.32
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=LINEA, width=10 * SS)
    for i in range(12):
        a = math.radians(i * 30 + t * 220)
        d.line((cx + math.cos(a) * r * 0.85, cy + math.sin(a) * r * 0.85, cx + math.cos(a) * r, cy + math.sin(a) * r), fill=LINEA, width=6 * SS)
    d.line((cx, cy, cx - r * 0.6, cy + r * 1.3), fill=LINEA, width=8 * SS)
    d.line((cx, cy, cx + r * 0.6, cy + r * 1.3), fill=LINEA, width=8 * SS)
    sb = 8 * SS * math.sin(t * 14)
    omino(d, cx, cy + r * 0.92 + sb, r * 0.42, ARANCIO)
    tc(d, W / 2, H * 0.03, 'prepararsi a vivere...', int(46 * k), SCURO)
    return fine(im, w, h)


def ora_tua(p, t, w, h):
    """Un'ora al giorno solo tua: l'orologio con una fetta verde; 'oggi'."""
    im, d = tela(w, h, (240, 248, 240, 255)); W, H = w * SS, h * SS; k = scala(w)
    cx, cy, r = W * 0.5, H * 0.46, min(W, H) * 0.34
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=CARTA, outline=LINEA, width=8 * SS)
    f = e(t * 1.2)
    d.pieslice((cx - r * 0.92, cy - r * 0.92, cx + r * 0.92, cy + r * 0.92), -90, -90 + 30 * f, fill=VERDE)
    for i in range(12):
        a = math.radians(i * 30 - 90)
        d.line((cx + math.cos(a) * r * 0.82, cy + math.sin(a) * r * 0.82, cx + math.cos(a) * r * 0.95, cy + math.sin(a) * r * 0.95), fill=LINEA, width=5 * SS)
    tc(d, W / 2, H * 0.04, "un'ora solo tua", int(54 * k), VERDE)
    if t > 1.0:
        d.rounded_rectangle((W * 0.3, H * 0.82, W * 0.7, H * 0.94), radius=24 * SS, fill=ROSSO, outline=LINEA, width=4 * SS)
        tc(d, W / 2, H * 0.84, 'OGGI', int(52 * k), CREMA, bordo=False)
    return fine(im, w, h)


SCENE = {'curva37': curva37, 'moltiplica': moltiplica, 'peggiora': peggiora, 'piccolo': piccolo, 'plateau': plateau,
         'somma': somma, 'catena': catena, 'pensione': pensione, 'esame': esame, 'weekend': weekend, 'ore_lavoro': ore_lavoro,
         'torta_vita': torta_vita, 'telefono45': telefono45, 'ruota': ruota, 'ora_tua': ora_tua}

if __name__ == '__main__':
    from PIL import Image
    nomi = list(SCENE)
    tav = Image.new('RGB', (5 * 420, 3 * 500), 'white')
    for i, n in enumerate(nomi):
        tav.paste(SCENE[n](1.0, 3.0, 420, 500), ((i % 5) * 420, (i // 5) * 500))
    tav.save(sys.argv[1])

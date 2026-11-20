"""Illustrazioni originali per «Perché non riusciamo a smettere di scrollare». f(p, t, w, h, **extra) -> RGB."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import ImageDraw
from scene_cielo import tela, fine, font, gradiente, LINEA, CREMA, ORO, ROSSO, ARANCIO, BLU, SS
from scene_inception import etichetta, VERDE, NOTTE, NOTTE2
from scene_procrastinazione import testo_c, SCURO, CARTA, scala
from scene_scuola import GRIGIO

VIOLA = (140, 84, 200, 255)
ROSA = (232, 110, 140, 255)
COLORI = [ROSSO, ORO, VERDE, BLU, VIOLA, ARANCIO, ROSA]


def tc(d, x, y, s, n, col=SCURO, bordo=True):
    testo_c(d, x, y, s, font(n), col, bordo)


def simbolo(d, cx, cy, r, tipo):
    """Cuore, stella o 7 disegnati (niente glifi del font)."""
    if tipo == 'cuore':
        d.ellipse((cx - r, cy - r * 0.8, cx, cy + r * 0.2), fill=ROSSO)
        d.ellipse((cx, cy - r * 0.8, cx + r, cy + r * 0.2), fill=ROSSO)
        d.polygon([(cx - r * 0.97, cy - r * 0.2), (cx + r * 0.97, cy - r * 0.2), (cx, cy + r)], fill=ROSSO)
    elif tipo == 'stella':
        pts = [(cx + (r if i % 2 == 0 else r * 0.45) * math.cos(math.radians(-90 + 36 * i)),
                cy + (r if i % 2 == 0 else r * 0.45) * math.sin(math.radians(-90 + 36 * i))) for i in range(10)]
        d.polygon(pts, fill=ORO, outline=LINEA)
    else:
        f = font(int(r * 1.6 / SS))
        tw = d.textlength('7', font=f)
        d.text((cx - tw / 2, cy - r * 0.95), '7', font=f, fill=VIOLA)


def e(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3


def telefono(d, cx, cy, w_, h_, schermo=(30, 30, 40, 255)):
    d.rounded_rectangle((cx - w_ / 2, cy - h_ / 2, cx + w_ / 2, cy + h_ / 2), radius=w_ * 0.14, fill=(40, 40, 48, 255), outline=LINEA, width=6 * SS)
    d.rounded_rectangle((cx - w_ / 2 + w_ * 0.06, cy - h_ / 2 + w_ * 0.12, cx + w_ / 2 - w_ * 0.06, cy + h_ / 2 - w_ * 0.12), radius=w_ * 0.06, fill=schermo)
    return (cx - w_ / 2 + w_ * 0.06, cy - h_ / 2 + w_ * 0.12, cx + w_ / 2 - w_ * 0.06, cy + h_ / 2 - w_ * 0.12)


def post(d, x0, y0, x1, y1, col, grigio=False):
    if y1 - y0 < 50 * SS: return
    g = lambda c: (int(sum(c[:3]) / 3),) * 3 + (255,) if grigio else c
    d.rounded_rectangle((x0, y0, x1, y1), radius=12 * SS, fill=g(col), outline=LINEA, width=3 * SS)
    d.ellipse((x0 + 12 * SS, y1 - 40 * SS, x0 + 36 * SS, y1 - 16 * SS), fill=g(ROSSO))


def slot_telefono(p, t, w, h):
    """Apertura: lo schermo del telefono e' una slot machine; tre rulli che girano e la leva."""
    im, d = tela(w, h, (34, 24, 52, 255)); W, H = w * SS, h * SS; k = scala(w)
    gradiente(im, (60, 30, 90), (20, 16, 40)); d = ImageDraw.Draw(im, 'RGBA')
    for i in range(16):
        a = (math.sin(t * 6 + i) + 1) / 2
        x = W * (0.05 + 0.9 * ((i * 0.37) % 1)); y = H * (0.04 + 0.9 * ((i * 0.61) % 1))
        d.ellipse((x - 6 * SS, y - 6 * SS, x + 6 * SS, y + 6 * SS), fill=(255, 220, 120, int(80 + 170 * a)))
    sx0, sy0, sx1, sy1 = telefono(d, W * 0.62, H * 0.56, W * 0.5, H * 0.66)
    rw = (sx1 - sx0) / 3
    for r in range(3):
        stop = 0.8 + r * 0.5
        giro = t * 9 if t < stop else float(round(stop * 9))
        for j in range(-1, 2):
            yy = (sy0 + sy1) / 2 + (j - (giro % 1)) * rw * 1.1
            x0 = sx0 + r * rw
            d.rounded_rectangle((x0 + 8 * SS, yy - rw * 0.45, x0 + rw - 8 * SS, yy + rw * 0.45), radius=14 * SS, fill=CARTA, outline=LINEA, width=3 * SS)
            sim = ['cuore', 'stella', '7'][(int(giro) + j + r) % 3] if t < stop else 'cuore'
            simbolo(d, x0 + rw / 2, yy, rw * 0.28, sim)
    d.rectangle((sx0, sy0, sx1, (sy0 + sy1) / 2 - rw * 0.62), fill=(30, 30, 40, 255))
    d.rectangle((sx0, (sy0 + sy1) / 2 + rw * 0.62, sx1, sy1), fill=(30, 30, 40, 255))
    # leva
    a = math.radians(-30 + 60 * e(min(1, t * 2)) if t < 0.6 else -30)
    lx, ly = W * 0.92, H * 0.5
    d.line((lx, ly, lx + math.sin(a) * H * 0.0, ly - math.cos(a) * H * 0.18), fill=(200, 200, 210, 255), width=12 * SS)
    d.ellipse((lx - 24 * SS, ly - H * 0.18 - 24 * SS, lx + 24 * SS, ly - H * 0.18 + 24 * SS), fill=ROSSO, outline=LINEA, width=4 * SS)
    return fine(im, w, h)


def scroll_ora(p, t, w, h):
    """Un video, poi un altro: il pollice che scorre e l'orologio che corre fino a un'ora."""
    im, d = tela(w, h, (240, 244, 252, 255)); W, H = w * SS, h * SS; k = scala(w)
    sx0, sy0, sx1, sy1 = telefono(d, W * 0.36, H * 0.55, W * 0.5, H * 0.74, schermo=(250, 250, 255, 255))
    off = (t * 1.6) % 1
    for i in range(-1, 4):
        y0 = sy0 + (i - off) * (sy1 - sy0) * 0.42
        post(d, sx0 + 10 * SS, max(sy0, y0), sx1 - 10 * SS, min(sy1, y0 + (sy1 - sy0) * 0.38), COLORI[(i + int(t * 1.6)) % 7])
    d.rectangle((0, 0, W, sy0), fill=(240, 244, 252, 255))
    d.rectangle((0, sy1, W, H), fill=(240, 244, 252, 255))
    cx_, cy_, w_, h_ = W * 0.36, H * 0.55, W * 0.5, H * 0.74
    d.rounded_rectangle((cx_ - w_ / 2, cy_ - h_ / 2, cx_ + w_ / 2, cy_ - h_ / 2 + w_ * 0.12), radius=w_ * 0.14, fill=(40, 40, 48, 255))
    d.rounded_rectangle((cx_ - w_ / 2, cy_ + h_ / 2 - w_ * 0.12, cx_ + w_ / 2, cy_ + h_ / 2), radius=w_ * 0.14, fill=(40, 40, 48, 255))
    d.rounded_rectangle((cx_ - w_ / 2, cy_ - h_ / 2, cx_ + w_ / 2, cy_ + h_ / 2), radius=w_ * 0.14, outline=LINEA, width=6 * SS)
    # pollice
    py = H * (0.7 - 0.2 * ((t * 1.6) % 1))
    d.ellipse((W * 0.42, py - H * 0.06, W * 0.58, py + H * 0.06), fill=(252, 200, 150, 255), outline=LINEA, width=5 * SS)
    # orologio
    cx, cy, r = W * 0.8, H * 0.3, W * 0.14
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=CARTA, outline=LINEA, width=6 * SS)
    for ang, lun, lw in ((t * 40, 0.5, 9), (t * 480, 0.8, 6)):
        a = math.radians(ang - 90)
        d.line((cx, cy, cx + math.cos(a) * r * lun, cy + math.sin(a) * r * lun), fill=LINEA, width=lw * SS)
    minuti = min(60, int(t * 22))
    tc(d, cx, cy + r + 12 * SS, f'{minuti} min', int(48 * k), ROSSO if minuti >= 60 else SCURO, bordo=False)
    etichetta(d, W, H, 'ancora uno...', y=0.03, col=SCURO, dim=int(56 * k))
    return fine(im, w, h)


def progettato(p, t, w, h):
    """Non e' colpa tua: e' progettato. Il telefono su un foglio di progetto con le quote."""
    im, d = tela(w, h, (40, 84, 150, 255)); W, H = w * SS, h * SS; k = scala(w)
    for i in range(0, 30):
        d.line((W * i / 30, 0, W * i / 30, H), fill=(255, 255, 255, 30), width=2 * SS)
        d.line((0, H * i / 30, W, H * i / 30), fill=(255, 255, 255, 30), width=2 * SS)
    cx, cy, ww, hh = W * 0.5, H * 0.5, W * 0.4, H * 0.56
    a = e(t * 1.2)
    d.rounded_rectangle((cx - ww / 2, cy - hh / 2, cx + ww / 2, cy + hh / 2), radius=40 * SS, outline=(255, 255, 255, int(255 * a)), width=6 * SS)
    for et, (x, y) in (('feed infinito', (0.5, 0.36)), ('notifiche', (0.5, 0.5)), ('premi a caso', (0.5, 0.64))):
        if t * 1.6 > (x + y) - 0.8:
            tc(d, W * x, H * y, et, int(40 * k), CREMA, bordo=False)
    etichetta(d, W, H, 'PROGETTATO', y=0.04, col=CREMA, dim=int(74 * k))
    etichetta(d, W, H, 'non è colpa tua', y=0.86, col=ORO, dim=int(50 * k))
    return fine(im, w, h)


def premio(p, t, w, h):
    """Ricompensa fissa contro ricompensa variabile: a sinistra premio sempre, a destra a caso; la 'voglia' sale a destra."""
    im, d = tela(w, h); W, H = w * SS, h * SS; k = scala(w)
    d.line((W / 2, H * 0.14, W / 2, H * 0.78), fill=LINEA, width=5 * SS)
    tc(d, W * 0.25, H * 0.04, 'premio sempre', int(36 * k), GRIGIO, bordo=False)
    tc(d, W * 0.75, H * 0.04, 'premio a caso', int(36 * k), ROSSO, bordo=False)
    n = int(t * 3)
    casuali = [1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1]
    for i in range(min(n, 12)):
        y = H * (0.16 + 0.05 * i)
        for xx in (0.18, 0.68):
            d.polygon([(W * xx - 10 * SS, y), (W * xx - 10 * SS, y + 24 * SS), (W * xx + 12 * SS, y + 12 * SS)], fill=GRIGIO)
        simbolo(d, W * 0.32, y + 12 * SS, 16 * SS, 'stella')
        if casuali[i]: simbolo(d, W * 0.82, y + 12 * SS, 16 * SS, 'stella')
        else: d.ellipse((W * 0.82 - 4 * SS, y + 8 * SS, W * 0.82 + 4 * SS, y + 16 * SS), fill=GRIGIO)
    # barre "voglia di cercare"
    for x, liv, col in ((0.25, 0.3, GRIGIO), (0.75, 0.9, ROSSO)):
        v = liv * e(t * 0.8)
        d.rounded_rectangle((W * (x - 0.15), H * 0.82, W * (x + 0.15), H * 0.88), radius=10 * SS, fill=(225, 220, 210, 255), outline=LINEA, width=3 * SS)
        d.rounded_rectangle((W * (x - 0.15), H * 0.82, W * (x - 0.15 + 0.3 * v), H * 0.88), radius=10 * SS, fill=col)
    tc(d, W / 2, H * 0.9, 'voglia di continuare', int(30 * k), SCURO, bordo=False)
    return fine(im, w, h)


def slot_feed(p, t, w, h):
    """Slot machine e feed affiancati: lo stesso gesto, tirare la leva = scorrere col dito."""
    im, d = tela(w, h, (250, 244, 232, 255)); W, H = w * SS, h * SS; k = scala(w)
    # slot
    d.rounded_rectangle((W * 0.05, H * 0.22, W * 0.45, H * 0.8), radius=30 * SS, fill=ROSSO, outline=LINEA, width=6 * SS)
    for r in range(3):
        x0 = W * (0.09 + 0.11 * r)
        d.rounded_rectangle((x0, H * 0.36, x0 + W * 0.09, H * 0.52), radius=8 * SS, fill=CARTA, outline=LINEA, width=3 * SS)
        simbolo(d, x0 + W * 0.045, H * 0.44, W * 0.035, ['7', 'stella', 'cuore'][(int(t * 8) + r) % 3])
    d.line((W * 0.47, H * 0.45, W * 0.47, H * (0.25 + 0.1 * abs(math.sin(t * 3)))), fill=(200, 200, 210, 255), width=10 * SS)
    # telefono
    sx0, sy0, sx1, sy1 = telefono(d, W * 0.76, H * 0.51, W * 0.36, H * 0.6, schermo=(250, 250, 255, 255))
    off = (t * 1.4) % 1
    for i in range(3):
        y0 = sy0 + (i - off) * (sy1 - sy0) * 0.4 + 6 * SS
        if y0 > sy0 - 1 and y0 + (sy1 - sy0) * 0.34 < sy1:
            post(d, sx0 + 8 * SS, y0, sx1 - 8 * SS, y0 + (sy1 - sy0) * 0.34, COLORI[(i + int(t * 1.4)) % 7])
    tc(d, W / 2, H * 0.84, '=', int(80 * k), SCURO, bordo=False)
    etichetta(d, W, H, 'stesso meccanismo', y=0.05, col=SCURO, dim=int(52 * k))
    return fine(im, w, h)


def dopamina(p, t, w, h):
    """La dopamina e' l'attesa: un indicatore che sale quando la carta e' coperta (?), non quando si scopre."""
    im, d = tela(w, h, (246, 240, 252, 255)); W, H = w * SS, h * SS; k = scala(w)
    etichetta(d, W, H, 'dopamina = attesa', y=0.04, col=VIOLA, dim=int(54 * k))
    fase = (t % 2.4) / 2.4
    coperta = fase < 0.7
    cx, cy = W * 0.36, H * 0.5
    d.rounded_rectangle((cx - W * 0.2, cy - H * 0.26, cx + W * 0.2, cy + H * 0.26), radius=24 * SS, fill=VIOLA if coperta else CARTA, outline=LINEA, width=6 * SS)
    if coperta: tc(d, cx, cy - H * 0.1, '?', int(170 * k), CREMA, bordo=False)
    else: simbolo(d, cx, cy, W * 0.12, 'stella')
    # indicatore
    x0, x1, y0, y1 = W * 0.7, W * 0.84, H * 0.2, H * 0.82
    liv = (fase / 0.7) if coperta else max(0.2, 1 - (fase - 0.7) / 0.3)
    d.rounded_rectangle((x0, y0, x1, y1), radius=20 * SS, fill=(226, 220, 236, 255), outline=LINEA, width=5 * SS)
    d.rounded_rectangle((x0, y1 - (y1 - y0) * liv, x1, y1), radius=20 * SS, fill=ROSA)
    tc(d, (x0 + x1) / 2, y1 + 14 * SS, 'attesa', int(34 * k), SCURO, bordo=False)
    etichetta(d, W, H, 'forse il prossimo...', y=0.88, col=SCURO, dim=int(44 * k))
    return fine(im, w, h)


def infinito(p, t, w, h):
    """Lo scroll infinito: la pagina non finisce mai, nessun segnale di stop (cartello STOP sbarrato)."""
    im, d = tela(w, h, (236, 240, 248, 255)); W, H = w * SS, h * SS; k = scala(w)
    off = (t * 0.9) % 1
    for i in range(-1, 7):
        y0 = H * (0.08 + 0.15 * (i - off))
        post(d, W * 0.12, y0, W * 0.56, y0 + H * 0.12, COLORI[(i + int(t * 0.9)) % 7])
    tc(d, W * 0.78, H * 0.72, 'senza fine', int(44 * k), BLU)
    # cartello stop sbarrato
    cx, cy, r = W * 0.78, H * 0.42, W * 0.13
    pts = [(cx + r * math.cos(math.radians(22.5 + 45 * i)), cy + r * math.sin(math.radians(22.5 + 45 * i))) for i in range(8)]
    d.polygon(pts, fill=ROSSO, outline=LINEA)
    tc(d, cx, cy - 28 * SS * k, 'STOP', int(44 * k), CREMA, bordo=False)
    if t > 0.6:
        d.line((cx - r * 1.2, cy - r * 1.2, cx + r * 1.2, cy + r * 1.2), fill=LINEA, width=14 * SS)
    tc(d, cx, cy + r + 20 * SS, 'nessuna fine', int(36 * k), SCURO, bordo=False)
    tc(d, cx, cy + r + 70 * SS * k, 'pagina', int(36 * k), SCURO, bordo=False)
    return fine(im, w, h)


def inventore(p, t, w, h):
    """2006: l'invenzione dello scroll infinito; oggi l'inventore dice di essersene pentito (fumetto, nessun ritratto)."""
    im, d = tela(w, h, (252, 246, 236, 255)); W, H = w * SS, h * SS; k = scala(w)
    tc(d, W / 2, H * 0.05, '2006', int(130 * k), BLU)
    # lampadina
    cx, cy = W * 0.3, H * 0.5
    d.ellipse((cx - W * 0.13, cy - H * 0.15, cx + W * 0.13, cy + H * 0.08), fill=(255, 230, 120, 255), outline=LINEA, width=6 * SS)
    d.rectangle((cx - W * 0.06, cy + H * 0.08, cx + W * 0.06, cy + H * 0.15), fill=GRIGIO, outline=LINEA, width=4 * SS)
    if t > 0.8:
        d.rounded_rectangle((W * 0.5, H * 0.34, W * 0.96, H * 0.66), radius=28 * SS, fill=(255, 255, 255, 255), outline=LINEA, width=5 * SS)
        d.polygon([(W * 0.52, H * 0.6), (W * 0.46, H * 0.7), (W * 0.6, H * 0.64)], fill=(255, 255, 255, 255))
        tc(d, W * 0.73, H * 0.4, '«me ne', int(40 * k), SCURO, bordo=False)
        tc(d, W * 0.73, H * 0.5, 'sono pentito»', int(40 * k), ROSSO, bordo=False)
    etichetta(d, W, H, "l'inventore dello scroll infinito", y=0.84, col=SCURO, dim=int(36 * k))
    return fine(im, w, h)


def bianco_nero(p, t, w, h):
    """Schermo in bianco e nero: lo stesso feed perde i colori; -20/50 minuti al giorno."""
    im, d = tela(w, h); W, H = w * SS, h * SS; k = scala(w)
    a = e((t - 0.6) * 1.2)
    sx0, sy0, sx1, sy1 = telefono(d, W * 0.36, H * 0.52, W * 0.5, H * 0.74, schermo=(250, 250, 255, 255))
    for i in range(3):
        y0 = sy0 + 10 * SS + i * (sy1 - sy0) * 0.33
        post(d, sx0 + 10 * SS, y0, sx1 - 10 * SS, y0 + (sy1 - sy0) * 0.3, COLORI[i * 2], grigio=a > 0.5)
    tc(d, W * 0.8, H * 0.3, '−20', int(80 * k), VERDE)
    tc(d, W * 0.8, H * 0.42, '/ 50', int(60 * k), VERDE)
    tc(d, W * 0.8, H * 0.54, 'min', int(46 * k), SCURO, bordo=False)
    tc(d, W * 0.8, H * 0.62, 'al giorno', int(36 * k), GRIGIO, bordo=False)
    etichetta(d, W, H, 'bianco e nero', y=0.03, col=SCURO, dim=int(58 * k))
    return fine(im, w, h)


def notifiche(p, t, w, h):
    """Togli le notifiche: la campanella che vibra, poi sbarrata."""
    im, d = tela(w, h, (255, 244, 238, 255)); W, H = w * SS, h * SS; k = scala(w)
    cx, cy = W * 0.5, H * 0.46
    sh = 10 * SS * math.sin(t * 30) if t < 0.9 else 0
    s = W * 0.22
    d.pieslice((cx - s + sh, cy - s, cx + s + sh, cy + s), 180, 360, fill=ORO, outline=LINEA, width=6 * SS)
    d.rectangle((cx - s + sh, cy, cx + s + sh, cy + s * 0.45), fill=ORO, outline=LINEA, width=6 * SS)
    d.rectangle((cx - s * 1.2 + sh, cy + s * 0.45, cx + s * 1.2 + sh, cy + s * 0.6), fill=ORO, outline=LINEA, width=6 * SS)
    d.ellipse((cx - s * 0.2 + sh, cy + s * 0.6, cx + s * 0.2 + sh, cy + s * 0.9), fill=ORO, outline=LINEA, width=5 * SS)
    for i, n in enumerate(['12', '99+', '7']):
        if t < 0.9:
            bx, by = cx + s * (0.6 + 0.3 * i), cy - s * (0.9 - 0.4 * i)
            d.ellipse((bx - 40 * SS, by - 40 * SS, bx + 40 * SS, by + 40 * SS), fill=ROSSO, outline=LINEA, width=3 * SS)
            tc(d, bx, by - 20 * SS, n, int(30 * k), CREMA, bordo=False)
    if t >= 0.9:
        r = s * 1.6
        d.line((cx - r, cy - r, cx + r, cy + r), fill=ROSSO, width=18 * SS)
    etichetta(d, W, H, 'togli le notifiche', y=0.86, col=SCURO, dim=int(50 * k))
    return fine(im, w, h)


SCENE = {'slot_telefono': slot_telefono, 'scroll_ora': scroll_ora, 'progettato': progettato, 'premio': premio,
         'slot_feed': slot_feed, 'dopamina': dopamina, 'infinito': infinito, 'inventore': inventore,
         'bianco_nero': bianco_nero, 'notifiche': notifiche}

if __name__ == '__main__':
    from PIL import Image
    tav = Image.new('RGB', (5 * 420, 2 * 500), 'white')
    for i, n in enumerate(SCENE):
        tav.paste(SCENE[n](1.0, 2.0, 420, 500), ((i % 5) * 420, (i // 5) * 500))
    tav.save(sys.argv[1])

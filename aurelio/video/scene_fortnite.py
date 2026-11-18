"""Illustrazioni originali per «Il token pirata di Fortnite».

Nessun logo, personaggio, arma o immagine del gioco: solo simboli generici (moneta da
pirata, forzieri, negozio, slot machine, calendario, orologio, telefono) nello stile del
Professore. f(p, t, w, h, **extra) -> immagine RGB.
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from scene_cielo import tela, fine, font, mix, gradiente, LINEA, CREMA, ORO, ROSSO, ARANCIO, BLU, SS
from scene_inception import etichetta, NOTTE, NOTTE2, ACCIAIO, SAIO, VERDE, VIOLA

ORO2 = (214, 150, 40, 255)
LEGNO = (150, 98, 58, 255)
LEGNO2 = (112, 70, 40, 255)
MARE = (40, 110, 170)
MARE2 = (90, 170, 210)


def moneta(d, cx, cy, r, giro=0.0):
    """Moneta d'oro con teschio e ossa incrociate; giro = fase della rotazione (schiaccia in larghezza)."""
    k = max(0.12, abs(math.cos(giro)))
    rx = r * k
    d.ellipse((cx - rx - 10 * SS, cy - r + 12 * SS, cx + rx + 10 * SS, cy + r + 12 * SS), fill=ORO2, outline=LINEA, width=7 * SS)
    d.ellipse((cx - rx, cy - r, cx + rx, cy + r), fill=ORO, outline=LINEA, width=7 * SS)
    if k > 0.45:
        s = r * 0.42 * k
        d.ellipse((cx - s, cy - s * 1.1, cx + s, cy + s * 0.6), fill=CREMA, outline=LINEA, width=5 * SS)
        d.rectangle((cx - s * 0.5, cy + s * 0.3, cx + s * 0.5, cy + s * 0.85), fill=CREMA, outline=LINEA, width=5 * SS)
        for ox in (-0.38, 0.38):
            d.ellipse((cx + s * ox - s * 0.22, cy - s * 0.45, cx + s * ox + s * 0.22, cy - s * 0.05), fill=LINEA)
        d.line((cx - s * 1.3, cy + s * 1.35, cx + s * 1.3, cy + s * 0.75), fill=CREMA, width=10 * SS)
        d.line((cx - s * 1.3, cy + s * 0.75, cx + s * 1.3, cy + s * 1.35), fill=CREMA, width=10 * SS)


def forziere(d, cx, cy, s, apri=0.0, luce=0.0):
    """Forziere di legno con borchie d'oro; apri 0..1 solleva il coperchio."""
    if luce > 0:
        r = s * (1.6 + 0.2 * math.sin(luce * 9))
        d.ellipse((cx - r, cy - r * 1.1, cx + r, cy + r * 0.6), fill=(255, 220, 110, int(110 * min(1, luce))))
    d.rounded_rectangle((cx - s, cy - s * 0.1, cx + s, cy + s * 0.8), radius=10 * SS, fill=LEGNO, outline=LINEA, width=7 * SS)
    alza = apri * s * 0.55
    d.rounded_rectangle((cx - s * 1.02, cy - s * 0.55 - alza, cx + s * 1.02, cy - s * 0.05 - alza * 0.4), radius=40 * SS, fill=LEGNO2, outline=LINEA, width=7 * SS)
    for x in (-0.65, 0.65):
        d.rectangle((cx + s * x - s * 0.08, cy - s * 0.1, cx + s * x + s * 0.08, cy + s * 0.8), fill=ORO2, outline=LINEA, width=4 * SS)
    d.rounded_rectangle((cx - s * 0.16, cy - s * 0.02, cx + s * 0.16, cy + s * 0.3), radius=6 * SS, fill=ORO, outline=LINEA, width=4 * SS)


def moneta_gancio(p, t, w, h):
    """Apertura: la moneta da pirata che gira sopra un mare e brilla."""
    im, d = tela(w, h)
    W, H = w * SS, h * SS
    gradiente(im, NOTTE, NOTTE2, 0, int(H * 0.70))
    d = ImageDraw.Draw(im, 'RGBA')
    d.rectangle((0, H * 0.70, W, H), fill=MARE + (255,))
    for i in range(7):
        y = H * (0.73 + 0.04 * i); x = (t * 60 * SS + i * 170 * SS) % W
        d.arc((x - 70 * SS, y - 12 * SS, x + 70 * SS, y + 12 * SS), 200, 340, fill=MARE2 + (255,), width=5 * SS)
    cx, cy = W * 0.72, H * 0.42 + 14 * SS * math.sin(t * 2)
    for k in range(10):
        a = k * math.pi / 5 + t
        d.line((cx + math.cos(a) * 190 * SS, cy + math.sin(a) * 190 * SS, cx + math.cos(a) * 240 * SS, cy + math.sin(a) * 240 * SS), fill=(255, 220, 110, 200), width=8 * SS)
    moneta(d, cx, cy, 150 * SS, giro=t * 3)
    return fine(im, w, h)


def negozio(p, t, w, h):
    """Il premio: il negozio dove i prezzi diventano GRATIS per 14 giorni."""
    im, d = tela(w, h, (250, 244, 232, 255))
    W, H = w * SS, h * SS
    d.rectangle((W * 0.06, H * 0.10, W * 0.94, H * 0.20), fill=ROSSO, outline=LINEA, width=7 * SS)
    for i in range(6):
        x = W * (0.06 + i * 0.147)
        d.pieslice((x, H * 0.15, x + W * 0.147, H * 0.25), 0, 180, fill=CREMA if i % 2 else ROSSO, outline=LINEA, width=5 * SS)
    f, g = font(46), font(40)
    for i in range(4):
        c, r = i % 2, i // 2
        x0, y0 = W * (0.10 + 0.43 * c), H * (0.30 + 0.30 * r)
        d.rounded_rectangle((x0, y0, x0 + W * 0.37, y0 + H * 0.25), radius=24 * SS, fill=CREMA, outline=LINEA, width=6 * SS)
        col = [VIOLA, BLU + (255,) if len(BLU) == 3 else BLU, VERDE, ARANCIO][i]
        d.ellipse((x0 + W * 0.10, y0 + H * 0.03, x0 + W * 0.27, y0 + H * 0.15), fill=col, outline=LINEA, width=5 * SS)
        gratis = t > 0.6 + i * 0.35
        testo = 'GRATIS' if gratis else '1.500 V'
        tw = d.textlength(testo, font=f if gratis else g)
        d.rounded_rectangle((x0 + (W * 0.37 - tw) / 2 - 14 * SS, y0 + H * 0.17, x0 + (W * 0.37 + tw) / 2 + 14 * SS, y0 + H * 0.23),
                            radius=16 * SS, fill=VERDE if gratis else (230, 222, 210, 255), outline=LINEA, width=4 * SS)
        d.text((x0 + (W * 0.37 - tw) / 2, y0 + H * 0.175), testo, font=f if gratis else g, fill=CREMA if gratis else LINEA)
    etichetta(d, W, H, '14 giorni gratis', y=0.90, col=(43, 33, 28, 255), dim=60)
    return fine(im, w, h)


def probabilita(p, t, w, h):
    """1 su 137.500: una griglia di forzieri che si allarga, uno solo brilla."""
    im, d = tela(w, h, (34, 38, 64, 255))
    W, H = w * SS, h * SS
    z = 1 + 5 * (1 - min(1, t / 2.2))      # parte vicino e si allontana: i forzieri diventano tantissimi
    s = 46 * SS / z * 1.0
    passo = s * 2.6
    cols = int(W / passo) + 2; rows = int(H * 0.72 / passo) + 2
    for r in range(rows):
        for c in range(cols):
            cx = c * passo + passo / 2; cy = H * 0.30 + r * passo
            speciale = (r == rows // 2 and c == cols // 2)
            if s > 8 * SS:
                forziere(d, cx, cy, s, luce=(t if speciale else 0))
            else:
                d.rectangle((cx - s, cy - s * 0.5, cx + s, cy + s * 0.6), fill=ORO if speciale else LEGNO)
    f = font(96)
    testo = '1 su 137.500'
    tw = d.textlength(testo, font=f)
    d.rounded_rectangle(((W - tw) / 2 - 30 * SS, H * 0.04, (W + tw) / 2 + 30 * SS, H * 0.04 + 140 * SS), radius=30 * SS, fill=ROSSO, outline=LINEA, width=6 * SS)
    d.text(((W - tw) / 2, H * 0.04 + 14 * SS), testo, font=f, fill=CREMA)
    etichetta(d, W, H, 'per ogni forziere', y=0.20, dim=48)
    return fine(im, w, h)


def slot(p, t, w, h):
    """Premio raro e casuale: la slot machine dei forzieri."""
    im, d = tela(w, h, (255, 244, 226, 255))
    W, H = w * SS, h * SS
    x0, y0, x1, y1 = W * 0.12, H * 0.16, W * 0.80, H * 0.80
    d.rounded_rectangle((x0, y0, x1, y1), radius=50 * SS, fill=ROSSO, outline=LINEA, width=8 * SS)
    d.rounded_rectangle((x0 + 40 * SS, y0 + 120 * SS, x1 - 40 * SS, y0 + 420 * SS), radius=24 * SS, fill=CREMA, outline=LINEA, width=6 * SS)
    simboli = ['forziere', 'moneta', 'x']
    larg = (x1 - x0 - 80 * SS) / 3
    for i in range(3):
        cx = x0 + 40 * SS + larg * (i + 0.5); cy = y0 + 270 * SS
        fermo = t > 0.8 + i * 0.45
        k = 0 if fermo else int(t * 12 + i * 3) % 3
        sim = 'moneta' if (fermo and i < 2) else ('forziere' if fermo else simboli[k])
        if sim == 'moneta': moneta(d, cx, cy, 70 * SS, giro=0)
        elif sim == 'forziere': forziere(d, cx, cy + 10 * SS, 70 * SS)
        else:
            d.line((cx - 50 * SS, cy - 50 * SS, cx + 50 * SS, cy + 50 * SS), fill=LINEA, width=14 * SS)
            d.line((cx - 50 * SS, cy + 50 * SS, cx + 50 * SS, cy - 50 * SS), fill=LINEA, width=14 * SS)
    # leva
    ang = math.radians(-60 + 50 * max(0, math.sin(t * 2)))
    lx, ly = x1 + 10 * SS, y0 + 220 * SS
    ex, ey = lx + math.cos(ang) * 200 * SS, ly + math.sin(ang) * 200 * SS
    d.line((lx, ly, ex, ey), fill=ACCIAIO, width=16 * SS)
    d.ellipse((ex - 34 * SS, ey - 34 * SS, ex + 34 * SS, ey + 34 * SS), fill=ROSSO, outline=LINEA, width=6 * SS)
    etichetta(d, W, H, 'quasi... ritenta!', y=0.86, col=(43, 33, 28, 255), dim=58)
    return fine(im, w, h)


def calendario(p, t, w, h):
    """Tempo limitato: il calendario fino al 5 dicembre e il conto alla rovescia."""
    im, d = tela(w, h, (250, 246, 236, 255))
    W, H = w * SS, h * SS
    x0, y0, x1, y1 = W * 0.10, H * 0.12, W * 0.90, H * 0.72
    d.rounded_rectangle((x0, y0, x1, y1), radius=36 * SS, fill=CREMA, outline=LINEA, width=8 * SS)
    d.rounded_rectangle((x0, y0, x1, y0 + 130 * SS), radius=36 * SS, fill=ROSSO, outline=LINEA, width=8 * SS)
    f = font(64)
    tw = d.textlength('DICEMBRE', font=f)
    d.text(((W - tw) / 2, y0 + 28 * SS), 'DICEMBRE', font=f, fill=CREMA)
    g = font(48)
    for n in range(1, 15):
        c, r = (n - 1) % 7, (n - 1) // 7
        cx = x0 + (x1 - x0) * (c + 0.5) / 7; cy = y0 + 220 * SS + r * 130 * SS
        tw = d.textlength(str(n), font=g)
        d.text((cx - tw / 2, cy - 30 * SS), str(n), font=g, fill=LINEA if n != 5 else ROSSO)
        if n == 5:
            k = 1 + 0.1 * math.sin(t * 6)
            d.ellipse((cx - 56 * SS * k, cy - 52 * SS * k, cx + 56 * SS * k, cy + 52 * SS * k), outline=ROSSO, width=8 * SS)
        if n < 5 and t > 0.3 * n:
            d.line((cx - 34 * SS, cy - 30 * SS, cx + 34 * SS, cy + 30 * SS), fill=(120, 104, 94, 255), width=6 * SS)
    secondi = int(max(0, 59 - t * 3))
    testo = f'finisce tra 0g 23h 59m {secondi:02d}s'
    h2 = font(46)
    tw = d.textlength(testo, font=h2)
    d.rounded_rectangle(((W - tw) / 2 - 24 * SS, H * 0.78, (W + tw) / 2 + 24 * SS, H * 0.78 + 90 * SS), radius=24 * SS, fill=LINEA)
    d.text(((W - tw) / 2, H * 0.78 + 18 * SS), testo, font=h2, fill=ORO)
    return fine(im, w, h)


def ore_tesoro(p, t, w, h):
    """Le ore del tesoro: un appuntamento a orario fisso con probabilità moltiplicate."""
    im, d = tela(w, h, (34, 38, 64, 255))
    W, H = w * SS, h * SS
    gradiente(im, (34, 38, 64), (70, 60, 110))
    d = ImageDraw.Draw(im, 'RGBA')
    cx, cy, r = W * 0.5, H * 0.42, 230 * SS
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=CREMA, outline=LINEA, width=10 * SS)
    for i in range(12):
        a = i * math.pi / 6
        d.line((cx + math.cos(a) * r * 0.82, cy + math.sin(a) * r * 0.82, cx + math.cos(a) * r * 0.92, cy + math.sin(a) * r * 0.92), fill=LINEA, width=8 * SS)
    am = -math.pi / 2 + t * 1.5
    d.line((cx, cy, cx + math.cos(am) * r * 0.75, cy + math.sin(am) * r * 0.75), fill=LINEA, width=10 * SS)
    d.line((cx, cy, cx + r * 0.45, cy), fill=LINEA, width=14 * SS)
    d.ellipse((cx - 16 * SS, cy - 16 * SS, cx + 16 * SS, cy + 16 * SS), fill=LINEA)
    k = 1 + 0.12 * max(0, math.sin(t * 5))
    f = font(int(150 * k))
    tw = d.textlength('x2', font=f)
    d.text((W * 0.80 - tw / 2, H * 0.12), 'x2', font=f, fill=ORO, stroke_width=8 * SS, stroke_fill=LINEA)
    etichetta(d, W, H, 'le ore del tesoro', y=0.80, dim=64)
    return fine(im, w, h)


def due_token(p, t, w, h):
    """Chi lo trova ne riceve due: uno per il 2026 e uno per il 2027."""
    im, d = tela(w, h, (250, 244, 232, 255))
    W, H = w * SS, h * SS
    f = font(70)
    for i, (anno, x) in enumerate((('2026', 0.30), ('2027', 0.70))):
        k = min(1, max(0, (t - i * 0.6) / 0.4))
        if k <= 0: continue
        cy = H * 0.45 - (1 - k) * 80 * SS
        moneta(d, W * x, cy, 130 * SS * (0.6 + 0.4 * k), giro=0.15 * math.sin(t * 3 + i))
        tw = d.textlength(anno, font=f)
        d.text((W * x - tw / 2, H * 0.66), anno, font=f, fill=ROSSO if i else LINEA)
    if t > 1.2:
        d.line((W * 0.40, H * 0.80, W * 0.60, H * 0.80), fill=LINEA, width=8 * SS)
        d.polygon([(W * 0.60, H * 0.80 - 22 * SS), (W * 0.60, H * 0.80 + 22 * SS), (W * 0.65, H * 0.80)], fill=LINEA)
    etichetta(d, W, H, 'torni anche l\'anno prossimo', y=0.86, col=(43, 33, 28, 255), dim=50)
    return fine(im, w, h)


def social(p, t, w, h):
    """Meme, video e crossover: il telefono che si riempie di notifiche."""
    im, d = tela(w, h, (232, 240, 252, 255))
    W, H = w * SS, h * SS
    x0, y0, x1, y1 = W * 0.08, H * 0.06, W * 0.92, H * 0.94
    d.rounded_rectangle((x0, y0, x1, y1), radius=70 * SS, fill=(40, 40, 46, 255), outline=LINEA, width=8 * SS)
    d.rounded_rectangle((x0 + 22 * SS, y0 + 60 * SS, x1 - 22 * SS, y1 - 40 * SS), radius=40 * SS, fill=CREMA)
    righe = [('🏴', 'trovato il token!!'), ('▶', 'video: 1 su 137.500'), ('😂', 'io dopo 300 forzieri'), ('⚓', 'crossover One Piece'), ('🔔', 'ore del tesoro: ora!')]
    g = font(40)
    n = min(len(righe), int(t * 2.2) + 1)
    for i in range(n):
        y = y0 + 90 * SS + i * 150 * SS
        k = min(1, (t * 2.2 - i) / 0.6)
        xo = (1 - k) * 200 * SS
        d.rounded_rectangle((x0 + 40 * SS + xo, y, x1 - 40 * SS + xo, y + 120 * SS), radius=26 * SS, fill=(255, 255, 255, 255), outline=(200, 190, 180, 255), width=3 * SS)
        d.ellipse((x0 + 60 * SS + xo, y + 26 * SS, x0 + 128 * SS + xo, y + 94 * SS), fill=[ROSSO, BLU, ORO, (40, 110, 170, 255), VERDE][i], outline=LINEA, width=4 * SS)
        d.text((x0 + 150 * SS + xo, y + 38 * SS), righe[i][1], font=g, fill=LINEA)
    return fine(im, w, h)


def prossimo(p, t, w, h):
    """Il trucco: il prossimo forziere, che brilla e promette."""
    im, d = tela(w, h, (34, 38, 64, 255))
    W, H = w * SS, h * SS
    gradiente(im, (24, 30, 58), (60, 56, 100))
    d = ImageDraw.Draw(im, 'RGBA')
    forziere(d, W * 0.5, H * 0.56, 190 * SS, apri=0.15 + 0.1 * math.sin(t * 3), luce=t + 1)
    q = font(int(220 * (1 + 0.05 * math.sin(t * 4))))
    tw = d.textlength('?', font=q)
    d.text((W / 2 - tw / 2, H * 0.12), '?', font=q, fill=ORO, stroke_width=8 * SS, stroke_fill=LINEA)
    etichetta(d, W, H, 'il prossimo forziere...', y=0.84, dim=58)
    return fine(im, w, h)


SCENE = {'f_moneta': moneta_gancio, 'negozio': negozio, 'probabilita': probabilita, 'slot': slot,
         'calendario': calendario, 'ore_tesoro': ore_tesoro, 'due_token': due_token, 'social': social,
         'prossimo': prossimo}

if __name__ == '__main__':
    S = sys.argv[1]
    nomi = list(SCENE)
    tav = Image.new('RGB', (5 * 310, 2 * 410), (90, 90, 90))
    for i, n in enumerate(nomi):
        im = SCENE[n](0.85, 2.4, 760, 1000).resize((300, 395))
        tav.paste(im, ((i % 5) * 310 + 5, (i // 5) * 410 + 5))
    tav.save(f'{S}/scene_fortnite.png')

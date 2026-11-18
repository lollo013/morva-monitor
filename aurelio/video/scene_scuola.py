"""Illustrazioni originali per «La scuola assomiglia a una prigione?».

Formato ricorrente «SCUOLA vs CARCERE»: schermo diviso, a sinistra la scuola, a destra il
carcere, con lo stesso gesto o la stessa regola. Simboli generici, nessuna scuola o carcere reali.
f(p, t, w, h, **extra) -> immagine RGB.
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from scene_cielo import tela, fine, font, mix, gradiente, LINEA, CREMA, ORO, ROSSO, ARANCIO, BLU, SS
from scene_inception import etichetta, NOTTE, NOTTE2, ACCIAIO, SAIO, VERDE

AZZURRO = (120, 178, 228, 255)
GRIGIO = (128, 134, 146, 255)
GRIGIO2 = (92, 98, 110, 255)
MURO = (196, 198, 204, 255)
PELLE = (252, 200, 150, 255)


def omino(d, cx, base, s, col, seduto=False, braccio_su=False):
    d.ellipse((cx - s * 0.3, base - s * 1.75, cx + s * 0.3, base - s * 1.15), fill=PELLE, outline=LINEA, width=5 * SS)
    alto = base - s * 1.15
    basso = base - (s * 0.45 if seduto else 0)
    d.rounded_rectangle((cx - s * 0.36, alto, cx + s * 0.36, basso), radius=14 * SS, fill=col, outline=LINEA, width=5 * SS)
    if braccio_su:
        d.line((cx + s * 0.3, alto + s * 0.15, cx + s * 0.55, alto - s * 0.55), fill=LINEA, width=10 * SS)
        d.ellipse((cx + s * 0.47, alto - s * 0.7, cx + s * 0.65, alto - s * 0.5), fill=PELLE, outline=LINEA, width=4 * SS)


def sbarre(d, x0, y0, x1, y1, n=6, col=GRIGIO2):
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        d.line((x, y0, x, y1), fill=col, width=12 * SS)
    d.line((x0, y0, x1, y0), fill=col, width=14 * SS)
    d.line((x0, y1, x1, y1), fill=col, width=14 * SS)


def diviso(w, h, t):
    """Fondo diviso: SCUOLA a sinistra, CARCERE a destra."""
    im, d = tela(w, h)
    W, H = w * SS, h * SS
    d.rectangle((0, 0, W / 2, H), fill=(236, 244, 252, 255))
    d.rectangle((W / 2, 0, W, H), fill=(226, 226, 230, 255))
    d.line((W / 2, 0, W / 2, H), fill=LINEA, width=7 * SS)
    f = font(50)
    for x, testo, col in ((0.25, 'SCUOLA', (40, 100, 180, 255)), (0.75, 'CARCERE', GRIGIO2)):
        tw = d.textlength(testo, font=f)
        d.rounded_rectangle((W * x - tw / 2 - 22 * SS, H * 0.04, W * x + tw / 2 + 22 * SS, H * 0.04 + 84 * SS), radius=40 * SS, fill=col)
        d.text((W * x - tw / 2, H * 0.04 + 12 * SS), testo, font=f, fill=CREMA)
    return im, d, W, H


def didascalia(d, W, H, testo, y=0.88):
    etichetta(d, W, H, testo, y=y, col=(43, 33, 28, 255), dim=46)


def sveglia(p, t, w, h):
    """La sveglia che suona all'alba: il sonno che servirebbe e quello che resta."""
    im, d = tela(w, h)
    W, H = w * SS, h * SS
    gradiente(im, (38, 44, 84), (120, 104, 150))
    d = ImageDraw.Draw(im, 'RGBA')
    # finestra con l'alba
    d.rectangle((W * 0.08, H * 0.08, W * 0.46, H * 0.36), fill=(255, 176, 120, 255), outline=LINEA, width=7 * SS)
    d.ellipse((W * 0.20, H * 0.26, W * 0.34, H * 0.40), fill=(255, 226, 120, 255))
    d.rectangle((W * 0.08, H * 0.30, W * 0.46, H * 0.36), fill=(120, 104, 150, 255))
    d.line((W * 0.27, H * 0.08, W * 0.27, H * 0.36), fill=LINEA, width=6 * SS)
    # sveglia che trema
    trema = 6 * math.sin(t * 40) if (t % 1.0) < 0.6 else 0
    cx, cy, r = W * 0.72, H * 0.24, 110 * SS
    a = math.radians(trema)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=ROSSO, outline=LINEA, width=7 * SS)
    d.ellipse((cx - r * 0.8, cy - r * 0.8, cx + r * 0.8, cy + r * 0.8), fill=CREMA, outline=LINEA, width=4 * SS)
    d.line((cx, cy, cx + math.sin(a) * r * 0.6, cy - math.cos(a) * r * 0.6), fill=LINEA, width=7 * SS)
    d.line((cx, cy, cx - r * 0.45, cy + r * 0.15), fill=LINEA, width=7 * SS)
    g = font(46)
    d.text((cx - 70 * SS, cy + r + 14 * SS), '6:45', font=g, fill=CREMA, stroke_width=3 * SS, stroke_fill=LINEA)
    # barre del sonno
    f = font(40)
    y0 = H * 0.55
    d.text((W * 0.08, y0 - 70 * SS), 'servono', font=f, fill=CREMA)
    d.rounded_rectangle((W * 0.08, y0, W * 0.92, y0 + 80 * SS), radius=20 * SS, fill=(96, 178, 104, 255), outline=LINEA, width=5 * SS)
    d.text((W * 0.12, y0 + 14 * SS), '8-10 ore', font=g, fill=CREMA, stroke_width=3 * SS, stroke_fill=LINEA)
    k = min(1, t / 1.2)
    y1 = H * 0.72
    d.text((W * 0.08, y1 - 70 * SS), 'con la sveglia presto', font=f, fill=CREMA)
    d.rounded_rectangle((W * 0.08, y1, W * 0.08 + (W * 0.84) * (1 - 0.3 * k), y1 + 80 * SS), radius=20 * SS, fill=(230, 150, 60, 255), outline=LINEA, width=5 * SS)
    if k >= 1:
        d.rounded_rectangle((W * 0.08 + W * 0.84 * 0.7, y1, W * 0.92, y1 + 80 * SS), radius=20 * SS, outline=ROSSO, width=6 * SS)
        f2 = font(40); tw = d.textlength('sonno arretrato', font=f2)
        d.text((W * 0.92 - tw, y1 + 96 * SS), 'sonno arretrato', font=f2, fill=CREMA, stroke_width=3 * SS, stroke_fill=LINEA)
    return fine(im, w, h)


def orario(p, t, w, h):
    """8:00 contro 8:30: l'orario consigliato dagli esperti del sonno."""
    im, d = tela(w, h, (250, 246, 236, 255))
    W, H = w * SS, h * SS
    f, g = font(64), font(42)
    for i, (x, ora, minuti, testo, col) in enumerate(((0.27, '8:00', 0, 'molte scuole', ROSSO), (0.73, '8:30', 30, 'consigliato', (96, 178, 104, 255)))):
        cx, cy, r = W * x, H * 0.40, 150 * SS
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=CREMA, outline=LINEA, width=8 * SS)
        for k in range(12):
            a = k * math.pi / 6
            d.line((cx + math.cos(a) * r * 0.82, cy + math.sin(a) * r * 0.82, cx + math.cos(a) * r * 0.92, cy + math.sin(a) * r * 0.92), fill=LINEA, width=5 * SS)
        am = -math.pi / 2 + (minuti / 60) * 2 * math.pi
        ah = -math.pi / 2 + ((8 + minuti / 60) / 12) * 2 * math.pi
        d.line((cx, cy, cx + math.cos(am) * r * 0.78, cy + math.sin(am) * r * 0.78), fill=LINEA, width=8 * SS)
        d.line((cx, cy, cx + math.cos(ah) * r * 0.5, cy + math.sin(ah) * r * 0.5), fill=LINEA, width=12 * SS)
        tw = d.textlength(ora, font=f)
        d.text((cx - tw / 2, H * 0.62), ora, font=f, fill=col)
        tw = d.textlength(testo, font=g)
        d.text((cx - tw / 2, H * 0.71), testo, font=g, fill=LINEA)
    if t > 0.8:
        didascalia(d, W, H, 'gli esperti: dalle 8:30', y=0.86)
    return fine(im, w, h)


def cancello(p, t, w, h):
    im, d, W, H = diviso(w, h, t)
    k = min(1, t / 1.3)
    # scuola: cancello che si chiude davanti all'edificio
    d.rectangle((W * 0.06, H * 0.22, W * 0.44, H * 0.58), fill=(240, 220, 190, 255), outline=LINEA, width=6 * SS)
    d.polygon([(W * 0.04, H * 0.23), (W * 0.25, H * 0.15), (W * 0.46, H * 0.23)], fill=ROSSO, outline=LINEA, width=6 * SS)
    for i in range(3):
        d.rectangle((W * (0.10 + 0.11 * i), H * 0.30, W * (0.17 + 0.11 * i), H * 0.38), fill=AZZURRO, outline=LINEA, width=4 * SS)
    lato = W * 0.19 * k
    sbarre(d, W * 0.06, H * 0.52, W * 0.06 + lato, H * 0.78, n=4, col=(60, 60, 70, 255))
    sbarre(d, W * 0.44 - lato, H * 0.52, W * 0.44, H * 0.78, n=4, col=(60, 60, 70, 255))
    # carcere: muro e porta a sbarre
    d.rectangle((W * 0.54, H * 0.18, W * 0.96, H * 0.78), fill=MURO, outline=LINEA, width=6 * SS)
    sbarre(d, W * 0.62, H * 0.34, W * 0.88, H * 0.78, n=6)
    g = font(44)
    d.text((W * 0.10, H * 0.82), 'ore 8:00', font=g, fill=LINEA)
    d.text((W * 0.60, H * 0.82), 'orario fisso', font=g, fill=LINEA)
    return fine(im, w, h)


def appello(p, t, w, h):
    im, d, W, H = diviso(w, h, t)
    g = font(38)
    # registro con le spunte
    d.rounded_rectangle((W * 0.06, H * 0.18, W * 0.44, H * 0.80), radius=20 * SS, fill=CREMA, outline=LINEA, width=6 * SS)
    nomi = ['Rossi', 'Bianchi', 'Russo', 'Ferrari', 'Esposito', 'Romano']
    for i, n in enumerate(nomi):
        y = H * (0.24 + 0.09 * i)
        d.text((W * 0.10, y), n, font=g, fill=LINEA)
        if t > 0.25 * i:
            d.line((W * 0.36, y + 22 * SS, W * 0.38, y + 40 * SS), fill=(96, 178, 104, 255), width=7 * SS)
            d.line((W * 0.38, y + 40 * SS, W * 0.42, y), fill=(96, 178, 104, 255), width=7 * SS)
    # conta: tacche che si contano
    f = font(60)
    tw = d.textlength('CONTA', font=f)
    d.text((W * 0.75 - tw / 2, H * 0.20), 'CONTA', font=f, fill=GRIGIO2)
    n = min(12, int(t * 5) + 1)
    for i in range(n):
        gx, gy = W * (0.58 + 0.08 * (i % 5)), H * (0.36 + 0.14 * (i // 5))
        if i % 5 == 4:
            d.line((W * 0.56, gy + 70 * SS, W * 0.92, gy + 10 * SS), fill=ROSSO, width=8 * SS)
        else:
            d.line((gx, gy, gx, gy + 80 * SS), fill=LINEA, width=10 * SS)
    d.text((W * 0.10, H * 0.84), 'appello', font=font(46), fill=LINEA)
    d.text((W * 0.62, H * 0.84), 'la conta', font=font(46), fill=LINEA)
    return fine(im, w, h)


def seduto(p, t, w, h):
    im, d, W, H = diviso(w, h, t)
    # banchi in fila
    for r in range(3):
        for c in range(2):
            cx, base = W * (0.15 + 0.19 * c), H * (0.38 + 0.17 * r)
            d.rectangle((cx - 60 * SS, base - 20 * SS, cx + 60 * SS, base), fill=(200, 150, 100, 255), outline=LINEA, width=4 * SS)
            omino(d, cx, base - 20 * SS, 70 * SS, AZZURRO, seduto=True)
    # cella con branda
    d.rectangle((W * 0.56, H * 0.20, W * 0.94, H * 0.78), fill=MURO, outline=LINEA, width=6 * SS)
    d.rectangle((W * 0.60, H * 0.60, W * 0.90, H * 0.66), fill=(150, 120, 90, 255), outline=LINEA, width=5 * SS)
    omino(d, W * 0.75, H * 0.60, 90 * SS, (230, 150, 60, 255), seduto=True)
    sbarre(d, W * 0.56, H * 0.20, W * 0.94, H * 0.78, n=5, col=(70, 74, 84, 255))
    # contatore delle ore
    ore = min(6, 1 + int(t * 3))
    didascalia(d, W, H, f'seduti per {ore} ore', y=0.86)
    return fine(im, w, h)


def permesso(p, t, w, h):
    im, d, W, H = diviso(w, h, t)
    omino(d, W * 0.25, H * 0.70, 170 * SS, AZZURRO, braccio_su=True)
    f = font(48)
    d.rounded_rectangle((W * 0.05, H * 0.16, W * 0.46, H * 0.30), radius=30 * SS, fill=CREMA, outline=LINEA, width=5 * SS)
    d.text((W * 0.08, H * 0.19), 'posso andare?', font=f, fill=LINEA)
    # porta chiusa con mazzo di chiavi
    d.rectangle((W * 0.62, H * 0.20, W * 0.88, H * 0.74), fill=(120, 124, 136, 255), outline=LINEA, width=7 * SS)
    kx, ky = W * 0.75, H * 0.48 + 12 * SS * math.sin(t * 5)
    d.ellipse((kx - 44 * SS, ky - 44 * SS, kx + 44 * SS, ky + 44 * SS), outline=ORO, width=10 * SS)
    for i in range(3):
        a = math.radians(60 + i * 30)
        x2, y2 = kx + math.cos(a) * 140 * SS, ky + math.sin(a) * 140 * SS
        d.line((kx + math.cos(a) * 44 * SS, ky + math.sin(a) * 44 * SS, x2, y2), fill=ORO, width=10 * SS)
    didascalia(d, W, H, 'serve il permesso', y=0.86)
    return fine(im, w, h)


def telefono(p, t, w, h):
    im, d, W, H = diviso(w, h, t)
    for x, cosa in ((0.25, 'spento'), (0.75, 'consegnato')):
        cx = W * x
        d.rounded_rectangle((cx - 90 * SS, H * 0.24, cx + 90 * SS, H * 0.62), radius=26 * SS, fill=(40, 40, 46, 255), outline=LINEA, width=6 * SS)
        d.rounded_rectangle((cx - 74 * SS, H * 0.27, cx + 74 * SS, H * 0.58), radius=16 * SS, fill=(20, 20, 24, 255))
        if t > 0.6:
            d.ellipse((cx - 120 * SS, H * 0.30, cx + 120 * SS, H * 0.56), outline=ROSSO, width=12 * SS)
            d.line((cx - 85 * SS, H * 0.52, cx + 85 * SS, H * 0.34), fill=ROSSO, width=12 * SS)
        tw = d.textlength(cosa, font=font(46))
        d.text((cx - tw / 2, H * 0.70), cosa, font=font(46), fill=LINEA)
    return fine(im, w, h)


def pausa(p, t, w, h, rivela=0.0):
    """Il confronto chiave: 10-15 minuti di ricreazione contro almeno 4 ore all'aria aperta."""
    im, d, W, H = diviso(w, h, t)
    base = H * 0.80
    alt_max = H * 0.48
    k = min(1, t / 1.5)
    # 15 minuti contro 240: altezze in proporzione vera
    for x, minuti, col, testo in ((0.25, 15, (40, 100, 180, 255), '10-15 min'), (0.75, 240, (230, 150, 60, 255), 'almeno 4 ore')):
        if x > 0.5 and p < rivela:      # la barra del carcere arriva solo quando la voce la dice
            q = font(200)
            tw = d.textlength('?', font=q)
            d.text((W * x - tw / 2, H * 0.40), '?', font=q, fill=GRIGIO2)
            continue
        kk = k if x < 0.5 else min(1, max(0, (p - rivela) * 3))
        a = alt_max * (minuti / 240) * kk
        d.rounded_rectangle((W * x - 90 * SS, base - max(a, 6 * SS), W * x + 90 * SS, base), radius=16 * SS, fill=col, outline=LINEA, width=6 * SS)
        g = font(54)
        tw = d.textlength(testo, font=g)
        d.text((W * x - tw / 2, base - max(a, 6 * SS) - 80 * SS), testo, font=g, fill=LINEA, stroke_width=3 * SS, stroke_fill=(255, 255, 255, 255))
    d.line((W * 0.04, base, W * 0.96, base), fill=LINEA, width=6 * SS)
    g = font(40)
    for x, r in ((0.25, 'ricreazione'), (0.75, "all'aria aperta")):
        tw = d.textlength(r, font=g)
        d.text((W * x - tw / 2, base + 20 * SS), r, font=g, fill=LINEA)
    return fine(im, w, h)


def campanella(p, t, w, h):
    im, d = tela(w, h, (255, 236, 200, 255))
    W, H = w * SS, h * SS
    a = math.radians(18 * math.sin(t * 14))
    cx, cy = W * 0.5, H * 0.20
    c, s = math.cos(a), math.sin(a)
    rot = lambda x, y: (cx + x * c - y * s, cy + x * s + y * c)
    corpo = [rot(-170 * SS, 380 * SS), rot(-120 * SS, 120 * SS), rot(-60 * SS, 40 * SS), rot(60 * SS, 40 * SS), rot(120 * SS, 120 * SS), rot(170 * SS, 380 * SS)]
    d.polygon(corpo, fill=ORO, outline=LINEA, width=8 * SS)
    bx, by = rot(0, 420 * SS)
    d.ellipse((bx - 40 * SS, by - 40 * SS, bx + 40 * SS, by + 40 * SS), fill=(214, 150, 40, 255), outline=LINEA, width=6 * SS)
    for lato in (-1, 1):
        for k in (1, 1.25):
            d.arc((cx - 300 * SS * k, H * 0.18, cx + 300 * SS * k, H * 0.70), 200 if lato < 0 else 300, 240 if lato < 0 else 340, fill=ROSSO, width=8 * SS)
    f = font(100)
    tw = d.textlength('DRIIIN!', font=f)
    d.text(((W - tw) / 2, H * 0.74), 'DRIIIN!', font=f, fill=ROSSO, stroke_width=5 * SS, stroke_fill=(255, 255, 255, 255))
    return fine(im, w, h)


def strada(p, t, w, h):
    """La scuola non è una prigione: la porta aperta, gli amici e la tua strada."""
    im, d = tela(w, h)
    W, H = w * SS, h * SS
    gradiente(im, (130, 196, 240), (230, 244, 252))
    d = ImageDraw.Draw(im, 'RGBA')
    d.ellipse((W * 0.70, H * 0.06, W * 0.92, H * 0.22), fill=(255, 214, 90, 255), outline=LINEA, width=6 * SS)
    d.rectangle((0, H * 0.62, W, H), fill=(120, 186, 104, 255))
    d.polygon([(W * 0.42, H * 0.62), (W * 0.58, H * 0.62), (W * 0.85, H), (W * 0.15, H)], fill=(230, 210, 170, 255), outline=LINEA, width=5 * SS)
    k = min(1, t / 1.0)
    d.rectangle((W * 0.08, H * 0.28, W * 0.34, H * 0.62), fill=(255, 240, 200, 255), outline=LINEA, width=6 * SS)
    d.rectangle((W * 0.05, H * 0.25, W * 0.37, H * 0.28), fill=(200, 150, 100, 255), outline=LINEA, width=5 * SS)
    d.polygon([(W * 0.08, H * 0.28), (W * 0.08 + W * 0.20 * (1 - k), H * 0.30), (W * 0.08 + W * 0.20 * (1 - k), H * 0.60), (W * 0.08, H * 0.62)], fill=SAIO, outline=LINEA, width=5 * SS)
    for i, col in enumerate((AZZURRO, (230, 150, 60, 255), (96, 178, 104, 255))):
        x = W * (0.42 + 0.10 * i) + math.sin(t * 3 + i) * 6 * SS
        omino(d, x, H * 0.74 + i * 10 * SS, 110 * SS, col)
    etichetta(d, W, H, 'la tua strada', y=0.88, col=(43, 33, 28, 255), dim=56)
    return fine(im, w, h)


SCENE = {'sveglia_presto': sveglia, 'orario': orario, 'cancello': cancello, 'appello': appello, 'seduto': seduto,
         'permesso': permesso, 'telefono': telefono, 'pausa': pausa, 'campanella': campanella, 'strada': strada}

if __name__ == '__main__':
    S = sys.argv[1]
    nomi = list(SCENE)
    tav = Image.new('RGB', (5 * 310, 2 * 410), (90, 90, 90))
    for i, n in enumerate(nomi):
        im = SCENE[n](0.85, 2.4, 760, 1000).resize((300, 395))
        tav.paste(im, ((i % 5) * 310 + 5, (i // 5) * 410 + 5))
    tav.save(f'{S}/scene_scuola.png')

"""Illustrazioni originali per «Inception spiegato in 2 minuti».

Nessuna immagine del film e nessun volto di attori: solo simboli disegnati nello stile
del Professore (contorno scuro, colori pieni). f(p, t, w, h, **extra) -> immagine RGB.
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from scene_cielo import tela, fine, font, mix, gradiente, nuvola, LINEA, CREMA, ORO, ROSSO, ARANCIO, BLU, SS

NOTTE = (24, 30, 58)
NOTTE2 = (52, 62, 112)
PELLE = (252, 186, 122, 255)
GRIGIO = (150, 156, 170, 255)
VERDE = (96, 178, 104, 255)
VIOLA = (122, 92, 170, 255)
ACCIAIO = (196, 204, 214, 255)
SAIO = (107, 74, 53, 255)


def etichetta(d, W, H, testo, y=0.07, col=CREMA, dim=56):
    f = font(dim)
    tw = d.textlength(testo, font=f)
    scuro = sum(col[:3]) < 360
    d.text(((W - tw) / 2, H * y), testo, font=f, fill=col, stroke_width=4 * SS,
           stroke_fill=(255, 255, 255, 255) if scuro else LINEA)


def trottola(d, cx, cy, s, ang=0.0, giri=0.0):
    """Trottola vista di lato; ang = inclinazione (gradi) quando vacilla, giri = fase della rotazione."""
    a = math.radians(ang)
    c, si = math.cos(a), math.sin(a)
    rot = lambda x, y: (cx + x * c - y * si, cy + x * si + y * c)
    corpo = [rot(-s, -s * 0.1), rot(0, -s * 0.55), rot(s, -s * 0.1), rot(s * 0.15, s * 0.9), rot(-s * 0.15, s * 0.9)]
    d.polygon(corpo, fill=ACCIAIO, outline=LINEA, width=7 * SS)
    for k in range(3):   # strisce che girano
        x = math.sin(giri + k * 2.1) * s * 0.8
        if math.cos(giri + k * 2.1) > 0:
            d.line([rot(x, -s * 0.25), rot(x * 0.3, s * 0.6)], fill=(110, 118, 132, 255), width=6 * SS)
    d.line([rot(0, -s * 0.55), rot(0, -s * 1.0)], fill=LINEA, width=12 * SS)
    d.line([rot(-s * 0.15, s * 0.9), rot(0, s * 1.05), rot(s * 0.15, s * 0.9)], fill=LINEA, width=6 * SS)


def gancio(p, t, w, h):
    """Apertura: una trottola enorme che gira su un tavolo, nel buio."""
    im, d = tela(w, h, NOTTE + (255,))
    W, H = w * SS, h * SS
    gradiente(im, NOTTE, NOTTE2)
    d = ImageDraw.Draw(im, 'RGBA')
    d.rectangle((0, H * 0.72, W, H), fill=(120, 80, 56, 255))
    d.line((0, H * 0.72, W, H * 0.72), fill=LINEA, width=7 * SS)
    cx, cy, s = W * 0.76, H * 0.56, 170 * SS
    for k in range(4):
        r = s * (1.3 + 0.18 * k)
        d.arc((cx - r, cy - r * 0.35, cx + r, cy + r * 0.35), 200 + t * 300 + k * 40, 320 + t * 300 + k * 40, fill=(255, 255, 255, 90), width=5 * SS)
    trottola(d, cx, cy, s, ang=4 * math.sin(t * 9), giri=t * 18)
    d.ellipse((cx - s * 0.7, H * 0.72 - 14 * SS, cx + s * 0.7, H * 0.72 + 14 * SS), fill=(0, 0, 0, 70))
    return fine(im, w, h)


def testa(d, cx, cy, s, col=(232, 210, 186, 255)):
    """Profilo di una testa generica, senza volto."""
    d.ellipse((cx - s, cy - s, cx + s, cy + s * 0.9), fill=col, outline=LINEA, width=7 * SS)
    d.polygon([(cx - s * 0.45, cy + s * 0.6), (cx + s * 0.35, cy + s * 0.6), (cx + s * 0.25, cy + s * 1.35), (cx - s * 0.35, cy + s * 1.35)],
              fill=col, outline=LINEA, width=7 * SS)
    d.polygon([(cx + s * 0.95, cy - s * 0.05), (cx + s * 1.18, cy + s * 0.25), (cx + s * 0.92, cy + s * 0.3)], fill=col, outline=LINEA, width=6 * SS)


def lampadina(d, cx, cy, s, acceso=1.0):
    if acceso > 0.05:
        r = s * (1.7 + 0.15 * math.sin(acceso * 20))
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 220, 90, int(90 * acceso)))
    d.ellipse((cx - s, cy - s, cx + s, cy + s * 0.9), fill=mix((230, 230, 230), (255, 214, 90), acceso) + (255,), outline=LINEA, width=6 * SS)
    d.rounded_rectangle((cx - s * 0.45, cy + s * 0.8, cx + s * 0.45, cy + s * 1.35), radius=6 * SS, fill=ACCIAIO, outline=LINEA, width=5 * SS)


def ladro(p, t, w, h):
    """Ruba idee: una lampadina esce dalla testa e una mano la porta via."""
    im, d = tela(w, h, (250, 243, 230, 255))
    W, H = w * SS, h * SS
    testa(d, W * 0.40, H * 0.55, 200 * SS)
    k = min(1, t / 1.6)
    lx, ly = W * 0.40 + k * W * 0.18, H * 0.45 - k * H * 0.17
    lampadina(d, lx, ly, 70 * SS, 1.0)
    # mano guantata che la afferra
    gx, gy = lx + 70 * SS, ly - 20 * SS
    d.rounded_rectangle((gx, gy - 36 * SS, gx + 160 * SS, gy + 36 * SS), radius=36 * SS, fill=(40, 40, 46, 255), outline=LINEA, width=6 * SS)
    for k2 in range(3):
        d.rounded_rectangle((gx - 20 * SS, gy - 30 * SS + k2 * 22 * SS, gx + 30 * SS, gy - 12 * SS + k2 * 22 * SS), radius=9 * SS, fill=(40, 40, 46, 255), outline=LINEA, width=4 * SS)
    etichetta(d, W, H, 'ruba IDEE', col=(43, 33, 28, 255), dim=64)
    return fine(im, w, h)


def sogni(p, t, w, h):
    """Entra nei sogni: una persona che dorme e una porta che si apre nella nuvola del sogno."""
    im, d = tela(w, h, NOTTE + (255,))
    W, H = w * SS, h * SS
    gradiente(im, NOTTE, NOTTE2)
    d = ImageDraw.Draw(im, 'RGBA')
    # letto e dormiente generico
    d.rounded_rectangle((W * 0.08, H * 0.70, W * 0.92, H * 0.84), radius=20 * SS, fill=(200, 210, 236, 255), outline=LINEA, width=7 * SS)
    d.ellipse((W * 0.12, H * 0.62, W * 0.30, H * 0.74), fill=(232, 210, 186, 255), outline=LINEA, width=6 * SS)
    d.rounded_rectangle((W * 0.26, H * 0.64, W * 0.90, H * 0.74), radius=30 * SS, fill=(150, 90, 180, 255), outline=LINEA, width=6 * SS)
    for i in range(3):
        f = (t * 0.6 + i / 3) % 1
        d.ellipse((W * (0.30 + 0.05 * i), H * (0.58 - 0.06 * i) - f * 40 * SS, W * (0.30 + 0.05 * i) + (16 + 10 * i) * SS, H * (0.58 - 0.06 * i) + (16 + 10 * i) * SS - f * 40 * SS), fill=CREMA)
    nuvola(d, W * 0.60, H * 0.32, 150 * SS)
    # porta che si apre dentro il sogno
    apri = min(1, t / 1.2)
    px0, py0, px1, py1 = W * 0.52, H * 0.18, W * 0.68, H * 0.42
    d.rectangle((px0, py0, px1, py1), fill=(255, 228, 140, 255), outline=LINEA, width=6 * SS)
    d.polygon([(px0, py0), (px0 + (px1 - px0) * (1 - 0.7 * apri), py0 + 10 * SS * apri), (px0 + (px1 - px0) * (1 - 0.7 * apri), py1 - 10 * SS * apri), (px0, py1)],
              fill=SAIO, outline=LINEA, width=6 * SS)
    etichetta(d, W, H, 'dentro i sogni', dim=58)
    return fine(im, w, h)


def seme(p, t, w, h):
    """Piantare un'idea: un seme entra nella testa e germoglia in una lampadina."""
    im, d = tela(w, h, (236, 246, 228, 255))
    W, H = w * SS, h * SS
    testa(d, W * 0.42, H * 0.56, 210 * SS)
    k = min(1, t / 0.8)
    sx, sy = W * 0.42, H * 0.12 + k * H * 0.30
    if k < 1:
        d.ellipse((sx - 26 * SS, sy - 36 * SS, sx + 26 * SS, sy + 36 * SS), fill=(140, 96, 60, 255), outline=LINEA, width=5 * SS)
    else:
        g = min(1, (t - 0.8) / 1.0)
        top = H * 0.45 - g * H * 0.18
        d.line((sx, H * 0.47, sx, top), fill=VERDE, width=12 * SS)
        for lato in (-1, 1):
            d.ellipse((sx + lato * 10 * SS - (45 * SS if lato < 0 else 0), H * 0.42 - g * 60 * SS, sx + lato * 10 * SS + (45 * SS if lato > 0 else 0), H * 0.42 - g * 60 * SS + 34 * SS), fill=VERDE, outline=LINEA, width=4 * SS)
        if g > 0.4:
            lampadina(d, sx, top - 60 * SS, 56 * SS, min(1, (g - 0.4) / 0.4))
    etichetta(d, W, H, 'PIANTARE un\'idea', col=(43, 33, 28, 255), dim=60)
    return fine(im, w, h)


def impero(p, t, w, h, crepa=0.5):
    """L'impero di Fischer: un grattacielo che si divide in due."""
    im, d = tela(w, h, (232, 238, 248, 255))
    W, H = w * SS, h * SS
    gradiente(im, (210, 226, 246), (246, 248, 252))
    d = ImageDraw.Draw(im, 'RGBA')
    k = min(1, max(0, (p - crepa) / 0.3))
    gap = k * 70 * SS
    x0, x1, y0, y1 = W * 0.28, W * 0.72, H * 0.14, H * 0.90
    mid = (x0 + x1) / 2
    for lato in (-1, 1):
        xa, xb = (x0 - gap, mid - gap) if lato < 0 else (mid + gap, x1 + gap)
        d.rectangle((xa, y0 + (1 - lato) * 8 * SS, xb, y1), fill=(92, 104, 138, 255), outline=LINEA, width=7 * SS)
        for r in range(9):
            for c in range(2):
                fx = xa + (xb - xa) * (0.18 + 0.42 * c); fy = y0 + 50 * SS + r * (y1 - y0 - 80 * SS) / 9
                d.rectangle((fx, fy, fx + (xb - xa) * 0.25, fy + 34 * SS), fill=(255, 226, 120, 255) if (r + c + int(t * 3)) % 3 else (180, 196, 226, 255))
    if 0 < k < 1:
        d.line((mid, y0, mid, y1), fill=ROSSO, width=8 * SS)
    d.rectangle((0, y1, W, H), fill=(120, 128, 140, 255))
    etichetta(d, W, H, 'l\'impero di Fischer', y=0.03, col=(43, 33, 28, 255), dim=54)
    return fine(im, w, h)


def casa(p, t, w, h):
    """Tornare a casa dai figli: una casetta con la luce accesa e un cuore."""
    im, d = tela(w, h, (255, 236, 206, 255))
    W, H = w * SS, h * SS
    gradiente(im, (255, 214, 160), (255, 244, 224))
    d = ImageDraw.Draw(im, 'RGBA')
    d.rectangle((0, H * 0.78, W, H), fill=(120, 186, 104, 255))
    x0, x1, y0, y1 = W * 0.22, W * 0.78, H * 0.42, H * 0.80
    d.rectangle((x0, y0, x1, y1), fill=(245, 236, 222, 255), outline=LINEA, width=7 * SS)
    d.polygon([(x0 - 40 * SS, y0 + 6 * SS), ((x0 + x1) / 2, H * 0.18), (x1 + 40 * SS, y0 + 6 * SS)], fill=ROSSO, outline=LINEA, width=7 * SS)
    d.rectangle((W * 0.44, H * 0.60, W * 0.56, y1), fill=SAIO, outline=LINEA, width=6 * SS)
    for wx in (0.30, 0.62):
        d.rectangle((W * wx, H * 0.50, W * (wx + 0.10), H * 0.58), fill=(255, 220, 110, 255), outline=LINEA, width=5 * SS)
    b = 1 + 0.12 * max(0, math.sin(t * 5))
    cx, cy, s = W * 0.5, H * 0.10, 70 * SS * b
    pts = []
    for i in range(60):
        a = i / 60 * 2 * math.pi
        pts.append((cx + 16 * math.sin(a) ** 3 * s / 16, cy - (13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a)) * s / 16))
    d.polygon(pts, fill=ROSSO, outline=LINEA, width=6 * SS)
    return fine(im, w, h)


def LIVELLO(d, x0, y0, x1, y1, tipo, t):
    """Mini-scenari dei livelli: città sotto la pioggia, albergo, fortezza nella neve."""
    if tipo == 0:
        d.rectangle((x0, y0, x1, y1), fill=(96, 110, 140, 255))
        for i in range(5):
            bx = x0 + (x1 - x0) * (0.06 + i * 0.19)
            d.rectangle((bx, y1 - (y1 - y0) * (0.4 + 0.1 * (i % 3)), bx + (x1 - x0) * 0.14, y1), fill=(60, 70, 96, 255))
        for i in range(18):
            rx = x0 + ((i * 53 + t * 400) % (x1 - x0)); ry = y0 + ((i * 37 + t * 700) % (y1 - y0))
            d.line((rx, ry, rx - 6 * SS, ry + 20 * SS), fill=(200, 220, 255, 200), width=3 * SS)
    elif tipo == 1:
        d.rectangle((x0, y0, x1, y1), fill=(176, 120, 90, 255))
        for i in range(4):
            cx = x0 + (x1 - x0) * (0.12 + i * 0.25)
            d.rectangle((cx, y0 + (y1 - y0) * 0.25, cx + (x1 - x0) * 0.14, y1), fill=(120, 70, 50, 255), outline=LINEA, width=3 * SS)
            d.ellipse((cx + (x1 - x0) * 0.1, y0 + (y1 - y0) * 0.6, cx + (x1 - x0) * 0.13, y0 + (y1 - y0) * 0.66), fill=ORO)
    else:
        d.rectangle((x0, y0, x1, y1), fill=(220, 234, 246, 255))
        d.polygon([(x0, y1), (x0 + (x1 - x0) * 0.3, y0 + (y1 - y0) * 0.2), (x0 + (x1 - x0) * 0.6, y1)], fill=(250, 252, 255, 255), outline=LINEA, width=3 * SS)
        d.rectangle((x0 + (x1 - x0) * 0.6, y0 + (y1 - y0) * 0.35, x0 + (x1 - x0) * 0.85, y1), fill=(150, 160, 176, 255), outline=LINEA, width=3 * SS)
        for i in range(14):
            sx = x0 + ((i * 61 + t * 60) % (x1 - x0)); sy = y0 + ((i * 29 + t * 120) % (y1 - y0))
            d.ellipse((sx, sy, sx + 7 * SS, sy + 7 * SS), fill=(255, 255, 255, 255))
    d.rectangle((x0, y0, x1, y1), outline=LINEA, width=6 * SS)


def livelli(p, t, w, h):
    """Un sogno dentro un sogno: tre livelli che scendono uno dentro l'altro."""
    im, d = tela(w, h, (34, 38, 64, 255))
    W, H = w * SS, h * SS
    nomi = ['1 · città', '2 · albergo', '3 · fortezza']
    f = font(44)
    for i in range(3):
        k = min(1, max(0, (t - i * 0.7) / 0.4))
        if k <= 0: continue
        m = W * (0.06 + 0.07 * i)
        y0 = H * (0.08 + 0.29 * i) + (1 - k) * 60 * SS
        LIVELLO(d, m, y0, W - m, y0 + H * 0.24, i, t)
        d.text((m + 20 * SS, y0 + 14 * SS), nomi[i], font=f, fill=CREMA, stroke_width=3 * SS, stroke_fill=LINEA)
        if i < 2 and k >= 1:
            ax = W / 2; ay = y0 + H * 0.245
            d.polygon([(ax - 30 * SS, ay), (ax + 30 * SS, ay), (ax, ay + 34 * SS)], fill=ORO, outline=LINEA, width=4 * SS)
    return fine(im, w, h)


def orologi(p, t, w, h):
    """Più scendi, più il tempo rallenta: la stessa durata si allunga a ogni livello."""
    im, d = tela(w, h, (255, 250, 240, 255))
    W, H = w * SS, h * SS
    righe = [('realtà', '10 ore', 1.0), ('sogno 1', '1 settimana', 0.45), ('sogno 2', '6 mesi', 0.18), ('sogno 3', '10 anni', 0.05)]
    f, g = font(46), font(56)
    for i, (nome, durata, vel) in enumerate(righe):
        k = min(1, max(0, (p * 1.6 - i * 0.28) / 0.25))
        if k <= 0: continue
        y = H * (0.12 + 0.22 * i)
        cx, r = W * 0.20, 70 * SS
        d.ellipse((cx - r, y - r, cx + r, y + r), fill=CREMA, outline=LINEA, width=7 * SS)
        a = t * 6 * vel - math.pi / 2
        d.line((cx, y, cx + math.cos(a) * r * 0.8, y + math.sin(a) * r * 0.8), fill=ROSSO, width=7 * SS)
        d.ellipse((cx - 9 * SS, y - 9 * SS, cx + 9 * SS, y + 9 * SS), fill=LINEA)
        d.text((W * 0.36, y - 66 * SS), nome, font=f, fill=(120, 104, 94, 255))
        d.text((W * 0.36, y - 6 * SS), durata, font=g, fill=(43, 33, 28, 255))
    return fine(im, w, h)


def calcio(p, t, w, h):
    """Il calcio: una caduta improvvisa che sveglia tutti i livelli insieme."""
    im, d = tela(w, h, (34, 38, 64, 255))
    W, H = w * SS, h * SS
    for i in range(3):
        y0 = H * (0.06 + 0.31 * i)
        flash = (t % 1.4) < 0.18
        LIVELLO(d, W * 0.06, y0, W * 0.94, y0 + H * 0.27, i, t)
        if flash:
            d.rectangle((W * 0.06, y0, W * 0.94, y0 + H * 0.27), fill=(255, 255, 255, 150))
        # figurina che cade
        cy = y0 + H * 0.05 + ((t * 1.4) % 1) * H * 0.18
        cx = W * 0.5
        d.ellipse((cx - 20 * SS, cy - 20 * SS, cx + 20 * SS, cy + 20 * SS), fill=(232, 210, 186, 255), outline=LINEA, width=4 * SS)
        d.line((cx, cy + 20 * SS, cx, cy + 70 * SS), fill=LINEA, width=6 * SS)
        d.line((cx - 34 * SS, cy + 10 * SS, cx + 34 * SS, cy + 10 * SS), fill=LINEA, width=6 * SS)
        for k in range(3):
            d.line((cx - 50 * SS + k * 50 * SS, cy - 50 * SS, cx - 50 * SS + k * 50 * SS, cy - 90 * SS), fill=(255, 255, 255, 160), width=4 * SS)
    etichetta(d, W, H, 'CALCIO = caduta', y=0.0, dim=52)
    return fine(im, w, h)


def limbo(p, t, w, h):
    """Il limbo: un mare grigio senza fine e palazzi che si sgretolano all'orizzonte."""
    im, d = tela(w, h, (150, 158, 170, 255))
    W, H = w * SS, h * SS
    gradiente(im, (110, 118, 134), (196, 202, 210))
    d = ImageDraw.Draw(im, 'RGBA')
    d.rectangle((0, H * 0.62, W, H), fill=(120, 132, 150, 255))
    for i in range(7):
        bx = W * (0.05 + i * 0.13); bh = H * (0.15 + 0.08 * ((i * 3) % 4))
        top = H * 0.62 - bh
        d.rectangle((bx, top, bx + W * 0.09, H * 0.62), fill=(92, 98, 112, 255), outline=LINEA, width=4 * SS)
        for k in range(3):
            f = (t * 0.5 + k * 0.33 + i * 0.1) % 1
            d.rectangle((bx + W * 0.03 * k, top - f * 80 * SS, bx + W * 0.03 * k + 14 * SS, top - f * 80 * SS + 14 * SS), fill=(92, 98, 112, int(255 * (1 - f))))
    for i in range(6):
        y = H * (0.68 + 0.05 * i)
        x = (t * 80 * SS + i * 140 * SS) % W
        d.arc((x - 60 * SS, y - 10 * SS, x + 60 * SS, y + 10 * SS), 200, 340, fill=(230, 236, 244, 200), width=4 * SS)
    etichetta(d, W, H, 'LIMBO: un sogno senza fine', y=0.08, dim=50)
    return fine(im, w, h)


def fantasma(p, t, w, h):
    """Il ricordo di Mal: una sagoma trasparente e l'idea che il mondo non sia reale."""
    im, d = tela(w, h, (40, 34, 60, 255))
    W, H = w * SS, h * SS
    gradiente(im, (40, 34, 60), (90, 70, 110))
    d = ImageDraw.Draw(im, 'RGBA')
    a = int(120 + 60 * math.sin(t * 2))
    cx = W * 0.5 + 20 * SS * math.sin(t * 0.8)
    d.ellipse((cx - 90 * SS, H * 0.22, cx + 90 * SS, H * 0.22 + 200 * SS), fill=(230, 230, 255, a))
    d.polygon([(cx - 70 * SS, H * 0.22 + 180 * SS), (cx + 70 * SS, H * 0.22 + 180 * SS), (cx + 190 * SS, H * 0.86), (cx - 190 * SS, H * 0.86)], fill=(230, 230, 255, a))
    d.ellipse((cx - 180 * SS, H * 0.18, cx + 180 * SS, H * 0.18 + 360 * SS), outline=(255, 255, 255, 60), width=4 * SS)
    f = font(52)
    for i, r in enumerate(['«questo mondo', 'non è reale»']):
        tw = d.textlength(r, font=f)
        d.text(((W - tw) / 2, H * (0.88 + 0.06 * i) - 40 * SS), r, font=f, fill=CREMA, stroke_width=4 * SS, stroke_fill=LINEA)
    return fine(im, w, h)


def padre(p, t, w, h):
    """L'idea che riesce: il figlio smette di essere la copia del padre e diventa sé stesso."""
    im, d = tela(w, h, (250, 244, 232, 255))
    W, H = w * SS, h * SS
    def omino(cx, base, s, col):
        d.ellipse((cx - s * 0.35, base - s * 1.9, cx + s * 0.35, base - s * 1.2), fill=(232, 210, 186, 255), outline=LINEA, width=6 * SS)
        d.rounded_rectangle((cx - s * 0.45, base - s * 1.2, cx + s * 0.45, base), radius=20 * SS, fill=col, outline=LINEA, width=6 * SS)
    k = min(1, t / 1.5)
    omino(W * 0.30, H * 0.86, 220 * SS, (80, 80, 96, 255))
    col = mix((80, 80, 96), (96, 178, 104), k) + (255,)
    omino(W * 0.66 + k * 40 * SS, H * 0.86, 190 * SS * (1 + 0.1 * k), col)
    if k >= 1:
        sx, sy, r = W * 0.70 + 40 * SS, H * 0.30, 50 * SS * (1 + 0.1 * math.sin(t * 6))
        pts = [(sx + (r if i % 2 == 0 else r * 0.45) * math.cos(-math.pi / 2 + i * math.pi / 5),
                sy + (r if i % 2 == 0 else r * 0.45) * math.sin(-math.pi / 2 + i * math.pi / 5)) for i in range(10)]
        d.polygon(pts, fill=ORO, outline=LINEA, width=5 * SS)
    etichetta(d, W, H, 'sii te stesso', y=0.06, col=(43, 33, 28, 255), dim=60)
    return fine(im, w, h)


def finale(p, t, w, h, nero=0.75):
    """La trottola che gira, vacilla... e lo schermo diventa nero."""
    im, d = tela(w, h, NOTTE + (255,))
    W, H = w * SS, h * SS
    gradiente(im, (60, 52, 44), (120, 86, 60))
    d = ImageDraw.Draw(im, 'RGBA')
    d.rectangle((0, H * 0.70, W, H), fill=(140, 96, 64, 255))
    d.line((0, H * 0.70, W, H * 0.70), fill=LINEA, width=7 * SS)
    vacilla = max(0, p - 0.35) / 0.4
    trottola(d, W * 0.5, H * 0.54, 140 * SS, ang=min(14, vacilla * 14) * math.sin(t * (9 - 4 * min(1, vacilla))), giri=t * 16)
    k = min(1, max(0, (p - nero) / 0.12))
    if k > 0:
        d.rectangle((0, 0, W, H), fill=(0, 0, 0, int(255 * k)))
    return fine(im, w, h)


def domanda(p, t, w, h):
    """Sogno o realtà? Metà schermo per uno."""
    im, d = tela(w, h, (250, 246, 236, 255))
    W, H = w * SS, h * SS
    d.rectangle((0, 0, W / 2, H), fill=(52, 62, 112, 255))
    d.rectangle((W / 2, 0, W, H), fill=(255, 226, 150, 255))
    nuvola(d, W * 0.25, H * 0.42, 90 * SS)
    d.ellipse((W * 0.75 - 80 * SS, H * 0.42 - 80 * SS, W * 0.75 + 80 * SS, H * 0.42 + 80 * SS), fill=(255, 196, 70, 255), outline=LINEA, width=7 * SS)
    f = font(64)
    for x, testo, col, bordo in ((0.25, 'SOGNO', CREMA, LINEA), (0.75, 'REALTÀ', (43, 33, 28, 255), (255, 255, 255, 255))):
        tw = d.textlength(testo, font=f)
        d.text((W * x - tw / 2, H * 0.66), testo, font=f, fill=col, stroke_width=3 * SS, stroke_fill=bordo)
    q = font(int(300 * (1 + 0.06 * math.sin(t * 4))))
    tw = d.textlength('?', font=q)
    d.text((W / 2 - tw / 2, H * 0.08), '?', font=q, fill=CREMA, stroke_width=8 * SS, stroke_fill=LINEA)
    return fine(im, w, h)


SCENE = {'i_gancio': gancio, 'ladro': ladro, 'sogni': sogni, 'seme': seme, 'impero': impero, 'casa': casa,
         'livelli': livelli, 'orologi': orologi, 'calcio': calcio, 'limbo': limbo, 'fantasma': fantasma,
         'padre': padre, 'finale': finale, 'domanda': domanda}

if __name__ == '__main__':
    import sys
    S = sys.argv[1]
    nomi = list(SCENE)
    tav = Image.new('RGB', (5 * 310, 3 * 410), (90, 90, 90))
    for i, n in enumerate(nomi):
        im = SCENE[n](0.85, 2.2, 760, 1000).resize((300, 395))
        tav.paste(im, ((i % 5) * 310 + 5, (i // 5) * 410 + 5))
    tav.save(f'{S}/scene_inception.png')

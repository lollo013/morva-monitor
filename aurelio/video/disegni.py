"""Illustrazioni 2D dello scenario, disegnate a mano in codice nello stile del Professore:
contorno scuro spesso, colori pieni, palette calda. Ogni funzione restituisce un RGBA LATO x LATO.
p = avanzamento della scena (0..1), t = secondi dall'inizio della scena.
"""
import math
from PIL import Image, ImageDraw, ImageFont

LATO = 440
SS = 2
L = LATO * SS
LINEA = (43, 33, 28, 255)
W = 7 * SS
NOTTE = (44, 52, 94, 255)
NOTTE2 = (64, 74, 128, 255)
ORO = (233, 186, 84, 255)
CREMA = (255, 250, 240, 255)
ROSA = (244, 168, 170, 255)
ROSA2 = (226, 128, 136, 255)
ROSSO = (138, 47, 39, 255)
GRIGIO = (176, 170, 168, 255)
GRIGIO2 = (140, 132, 130, 255)
PELLE = (252, 186, 122, 255)
SAIO = (107, 74, 53, 255)
VERDE = (96, 160, 110, 255)

F = '/usr/share/fonts/opentype/inter/'
etich = ImageFont.truetype(F + 'InterDisplay-ExtraBold.otf', 34 * SS)
zfont = ImageFont.truetype(F + 'InterDisplay-ExtraBold.otf', 44 * SS)


def tela():
    im = Image.new('RGBA', (L, L), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def fine(im):
    return im.resize((LATO, LATO), Image.LANCZOS)


def stella(d, x, y, r, col=ORO):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    d.polygon(pts, fill=col, outline=LINEA, width=max(2, W // 2))


def nuvola(d, x, y, s, col=CREMA):
    for cx, cy, r in [(0, 0, 1.0), (-0.9, 0.25, 0.7), (0.95, 0.2, 0.75), (0.3, -0.45, 0.75)]:
        d.ellipse((x + (cx - r) * s, y + (cy - r) * s, x + (cx + r) * s, y + (cy + r) * s), fill=LINEA)
    for cx, cy, r in [(0, 0, 1.0), (-0.9, 0.25, 0.7), (0.95, 0.2, 0.75), (0.3, -0.45, 0.75)]:
        r2 = r - W / s
        d.ellipse((x + (cx - r2) * s, y + (cy - r2) * s, x + (cx + r2) * s, y + (cy + r2) * s), fill=col)


def sogno(p, t):
    """Finestra sul cielo notturno: luna, stelle che brillano, nuvola, Zzz."""
    im, d = tela()
    m = 30 * SS
    d.rounded_rectangle((m, m, L - m, L - m), radius=60 * SS, fill=NOTTE, outline=LINEA, width=W)
    # luna
    cx, cy, r = L * 0.52, L * 0.38, 88 * SS
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=ORO, outline=LINEA, width=W)
    d.ellipse((cx - r + 42 * SS, cy - r - 22 * SS, cx + r + 42 * SS, cy + r - 22 * SS), fill=NOTTE)
    for i, (x, y, rr) in enumerate([(0.22, 0.25, 22), (0.35, 0.55, 14), (0.82, 0.70, 16), (0.18, 0.72, 12)]):
        k = 0.75 + 0.25 * math.sin(t * 3 + i * 1.9)
        stella(d, L * x, L * y, rr * SS * k)
    nuvola(d, L * 0.42 + 18 * SS * math.sin(t * 0.8), L * 0.80, 52 * SS)
    for i in range(3):
        f = (t * 0.6 + i / 3) % 1
        a = int(255 * min(1, 2 - 2 * f) * min(1, 4 * f))
        d.text((L * (0.70 + 0.07 * i), L * (0.86 - 0.42 * f)), 'z', font=zfont, fill=(255, 245, 225, a))
    return fine(im)


def cervello(p, t):
    """Cervello attivissimo con il tracciato che corre: fase REM."""
    im, d = tela()
    cx, cy = L * 0.5, L * 0.56
    lobi = [(-0.42, -0.08, 0.36), (-0.12, -0.30, 0.38), (0.22, -0.24, 0.38), (0.42, 0.02, 0.33),
            (0.15, 0.18, 0.36), (-0.25, 0.18, 0.34)]
    s = L * 0.42
    for dx, dy, r in lobi:
        d.ellipse((cx + (dx - r) * s, cy + (dy - r) * s, cx + (dx + r) * s, cy + (dy + r) * s), fill=LINEA)
    for dx, dy, r in lobi:
        r2 = r - W / s
        d.ellipse((cx + (dx - r2) * s, cy + (dy - r2) * s, cx + (dx + r2) * s, cy + (dy + r2) * s), fill=ROSA)
    for a0, a1, dx, dy, r in [(200, 330, -0.15, -0.1, 0.25), (220, 340, 0.2, -0.05, 0.22), (20, 160, -0.05, 0.05, 0.25), (30, 150, 0.3, 0.1, 0.15)]:
        d.arc((cx + (dx - r) * s, cy + (dy - r) * s, cx + (dx + r) * s, cy + (dy + r) * s), a0, a1, fill=ROSA2, width=W)
    d.line((cx, cy - 0.5 * s, cx, cy + 0.35 * s), fill=ROSA2, width=W)
    # tracciato dell'attivita'
    y0 = L * 0.13
    pts = []
    for i in range(0, 61):
        x = L * 0.08 + i * (L * 0.84) / 60
        f = i / 60 * 14 - t * 9
        v = math.sin(f) * 0.6 + math.sin(f * 2.7) * 0.4
        pts.append((x, y0 + v * 30 * SS))
    d.line(pts, fill=ROSSO, width=W, joint='curve')
    # lampi di attivita'
    for i, (x, y) in enumerate([(0.12, 0.42), (0.88, 0.40), (0.86, 0.78)]):
        if math.sin(t * 6 + i * 2) > 0:
            d.line((L * x - 14 * SS, L * y, L * x + 14 * SS, L * y), fill=ORO, width=W)
            d.line((L * x, L * y - 14 * SS, L * x, L * y + 14 * SS), fill=ORO, width=W)
    return fine(im)


def noradrenalina(p, t):
    """Livello della noradrenalina che crolla quasi a zero."""
    im, d = tela()
    x0, x1, y0, y1 = L * 0.30, L * 0.62, L * 0.12, L * 0.82
    d.rounded_rectangle((x0 + 30 * SS, y0 - 26 * SS, x1 - 30 * SS, y0 + 8 * SS), radius=10 * SS, fill=GRIGIO, outline=LINEA, width=W)
    d.rounded_rectangle((x0, y0, x1, y1), radius=40 * SS, fill=CREMA, outline=LINEA, width=W)
    livello = 0.92 - 0.84 * min(1, max(0, (p - 0.1) / 0.6)) ** 0.8
    yl = y1 - W - (y1 - y0 - 2 * W) * livello
    col = VERDE if livello > 0.5 else (ORO if livello > 0.25 else ROSSO)
    d.rounded_rectangle((x0 + W, yl, x1 - W, y1 - W), radius=32 * SS, fill=col)
    for k in range(1, 4):
        y = y0 + (y1 - y0) * k / 4
        d.line((x0 + W, y, x0 + 40 * SS, y), fill=LINEA, width=W // 2)
    # freccia giu'
    ax = L * 0.80
    b = 10 * SS * math.sin(t * 5)
    d.rectangle((ax - 16 * SS, L * 0.30 + b, ax + 16 * SS, L * 0.56 + b), fill=ROSSO, outline=LINEA, width=W)
    d.polygon([(ax - 46 * SS, L * 0.54 + b), (ax + 46 * SS, L * 0.54 + b), (ax, L * 0.68 + b)], fill=ROSSO, outline=LINEA, width=W)
    tw = d.textlength('noradrenalina', font=etich)
    d.text(((L - tw) / 2, L * 0.86), 'noradrenalina', font=etich, fill=LINEA)
    return fine(im)


def ricordo(p, t):
    """Il ricordo del sogno che svanisce: una foto che si dissolve."""
    im, d = tela()
    ang = -6
    foto = Image.new('RGBA', (int(L * 0.72), int(L * 0.80)), (0, 0, 0, 0))
    fd = ImageDraw.Draw(foto)
    fw, fh = foto.size
    fd.rounded_rectangle((0, 0, fw - 1, fh - 1), radius=16 * SS, fill=CREMA, outline=LINEA, width=W)
    sk = Image.new('RGBA', (fw - 60 * SS, int(fh * 0.66)), NOTTE)
    sd = ImageDraw.Draw(sk)
    r = 60 * SS
    sd.ellipse((sk.width * 0.55 - r, sk.height * 0.42 - r, sk.width * 0.55 + r, sk.height * 0.42 + r), fill=ORO)
    sd.ellipse((sk.width * 0.55 - r + 35 * SS, sk.height * 0.42 - r - 15 * SS, sk.width * 0.55 + r + 35 * SS, sk.height * 0.42 + r - 15 * SS), fill=NOTTE)
    stella(sd, sk.width * 0.22, sk.height * 0.3, 18 * SS)
    svanisce = min(1, max(0, (p - 0.15) / 0.7))
    a = sk.split()[3].point(lambda v: int(v * (1 - 0.9 * svanisce)))
    sk.putalpha(a)
    foto.paste(sk, (30 * SS, 30 * SS), sk)
    fd.rectangle((30 * SS, 30 * SS, fw - 30 * SS, 30 * SS + sk.height), outline=LINEA, width=W // 2)
    fd.text((40 * SS, fh - 92 * SS), '?', font=zfont, fill=ROSSO)
    foto = foto.rotate(ang, resample=Image.BICUBIC, expand=True)
    im.paste(foto, ((L - foto.width) // 2, (L - foto.height) // 2), foto)
    # puntini che volano via
    for i in range(6):
        f = (svanisce * 1.4 + i * 0.13) % 1
        x = L * (0.7 + 0.25 * f); y = L * (0.35 + 0.08 * math.sin(i * 2 + f * 6)) - f * 60 * SS
        rr = (10 - i) * SS * (1 - f)
        if svanisce > 0.05 and rr > 1:
            d = ImageDraw.Draw(im)
            d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=ORO)
    return fine(im)


def neurone(d, cx, cy, s, t, acceso=True):
    rami = 7
    for i in range(rami):
        a = i * 2 * math.pi / rami + 0.3
        x1, y1 = cx + math.cos(a) * s * 1.6, cy + math.sin(a) * s * 1.6
        d.line((cx, cy, x1, y1), fill=LINEA, width=int(W * 1.8))
        d.line((cx, cy, x1, y1), fill=ROSA2, width=int(W * 0.8))
        for b in (-0.5, 0.5):
            x2, y2 = x1 + math.cos(a + b) * s * 0.55, y1 + math.sin(a + b) * s * 0.55
            d.line((x1, y1, x2, y2), fill=LINEA, width=int(W * 1.4))
            d.line((x1, y1, x2, y2), fill=ROSA2, width=int(W * 0.5))
    k = 1 + (0.12 * math.sin(t * 7) if acceso else 0)
    r = s * 0.62 * k
    if acceso:
        alone = r * 1.6
        d.ellipse((cx - alone, cy - alone, cx + alone, cy + alone), fill=(233, 186, 84, 70))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=ROSA, outline=LINEA, width=W)
    d.ellipse((cx - r * 0.35, cy - r * 0.35, cx + r * 0.35, cy + r * 0.35), fill=ROSSO)


def topo(d, cx, cy, s, t):
    # coda
    pts = [(cx + s * 0.9 + s * 0.15 * i, cy + s * 0.3 - s * 0.25 * math.sin(i * 0.9 + t * 4)) for i in range(8)]
    d.line(pts, fill=LINEA, width=int(W * 1.6), joint='curve')
    d.line(pts, fill=ROSA2, width=int(W * 0.6), joint='curve')
    d.ellipse((cx - s, cy - s * 0.6, cx + s, cy + s * 0.6), fill=GRIGIO, outline=LINEA, width=W)
    hx, hy = cx - s * 0.9, cy - s * 0.15
    for ex in (-0.15, 0.25):
        r = s * 0.32
        d.ellipse((hx + ex * s - r, hy - s * 0.55 - r, hx + ex * s + r, hy - s * 0.55 + r), fill=GRIGIO, outline=LINEA, width=W)
        d.ellipse((hx + ex * s - r * 0.55, hy - s * 0.55 - r * 0.55, hx + ex * s + r * 0.55, hy - s * 0.55 + r * 0.55), fill=ROSA)
    d.polygon([(hx - s * 0.55, hy + s * 0.1), (hx + s * 0.35, hy - s * 0.35), (hx + s * 0.4, hy + s * 0.4)], fill=GRIGIO, outline=LINEA, width=W)
    d.ellipse((hx - s * 0.63, hy + s * 0.02, hx - s * 0.47, hy + s * 0.18), fill=ROSA2, outline=LINEA, width=W // 2)
    d.ellipse((hx - s * 0.12, hy - s * 0.12, hx + s * 0.02, hy + s * 0.02), fill=LINEA)


def scoperta(p, t):
    """Lo studio del 2019: un topo che dorme e i neuroni che fanno dimenticare."""
    im, d = tela()
    d.rounded_rectangle((20 * SS, 20 * SS, L - 20 * SS, L - 20 * SS), radius=60 * SS, fill=(250, 241, 228, 255), outline=LINEA, width=W)
    neurone(d, L * 0.62, L * 0.36, 62 * SS, t, acceso=p > 0.25)
    topo(d, L * 0.36, L * 0.74, 70 * SS, t)
    for i in range(3):
        f = (t * 0.5 + i / 3) % 1
        a = int(255 * min(1, 2 - 2 * f) * min(1, 4 * f))
        d.text((L * (0.14 + 0.05 * i), L * (0.58 - 0.3 * f)), 'z', font=etich, fill=(44, 52, 94, a))
    tw = d.textlength('2019', font=etich)
    d.rounded_rectangle((L * 0.08, L * 0.08, L * 0.08 + tw + 40 * SS, L * 0.08 + 58 * SS), radius=28 * SS, fill=ROSSO)
    d.text((L * 0.08 + 20 * SS, L * 0.08 + 8 * SS), '2019', font=etich, fill=CREMA)
    return fine(im)


def sveglia(p, t):
    """Sveglia che suona: ci si ricorda il sogno se ci si sveglia durante."""
    im, d = tela()
    trema = 4 * math.sin(t * 40) if (t % 1.2) < 0.6 else 0
    c = Image.new('RGBA', (L, L), (0, 0, 0, 0))
    cd = ImageDraw.Draw(c)
    cx, cy, r = L / 2, L * 0.55, L * 0.30
    for sx in (-1, 1):
        bx = cx + sx * r * 0.72
        cd.ellipse((bx - r * 0.32, cy - r * 1.18, bx + r * 0.32, cy - r * 0.54), fill=ORO, outline=LINEA, width=W)
    for sx in (-1, 1):
        cd.line((cx + sx * r * 0.55, cy + r * 0.8, cx + sx * r * 0.8, cy + r * 1.15), fill=LINEA, width=int(W * 1.6))
    cd.ellipse((cx - r, cy - r, cx + r, cy + r), fill=ROSSO, outline=LINEA, width=W)
    cd.ellipse((cx - r * 0.8, cy - r * 0.8, cx + r * 0.8, cy + r * 0.8), fill=CREMA, outline=LINEA, width=W // 2)
    for i in range(12):
        a = i * math.pi / 6
        cd.line((cx + math.cos(a) * r * 0.66, cy + math.sin(a) * r * 0.66, cx + math.cos(a) * r * 0.74, cy + math.sin(a) * r * 0.74), fill=LINEA, width=W // 2)
    cd.line((cx, cy, cx, cy - r * 0.55), fill=LINEA, width=W)
    cd.line((cx, cy, cx + r * 0.42, cy + r * 0.1), fill=LINEA, width=W)
    cd.ellipse((cx - 10 * SS, cy - 10 * SS, cx + 10 * SS, cy + 10 * SS), fill=LINEA)
    c = c.rotate(trema, resample=Image.BICUBIC, center=(cx, cy))
    im.paste(c, (0, 0), c)
    if trema:
        for sx in (-1, 1):
            for k in (1.25, 1.45):
                d.arc((cx - r * k, cy - r * k, cx + r * k, cy + r * k), 200 if sx < 0 else 300, 240 if sx < 0 else 340, fill=ORO, width=W)
    return fine(im)


def quaderno(p, t):
    """Quaderno sul comodino: il sogno scritto subito."""
    im, d = tela()
    x0, y0, x1, y1 = L * 0.14, L * 0.12, L * 0.80, L * 0.90
    d.rounded_rectangle((x0 + 14 * SS, y0 + 14 * SS, x1 + 14 * SS, y1 + 14 * SS), radius=22 * SS, fill=SAIO, outline=LINEA, width=W)
    d.rounded_rectangle((x0, y0, x1, y1), radius=22 * SS, fill=CREMA, outline=LINEA, width=W)
    for i in range(7):
        y = y0 + 40 * SS + i * 38 * SS
        d.ellipse((x0 - 14 * SS, y - 9 * SS, x0 + 14 * SS, y + 9 * SS), fill=GRIGIO2, outline=LINEA, width=W // 2)
    righe = 6
    scritto = min(1, max(0, (p - 0.05) / 0.8)) * righe
    penna = None
    for i in range(righe):
        y = y0 + 70 * SS + i * 44 * SS
        d.line((x0 + 40 * SS, y + 14 * SS, x1 - 26 * SS, y + 14 * SS), fill=(214, 200, 186, 255), width=SS * 2)
        f = min(1, max(0, scritto - i))
        if f > 0:
            xa, xb = x0 + 46 * SS, x0 + 46 * SS + (x1 - x0 - 90 * SS) * f * (0.75 if i % 2 else 0.95)
            pts = [(x, y + 4 * SS * math.sin((x - xa) / (9 * SS))) for x in range(int(xa), int(xb) + 1, 3 * SS)]
            if len(pts) > 1:
                d.line(pts, fill=NOTTE, width=int(W * 0.8), joint='curve')
            if f < 1:
                penna = pts[-1] if pts else (xa, y)
    if penna is None:
        penna = (x1 - 40 * SS, y0 + 70 * SS + (righe - 1) * 44 * SS)
    px, py = penna
    px += 6 * SS * math.sin(t * 18)
    lung, larg = 170 * SS, 26 * SS
    a = math.radians(-50)
    dx, dy = math.cos(a), math.sin(a)
    nx, ny = -dy, dx
    punta = (px, py)
    base = (px + dx * 40 * SS, py + dy * 40 * SS)
    fine_ = (px + dx * lung, py + dy * lung)
    poly = [(base[0] + nx * larg / 2, base[1] + ny * larg / 2), (fine_[0] + nx * larg / 2, fine_[1] + ny * larg / 2),
            (fine_[0] - nx * larg / 2, fine_[1] - ny * larg / 2), (base[0] - nx * larg / 2, base[1] - ny * larg / 2)]
    d.polygon(poly, fill=ORO, outline=LINEA, width=W)
    d.polygon([punta, (base[0] + nx * larg / 2, base[1] + ny * larg / 2), (base[0] - nx * larg / 2, base[1] - ny * larg / 2)], fill=PELLE, outline=LINEA, width=W)
    return fine(im)


def cuore(d, cx, cy, s, col, bordo=True):
    pts = []
    for i in range(80):
        a = i / 80 * 2 * math.pi
        x = 16 * math.sin(a) ** 3
        y = -(13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a))
        pts.append((cx + x * s / 16, cy + y * s / 16))
    d.polygon(pts, fill=col, outline=LINEA if bordo else None, width=W if bordo else 0)


def invito(p, t):
    """Commenta, like e segui: fumetto del commento, cuore che pulsa, pulsante «+ Segui»."""
    im, d = tela()
    # fumetto del commento, con i puntini che si scrivono
    x0, y0, x1, y1 = L * 0.06, L * 0.08, L * 0.52, L * 0.42
    d.rounded_rectangle((x0, y0, x1, y1), radius=40 * SS, fill=CREMA, outline=LINEA, width=W)
    d.polygon([(x0 + 60 * SS, y1 - 4 * SS), (x0 + 120 * SS, y1 - 4 * SS), (x0 + 50 * SS, y1 + 60 * SS)], fill=CREMA, outline=LINEA, width=W)
    d.line((x0 + 64 * SS, y1 - 4 * SS, x0 + 114 * SS, y1 - 4 * SS), fill=CREMA, width=W + 2 * SS)
    n = int(t * 3) % 4
    for i in range(3):
        cx = (x0 + x1) / 2 + (i - 1) * 46 * SS
        col = NOTTE if i < n else GRIGIO
        d.ellipse((cx - 14 * SS, (y0 + y1) / 2 - 14 * SS, cx + 14 * SS, (y0 + y1) / 2 + 14 * SS), fill=col)
    # cuore
    batt = 1 + 0.08 * max(0, math.sin(t * 6))
    cuore(d, L * 0.74, L * 0.36, 92 * SS * batt, ROSSO)
    for i in range(3):
        f = (t * 0.7 + i / 3) % 1
        a = int(200 * (1 - f))
        x = (0.60, 0.94, 0.86)[i]
        cuore(d, L * x, L * (0.56 - 0.40 * f), 26 * SS, (226, 128, 136, a), bordo=False)
    # pulsante segui
    premuto = (t % 1.6) > 1.1
    y = L * 0.70 + (6 * SS if premuto else 0)
    testo = '+ Segui'
    tw = d.textlength(testo, font=zfont)
    bx0, bx1 = (L - tw) / 2 - 50 * SS, (L + tw) / 2 + 50 * SS
    if not premuto:
        d.rounded_rectangle((bx0, y + 12 * SS, bx1, y + 120 * SS), radius=56 * SS, fill=LINEA)
    d.rounded_rectangle((bx0, y, bx1, y + 108 * SS), radius=54 * SS, fill=ORO, outline=LINEA, width=W)
    d.text(((L - tw) / 2, y + 22 * SS), testo, font=zfont, fill=LINEA)
    return fine(im)


VIOLA = (150, 84, 140, 255)
VIOLA2 = (196, 132, 186, 255)
VERDE_GAS = (170, 214, 120, 255)
ACCIAIO = (200, 206, 214, 255)
AZZURRO = (120, 190, 235, 255)


def bulbo(d, cx, cy, s):
    """Cipolla intera: bulbo con strati e germoglio."""
    d.polygon([(cx - s * 0.12, cy - s * 0.85), (cx + s * 0.12, cy - s * 0.85), (cx + s * 0.05, cy - s * 1.25), (cx - s * 0.05, cy - s * 1.25)],
              fill=VERDE, outline=LINEA, width=W)
    pts = []
    for i in range(90):
        a = i / 90 * 2 * math.pi
        x = math.sin(a) * s * (0.95 - 0.25 * max(0, -math.cos(a)) ** 3)
        y = -math.cos(a) * s * 0.9 - (s * 0.25 if math.cos(a) > 0.92 else 0) * (math.cos(a) - 0.92) / 0.08
        pts.append((cx + x, cy + y))
    d.polygon(pts, fill=VIOLA, outline=LINEA, width=W)
    for k in (0.35, 0.65):
        d.arc((cx - s * k, cy - s * 0.85, cx + s * k, cy + s * 0.85), 270 - 70, 270 + 70, fill=VIOLA2, width=W)
        d.arc((cx - s * k, cy - s * 0.85, cx + s * k, cy + s * 0.85), 90 - 70, 90 + 70, fill=VIOLA2, width=W)
    for i in range(5):
        x = cx - s * 0.3 + i * s * 0.15
        d.line((x, cy + s * 0.88, x - s * 0.05 + i * s * 0.025, cy + s * 1.05), fill=LINEA, width=W // 2)


def goccia(d, cx, cy, s, col=AZZURRO):
    pts = []
    for i in range(60):
        a = i / 60 * 2 * math.pi
        r = s * (1 - 0.0) 
        x = math.sin(a) * s * 0.62 * (1 - 0.55 * max(0, math.cos(a)))
        y = -math.cos(a) * s
        pts.append((cx + x, cy + y * (0.75 if math.cos(a) < 0 else 1.0)))
    d.polygon(pts, fill=col, outline=LINEA, width=W)
    d.ellipse((cx - s * 0.25, cy - s * 0.05, cx - s * 0.05, cy + s * 0.25), fill=(235, 248, 255, 255))


def cipolla(p, t):
    """La domanda: una cipolla e una lacrima che scende."""
    im, d = tela()
    bulbo(d, L * 0.44, L * 0.60, 150 * SS)
    f = (t * 0.5) % 1
    goccia(d, L * 0.84, L * (0.20 + 0.45 * f), 40 * SS)
    d.text((L * 0.74, L * 0.80), '?', font=zfont, fill=ROSSO)
    return fine(im)


def coltello(d, x, y, s, ang=0):
    lama = [(0, 0), (s * 1.4, 0), (s * 1.3, s * 0.34), (s * 0.1, s * 0.34)]
    manico = [(-s * 0.75, s * 0.02), (0, s * 0.02), (0, s * 0.3), (-s * 0.75, s * 0.3)]
    c, si = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    rot = lambda pts: [(x + px * c - py * si, y + px * si + py * c) for px, py in pts]
    d.polygon(rot(lama), fill=ACCIAIO, outline=LINEA, width=W)
    d.rounded_rectangle((0, 0, 0, 0), radius=1)
    d.polygon(rot(manico), fill=SAIO, outline=LINEA, width=W)


def taglio(p, t):
    """Il coltello rompe le cellule: zolfo ed enzima si mescolano."""
    im, d = tela()
    # mezza cipolla vista in sezione
    cx, cy, r = L * 0.55, L * 0.80, 175 * SS
    d.pieslice((cx - r, cy - r, cx + r, cy + r), 180, 360, fill=VIOLA, outline=LINEA, width=W)
    for k in (0.8, 0.6, 0.4, 0.2):
        rr = r * k
        d.arc((cx - rr, cy - rr, cx + rr, cy + rr), 180, 360, fill=CREMA, width=int(W * 1.2))
    d.line((cx - r, cy, cx + r, cy), fill=LINEA, width=W)
    # coltello che scende e risale
    su = abs(math.sin(t * 2.6))
    coltello(d, L * 0.34, L * 0.14 + su * L * 0.26, 150 * SS, ang=0)
    # cellule che si rompono: puntini gialli (zolfo) e verdi (enzima) che si incontrano
    n = 6
    for i in range(n):
        f = min(1, max(0, p * 2.2 - i * 0.12))
        y = cy - L * 0.06 - (i % 3) * 24 * SS
        x1 = cx - r * 0.75 + i * r * 0.27
        d.ellipse((x1 - 16 * SS - (1 - f) * 22 * SS, y - 16 * SS, x1 + 16 * SS - (1 - f) * 22 * SS, y + 16 * SS), fill=ORO, outline=LINEA, width=W // 2)
        d.ellipse((x1 - 12 * SS + (1 - f) * 22 * SS, y - 12 * SS, x1 + 12 * SS + (1 - f) * 22 * SS, y + 12 * SS), fill=VERDE, outline=LINEA, width=W // 2)
    return fine(im)


def occhio(d, cx, cy, s, aperto=1.0):
    h = s * 0.55 * aperto
    d.chord((cx - s, cy - h, cx + s, cy + h), 0, 360, fill=CREMA, outline=LINEA, width=W)
    if aperto > 0.3:
        r = s * 0.36
        d.ellipse((cx - r, cy - min(r, h), cx + r, cy + min(r, h)), fill=(110, 80, 50, 255), outline=LINEA, width=W // 2)
        d.ellipse((cx - r * 0.45, cy - r * 0.45, cx + r * 0.45, cy + r * 0.45), fill=LINEA)
        d.ellipse((cx + r * 0.1, cy - r * 0.5, cx + r * 0.4, cy - r * 0.2), fill=CREMA)


def gas(p, t):
    """Il gas irritante sale dalla cipolla e vola verso gli occhi."""
    im, d = tela()
    cx, cy, r = L * 0.30, L * 0.86, 110 * SS
    d.pieslice((cx - r, cy - r, cx + r, cy + r), 180, 360, fill=VIOLA, outline=LINEA, width=W)
    d.line((cx - r, cy, cx + r, cy), fill=LINEA, width=W)
    occhio(d, L * 0.70, L * 0.22, 105 * SS, aperto=0.85 - 0.25 * max(0, math.sin(t * 3)))
    for i in range(7):
        f = (t * 0.45 + i / 7) % 1
        x = cx + (L * 0.72 - cx) * f + 30 * SS * math.sin(f * 9 + i)
        y = cy - r * 0.5 - (cy - r * 0.5 - L * 0.32) * f
        rr = (18 + 26 * f) * SS
        a = int(230 * min(1, 3 * (1 - f)))
        d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=VERDE_GAS[:3] + (a,))
    return fine(im)


def enzima(p, t):
    """Lo studio del 2002: l'enzima che fabbrica il gas."""
    im, d = tela()
    d.rounded_rectangle((20 * SS, 20 * SS, L - 20 * SS, L - 20 * SS), radius=60 * SS, fill=(250, 241, 228, 255), outline=LINEA, width=W)
    tw = d.textlength('2002', font=etich)
    d.rounded_rectangle((L * 0.08, L * 0.08, L * 0.08 + tw + 40 * SS, L * 0.08 + 58 * SS), radius=28 * SS, fill=ROSSO)
    d.text((L * 0.08 + 20 * SS, L * 0.08 + 8 * SS), '2002', font=etich, fill=CREMA)
    # enzima a forma di bocca che si apre e chiude
    bocca = 25 + 20 * abs(math.sin(t * 4))
    ex, ey, er = L * 0.40, L * 0.56, 120 * SS
    d.pieslice((ex - er, ey - er, ex + er, ey + er), bocca, 360 - bocca, fill=VERDE, outline=LINEA, width=W)
    d.ellipse((ex - 10 * SS, ey - er * 0.55, ex + 14 * SS, ey - er * 0.55 + 24 * SS), fill=LINEA)
    # molecole di zolfo in arrivo, nuvolette di gas in uscita
    for i in range(3):
        f = (t * 0.6 + i / 3) % 1
        x = L * 0.92 - (L * 0.92 - ex - er * 0.35) * f
        if f < 0.9:
            d.ellipse((x - 16 * SS, ey - 16 * SS, x + 16 * SS, ey + 16 * SS), fill=ORO, outline=LINEA, width=W // 2)
    for i in range(4):
        f = (t * 0.5 + i / 4) % 1
        x = ex + er * 0.55 + f * L * 0.08
        y = ey - er * 1.1 - f * L * 0.22
        rr = (16 + 18 * f) * SS
        d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=VERDE_GAS[:3] + (int(230 * (1 - f)),))
    return fine(im)


def lacrime(p, t):
    """Gli occhi si difendono: lacrime che lavano via il gas."""
    im, d = tela()
    for sx in (0.28, 0.72):
        occhio(d, L * sx, L * 0.32, 88 * SS, aperto=0.6)
        for k in range(2):
            f = (t * 0.7 + k * 0.5 + sx) % 1
            goccia(d, L * sx + 50 * SS, L * (0.45 + 0.42 * f), 30 * SS)
    for i in range(4):
        f = (t * 0.4 + i / 4) % 1
        x = L * (0.15 + 0.7 * i / 3); y = L * 0.12 - f * 40 * SS
        rr = 20 * SS * (1 - f)
        d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=VERDE_GAS[:3] + (int(160 * (1 - f)),))
    return fine(im)


def frigo(p, t):
    """Il consiglio: cipolla in frigo e coltello affilato."""
    im, d = tela()
    x0, y0, x1, y1 = L * 0.10, L * 0.08, L * 0.56, L * 0.92
    d.rounded_rectangle((x0, y0, x1, y1), radius=36 * SS, fill=(232, 240, 246, 255), outline=LINEA, width=W)
    d.line((x0, L * 0.38, x1, L * 0.38), fill=LINEA, width=W)
    d.rounded_rectangle((x1 - 40 * SS, L * 0.16, x1 - 24 * SS, L * 0.30), radius=8 * SS, fill=GRIGIO2, outline=LINEA, width=W // 2)
    d.rounded_rectangle((x1 - 40 * SS, L * 0.46, x1 - 24 * SS, L * 0.62), radius=8 * SS, fill=GRIGIO2, outline=LINEA, width=W // 2)
    bulbo(d, (x0 + x1) / 2 - 10 * SS, L * 0.68, 72 * SS)
    # fiocco di neve
    fx, fy, fr = (x0 + x1) / 2 - 30 * SS, L * 0.23, 46 * SS
    for k in range(3):
        a = math.radians(k * 60 + 20 * math.sin(t))
        d.line((fx - fr * math.cos(a), fy - fr * math.sin(a), fx + fr * math.cos(a), fy + fr * math.sin(a)), fill=AZZURRO, width=W)
    # coltello che luccica
    coltello(d, L * 0.70, L * 0.30, 140 * SS, ang=60)
    if (t % 1.4) < 0.5:
        sx, sy = L * 0.86, L * 0.62
        d.line((sx - 22 * SS, sy, sx + 22 * SS, sy), fill=ORO, width=W)
        d.line((sx, sy - 22 * SS, sx, sy + 22 * SS), fill=ORO, width=W)
    return fine(im)


SCENE = {'sogno': sogno, 'cervello': cervello, 'noradrenalina': noradrenalina, 'ricordo': ricordo,
         'scoperta': scoperta, 'sveglia': sveglia, 'quaderno': quaderno, 'invito': invito,
         'cipolla': cipolla, 'taglio': taglio, 'gas': gas, 'enzima': enzima, 'lacrime': lacrime, 'frigo': frigo}

if __name__ == '__main__':
    import sys
    S = sys.argv[1]
    tav = Image.new('RGBA', (LATO * 4, LATO * 2), (253, 252, 251, 255))
    for i, (n, f) in enumerate(SCENE.items()):
        im = f(0.6, 1.3)
        tav.paste(im, ((i % 4) * LATO, (i // 4) * LATO), im)
    tav.convert('RGB').save(f'{S}/disegni.png')

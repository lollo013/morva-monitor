"""Illustrazioni originali per «Duemila euro e la regola 50-30-20». f(p, t, w, h, **extra) -> RGB."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from scene_cielo import tela, fine, font, mix, gradiente, LINEA, CREMA, ORO, ROSSO, ARANCIO, BLU, SS
from scene_inception import etichetta, SAIO, VERDE
from scene_larping import banconota, moneta_oro, ORO_SCURO

C50 = (64, 120, 210, 255)     # necessità
C30 = (240, 150, 60, 255)     # desideri
C20 = (96, 178, 104, 255)     # risparmio
SCURO = (43, 33, 28, 255)


def busta(p, t, w, h):
    """Apertura: la busta paga con 2.000 € e le banconote che escono."""
    im, d = tela(w, h)
    W, H = w * SS, h * SS
    gradiente(im, (255, 240, 200), (255, 252, 240))
    d = ImageDraw.Draw(im, 'RGBA')
    x0, y0, x1, y1 = W * 0.10, H * 0.30, W * 0.90, H * 0.78
    for i in range(6):
        f = min(1, max(0, t * 1.2 - i * 0.12))
        banconota(d, W * (0.25 + 0.1 * i), y0 - f * H * 0.18 + 40 * SS, 80 * SS, ang=-20 + 8 * i)
    d.rectangle((x0, y0, x1, y1), fill=(250, 244, 230, 255), outline=LINEA, width=8 * SS)
    d.polygon([(x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2), (x1, y0)], fill=(236, 226, 206, 255), outline=LINEA, width=6 * SS)
    k = 1 + 0.06 * max(0, math.sin(t * 5))
    f = font(int(150 * k))
    tw = d.textlength('2.000 €', font=f)
    d.text(((W - tw) / 2, H * 0.58), '2.000 €', font=f, fill=ROSSO, stroke_width=6 * SS, stroke_fill=(255, 255, 255, 255))
    etichetta(d, W, H, 'busta paga', y=0.86, col=SCURO, dim=52)
    return fine(im, w, h)


def quindici(p, t, w, h):
    """Dopo 15 giorni è già finito: la barra dei soldi che si svuota giorno per giorno."""
    im, d = tela(w, h, (250, 246, 236, 255))
    W, H = w * SS, h * SS
    giorno = min(15, 1 + int(t * 7))
    f, g = font(74), font(46)
    tw = d.textlength(f'giorno {giorno}', font=f)
    d.text(((W - tw) / 2, H * 0.08), f'giorno {giorno}', font=f, fill=SCURO)
    # griglia del calendario
    for n in range(1, 31):
        c, r = (n - 1) % 7, (n - 1) // 7
        cx = W * (0.12 + 0.127 * c); cy = H * (0.24 + 0.085 * r)
        col = ROSSO if n <= giorno else (200, 192, 182, 255)
        d.rounded_rectangle((cx - 36 * SS, cy - 30 * SS, cx + 36 * SS, cy + 30 * SS), radius=10 * SS, fill=col if n <= giorno else CREMA, outline=LINEA, width=3 * SS)
        tw = d.textlength(str(n), font=font(30))
        d.text((cx - tw / 2, cy - 18 * SS), str(n), font=font(30), fill=CREMA if n <= giorno else SCURO)
    resto = max(0, 2000 - giorno * 2000 / 15)
    bx0, bx1, by = W * 0.10, W * 0.90, H * 0.74
    d.rounded_rectangle((bx0, by, bx1, by + 90 * SS), radius=20 * SS, fill=(226, 220, 210, 255), outline=LINEA, width=5 * SS)
    d.rounded_rectangle((bx0, by, bx0 + (bx1 - bx0) * resto / 2000 + 1, by + 90 * SS), radius=20 * SS, fill=C20 if resto > 600 else ROSSO)
    testo = f'{int(round(resto, -1))} €'
    tw = d.textlength(testo, font=g)
    d.text(((W - tw) / 2, by + 104 * SS), testo, font=g, fill=SCURO)
    return fine(im, w, h)


def portafoglio(p, t, w, h):
    """Dove sono andati? Il portafoglio aperto e le banconote che volano via."""
    im, d = tela(w, h, (236, 240, 250, 255))
    W, H = w * SS, h * SS
    cx, cy = W * 0.5, H * 0.66
    d.rounded_rectangle((cx - 260 * SS, cy - 150 * SS, cx + 260 * SS, cy + 150 * SS), radius=40 * SS, fill=SAIO, outline=LINEA, width=8 * SS)
    d.rounded_rectangle((cx - 220 * SS, cy - 190 * SS, cx + 220 * SS, cy - 110 * SS), radius=20 * SS, fill=(140, 100, 70, 255), outline=LINEA, width=6 * SS)
    for i in range(7):
        f = (t * 0.6 + i / 7) % 1
        x = cx + (i - 3) * 70 * SS + f * 140 * SS * math.sin(i * 2)
        y = cy - 200 * SS - f * H * 0.48
        banconota(d, x, y, 60 * SS, ang=f * 220 + i * 30)
    q = font(int(150 * (1 + 0.05 * math.sin(t * 4))))
    tw = d.textlength('?', font=q)
    d.text((W * 0.82 - tw / 2, H * 0.10), '?', font=q, fill=ROSSO, stroke_width=6 * SS, stroke_fill=(255, 255, 255, 255))
    etichetta(d, W, H, 'dove sono finiti?', y=0.88, col=SCURO, dim=52)
    return fine(im, w, h)


def regola(p, t, w, h):
    """Il titolo della regola: tre blocchi 50 · 30 · 20."""
    im, d = tela(w, h, (250, 246, 236, 255))
    W, H = w * SS, h * SS
    f = font(170)
    for i, (n, col) in enumerate(((50, C50), (30, C30), (20, C20))):
        k = min(1, max(0, (t - i * 0.25) / 0.3))
        if k <= 0: continue
        y = H * (0.12 + 0.26 * i) + (1 - k) * 80 * SS
        d.rounded_rectangle((W * 0.12, y, W * 0.88, y + H * 0.22), radius=40 * SS, fill=col, outline=LINEA, width=8 * SS)
        testo = f'{n}%'
        tw = d.textlength(testo, font=f)
        d.text(((W - tw) / 2, y + H * 0.03), testo, font=f, fill=CREMA, stroke_width=5 * SS, stroke_fill=LINEA)
    return fine(im, w, h)


def torta(p, t, w, h, fette=3):
    """Grafico a torta in proporzioni vere: 50% necessità, 30% desideri, 20% risparmio."""
    im, d = tela(w, h, (250, 246, 236, 255))
    W, H = w * SS, h * SS
    cx, cy, r = W * 0.5, H * 0.40, W * 0.36
    voci = [(50, C50, 'necessità', '1.000 €'), (30, C30, 'desideri', '600 €'), (20, C20, 'risparmio', '400 €')]
    a0 = -90
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(226, 220, 210, 255), outline=LINEA, width=6 * SS)
    for i, (pc, col, nome, euro) in enumerate(voci):
        a1 = a0 + pc * 3.6
        if i < fette:
            k = min(1, t / 0.5) if i == fette - 1 else 1
            d.pieslice((cx - r, cy - r, cx + r, cy + r), a0, a0 + (a1 - a0) * k, fill=col, outline=LINEA, width=6 * SS)
            if k >= 1:
                am = math.radians((a0 + a1) / 2)
                tx, ty = cx + math.cos(am) * r * 0.58, cy + math.sin(am) * r * 0.58
                g = font(66)
                tw = d.textlength(f'{pc}%', font=g)
                d.text((tx - tw / 2, ty - 40 * SS), f'{pc}%', font=g, fill=CREMA, stroke_width=4 * SS, stroke_fill=LINEA)
        a0 = a1
    # legenda con gli importi su 2.000 €
    g, h2 = font(46), font(54)
    for i, (pc, col, nome, euro) in enumerate(voci):
        if i >= fette: break
        y = H * (0.80 + 0.065 * i) - (0.065 * H * (fette - 1)) * 0.5
        d.rounded_rectangle((W * 0.10, y, W * 0.10 + 50 * SS, y + 50 * SS), radius=10 * SS, fill=col, outline=LINEA, width=3 * SS)
        d.text((W * 0.10 + 70 * SS, y - 2 * SS), nome, font=g, fill=SCURO)
        tw = d.textlength(euro, font=h2)
        d.text((W * 0.90 - tw, y - 8 * SS), euro, font=h2, fill=col[:3] + (255,), stroke_width=2 * SS, stroke_fill=LINEA)
    return fine(im, w, h)


def icone(d, W, H, tipo, t):
    if tipo == 'casa':
        d.rectangle((-90, -20, 90, 110), fill=CREMA, outline=LINEA, width=6)
        d.polygon([(-120, -10), (0, -110), (120, -10)], fill=ROSSO, outline=LINEA, width=6)
        d.rectangle((-25, 40, 25, 110), fill=SAIO, outline=LINEA, width=4)
    elif tipo == 'lampadina':
        d.ellipse((-70, -110, 70, 30), fill=ORO, outline=LINEA, width=6)
        d.rounded_rectangle((-35, 20, 35, 80), radius=8, fill=(196, 204, 214, 255), outline=LINEA, width=5)
    elif tipo == 'carrello':
        d.polygon([(-110, -70), (100, -70), (80, 30), (-80, 30)], fill=(196, 204, 214, 255), outline=LINEA, width=6)
        for x in (-60, 60):
            d.ellipse((x - 22, 50, x + 22, 94), fill=LINEA)
    elif tipo == 'bus':
        d.rounded_rectangle((-120, -80, 120, 60), radius=20, fill=ORO, outline=LINEA, width=6)
        d.rectangle((-100, -60, 100, -10), fill=(190, 226, 250, 255), outline=LINEA, width=4)
        for x in (-70, 70):
            d.ellipse((x - 24, 44, x + 24, 92), fill=LINEA)
    elif tipo == 'pizza':
        d.pieslice((-110, -110, 110, 110), 200, 340, fill=(240, 200, 110, 255), outline=LINEA, width=6)
        for x, y in ((-30, -70), (20, -85), (0, -50)):
            d.ellipse((x - 14, y - 14, x + 14, y + 14), fill=ROSSO)
    elif tipo == 'maglia':
        d.polygon([(-100, -70), (-40, -100), (40, -100), (100, -70), (80, -30), (55, -45), (55, 90), (-55, 90), (-55, -45), (-80, -30)], fill=(140, 90, 190, 255), outline=LINEA, width=6)
    elif tipo == 'joystick':
        d.rounded_rectangle((-120, -50, 120, 60), radius=50, fill=(60, 60, 70, 255), outline=LINEA, width=6)
        d.line((-75, 5, -35, 5), fill=CREMA, width=10); d.line((-55, -15, -55, 25), fill=CREMA, width=10)
        for x, y in ((50, -10), (80, 15)):
            d.ellipse((x - 14, y - 14, x + 14, y + 14), fill=ROSSO)
    elif tipo == 'biglietto':
        d.rounded_rectangle((-110, -60, 110, 60), radius=14, fill=(255, 220, 120, 255), outline=LINEA, width=6)
        d.line((40, -60, 40, 60), fill=LINEA, width=4)


def gruppo(p, t, w, h, titolo, euro, col, voci):
    im, d = tela(w, h, (250, 246, 236, 255))
    W, H = w * SS, h * SS
    d.rounded_rectangle((W * 0.08, H * 0.05, W * 0.92, H * 0.22), radius=40 * SS, fill=col, outline=LINEA, width=7 * SS)
    f = font(80)
    tw = d.textlength(euro, font=f)
    d.text(((W - tw) / 2, H * 0.08), euro, font=f, fill=CREMA, stroke_width=4 * SS, stroke_fill=LINEA)
    for i, (tipo, nome) in enumerate(voci):
        k = min(1, max(0, (t - i * 0.3) / 0.3))
        if k <= 0: continue
        c, r = i % 2, i // 2
        cx, cy = W * (0.30 + 0.40 * c), H * (0.40 + 0.28 * r)
        s = SS * 0.95 * (0.6 + 0.4 * k)
        lay = Image.new('RGBA', (int(300 * SS), int(300 * SS)), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        tmp = Image.new('RGBA', (300, 300), (0, 0, 0, 0)); td = ImageDraw.Draw(tmp)
        td_draw = ImageDraw.Draw(tmp)
        class Sp:   # disegno delle icone centrato su (150, 150)
            def __getattr__(self, n):
                fn = getattr(td_draw, n)
                def g(xy, *a, **k):
                    if isinstance(xy, (list, tuple)) and xy and isinstance(xy[0], (list, tuple)):
                        xy = [(x + 150, y + 150) for x, y in xy]
                    else:
                        xy = tuple(v + 150 for v in xy)
                    return fn(xy, *a, **k)
                return g
        icone(Sp(), W, H, tipo, t)
        tmp = tmp.resize((int(300 * s), int(300 * s)), Image.LANCZOS)
        im.paste(tmp, (int(cx - tmp.width / 2), int(cy - tmp.height / 2 - 30 * SS)), tmp)
        g = font(44)
        tw = d.textlength(nome, font=g)
        d.text((cx - tw / 2, cy + 110 * SS), nome, font=g, fill=SCURO)
    etichetta(d, W, H, titolo, y=0.90, col=SCURO, dim=52)
    return fine(im, w, h)


def necessita(p, t, w, h):
    return gruppo(p, t, w, h, '50% · cose necessarie', '1.000 €', C50,
                  [('casa', 'affitto'), ('lampadina', 'bollette'), ('carrello', 'spesa'), ('bus', 'trasporti')])


def desideri(p, t, w, h):
    return gruppo(p, t, w, h, '30% · quello che ti piace', '600 €', C30,
                  [('pizza', 'uscite'), ('maglia', 'vestiti'), ('joystick', 'hobby'), ('biglietto', 'cinema')])


def salvadanaio(p, t, w, h):
    """Il 20%: il salvadanaio che si riempie di monete."""
    im, d = tela(w, h, (236, 246, 232, 255))
    W, H = w * SS, h * SS
    d.rounded_rectangle((W * 0.08, H * 0.05, W * 0.92, H * 0.22), radius=40 * SS, fill=C20, outline=LINEA, width=7 * SS)
    f = font(80)
    tw = d.textlength('400 €', font=f)
    d.text(((W - tw) / 2, H * 0.08), '400 €', font=f, fill=CREMA, stroke_width=4 * SS, stroke_fill=LINEA)
    cx, cy, rx, ry = W * 0.5, H * 0.58, 250 * SS, 190 * SS
    for i in range(5):
        fz = (t * 1.2 + i * 0.2) % 1
        moneta_oro(d, cx + (i - 2) * 30 * SS, H * 0.26 + fz * (cy - ry - H * 0.26), 40 * SS)
    d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=(244, 160, 170, 255), outline=LINEA, width=8 * SS)
    d.ellipse((cx + rx * 0.7, cy - 50 * SS, cx + rx * 1.1, cy + 50 * SS), fill=(244, 160, 170, 255), outline=LINEA, width=7 * SS)
    for ox in (-0.5, 0.4):
        d.rectangle((cx + rx * ox, cy + ry * 0.8, cx + rx * ox + 60 * SS, cy + ry * 1.25), fill=(244, 160, 170, 255), outline=LINEA, width=6 * SS)
    d.ellipse((cx + rx * 0.35, cy - 70 * SS, cx + rx * 0.45, cy - 40 * SS), fill=LINEA)
    d.rounded_rectangle((cx - 60 * SS, cy - ry - 6 * SS, cx + 60 * SS, cy - ry + 14 * SS), radius=8 * SS, fill=LINEA)
    etichetta(d, W, H, '20% · risparmi o debiti', y=0.88, col=SCURO, dim=50)
    return fine(im, w, h)


def subito(p, t, w, h):
    """Il trucco: appena arriva lo stipendio, il 20% va subito da parte."""
    im, d = tela(w, h, (250, 246, 236, 255))
    W, H = w * SS, h * SS
    f = font(70)
    d.text((W * 0.08, H * 0.08), 'arriva lo stipendio', font=font(56), fill=SCURO)
    d.rounded_rectangle((W * 0.08, H * 0.18, W * 0.92, H * 0.34), radius=30 * SS, fill=CREMA, outline=LINEA, width=6 * SS)
    tw = d.textlength('2.000 €', font=f)
    d.text(((W - tw) / 2, H * 0.21), '2.000 €', font=f, fill=SCURO)
    k = min(1, t / 0.8)
    y = H * 0.36 + k * H * 0.22
    d.line((W * 0.5, H * 0.36, W * 0.5, y), fill=C20, width=18 * SS)
    d.polygon([(W * 0.5 - 50 * SS, y), (W * 0.5 + 50 * SS, y), (W * 0.5, y + 60 * SS)], fill=C20, outline=LINEA, width=5 * SS)
    if k >= 1:
        d.rounded_rectangle((W * 0.20, H * 0.66, W * 0.80, H * 0.80), radius=30 * SS, fill=C20, outline=LINEA, width=7 * SS)
        tw = d.textlength('-400 € subito', font=font(62))
        d.text(((W - tw) / 2, H * 0.69), '-400 € subito', font=font(62), fill=CREMA, stroke_width=3 * SS, stroke_fill=LINEA)
    etichetta(d, W, H, 'prima il 20%, poi il resto', y=0.86, col=SCURO, dim=48)
    return fine(im, w, h)


def anno(p, t, w, h):
    """In un anno: 12 barre da 400 € che arrivano a 4.800 €."""
    im, d = tela(w, h, (250, 246, 236, 255))
    W, H = w * SS, h * SS
    mesi = min(12, 1 + int(t * 7))
    base, alt = H * 0.80, H * 0.55
    larg = W * 0.80 / 12
    for i in range(12):
        x = W * 0.10 + i * larg
        a = alt * (i + 1) / 12
        if i < mesi:
            d.rectangle((x + 6 * SS, base - a, x + larg - 6 * SS, base), fill=C20, outline=LINEA, width=3 * SS)
        tw = d.textlength('GFMAMGLASOND'[i], font=font(32))
        d.text((x + larg / 2 - tw / 2, base + 14 * SS), 'GFMAMGLASOND'[i], font=font(32), fill=SCURO)
    d.line((W * 0.08, base, W * 0.92, base), fill=LINEA, width=5 * SS)
    tot = mesi * 400
    testo = f'{tot:,} €'.replace(',', '.')
    f = font(110)
    tw = d.textlength(testo, font=f)
    d.text(((W - tw) / 2, H * 0.06), testo, font=f, fill=C20[:3] + (255,), stroke_width=5 * SS, stroke_fill=LINEA)
    etichetta(d, W, H, 'risparmiati in un anno', y=0.89, col=SCURO, dim=48)
    return fine(im, w, h)


SCENE = {'busta': busta, 'quindici': quindici, 'portafoglio': portafoglio, 'regola': regola, 'torta': torta,
         'necessita': necessita, 'desideri': desideri, 'salvadanaio': salvadanaio, 'subito': subito, 'anno': anno}

if __name__ == '__main__':
    S = sys.argv[1]
    nomi = list(SCENE)
    tav = Image.new('RGB', (5 * 310, 2 * 410), (90, 90, 90))
    for i, n in enumerate(nomi):
        im = SCENE[n](0.95, 2.4, 760, 1000).resize((300, 395))
        tav.paste(im, ((i % 5) * 310 + 5, (i // 5) * 410 + 5))
    tav.save(f'{S}/scene_stipendio.png')

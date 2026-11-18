"""Scene animate a tutto schermo per «Perché il cielo è azzurro?».

Ogni funzione disegna il fenomeno mentre la voce lo spiega: f(p, t, larg, alt) -> RGBA.
p = avanzamento della scena 0..1, t = secondi dall'inizio della scena.
Stile del Professore: contorno scuro spesso, colori pieni, palette calda.
"""
import math
from PIL import Image, ImageDraw, ImageFont

SS = 2
LINEA = (43, 33, 28, 255)
CREMA = (255, 250, 240, 255)
ORO = (240, 186, 70, 255)
SOLE = (255, 206, 84, 255)
ROSSO = (205, 62, 48, 255)
ARANCIO = (240, 132, 52, 255)
GIALLO = (248, 214, 72, 255)
VERDE = (96, 178, 104, 255)
BLU = (56, 120, 214, 255)
INDACO = (82, 74, 170, 255)
VIOLA = (140, 84, 180, 255)
CIELO_ALTO = (78, 150, 228)
CIELO_BASSO = (176, 220, 248)
SPETTRO = [ROSSO, ARANCIO, GIALLO, VERDE, BLU, INDACO, VIOLA]

F = '/usr/share/fonts/opentype/inter/'
def font(n): return ImageFont.truetype(F + 'InterDisplay-ExtraBold.otf', n * SS)


def tela(w, h, sfondo=(250, 246, 236, 255)):
    # tela opaca: cosi' le forme semitrasparenti si fondono con lo sfondo
    im = Image.new('RGB', (w * SS, h * SS), sfondo[:3])
    return im, ImageDraw.Draw(im, 'RGBA')


def fine(im, w, h):
    return im.resize((w, h), Image.LANCZOS)


def mix(a, b, k):
    return tuple(round(a[i] + (b[i] - a[i]) * k) for i in range(3))


def gradiente(im, alto, basso, y0=0, y1=None):
    d = ImageDraw.Draw(im, 'RGBA')
    y1 = im.height if y1 is None else y1
    for y in range(y0, y1, 2):
        k = (y - y0) / max(1, (y1 - y0))
        d.rectangle((0, y, im.width, y + 2), fill=mix(alto, basso, k) + (255,))


def sole(d, cx, cy, r, t, raggi=True):
    if raggi:
        for i in range(12):
            a = i * math.pi / 6 + t * 0.6
            l0, l1 = r * 1.25, r * (1.55 + 0.12 * math.sin(t * 4 + i))
            d.line((cx + math.cos(a) * l0, cy + math.sin(a) * l0, cx + math.cos(a) * l1, cy + math.sin(a) * l1),
                   fill=SOLE, width=int(10 * SS))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=SOLE, outline=LINEA, width=7 * SS)


def nuvola(d, x, y, s):
    for col, extra in ((LINEA, 0), (CREMA, -7 * SS)):
        for cx, cy, r in [(0, 0, 1.0), (-0.9, 0.25, 0.7), (0.95, 0.2, 0.75), (0.3, -0.45, 0.75)]:
            rr = r * s + extra
            d.ellipse((x + cx * s - rr, y + cy * s - rr, x + cx * s + rr, y + cy * s + rr), fill=col)


# ------------------------------------------------------------------ 1. apertura
def gancio(p, t, w, h, punto=(0.5, 0.16)):
    """Il cielo che si accende di blu dietro un grande punto di domanda."""
    im, d = tela(w, h)
    W, H = w * SS, h * SS
    k = min(1, t / 1.2)
    gradiente(im, mix((250, 246, 236), CIELO_ALTO, k), mix((250, 246, 236), CIELO_BASSO, k))
    d = ImageDraw.Draw(im, 'RGBA')
    sole(d, W * 0.78, H * 0.20, 95 * SS, t)
    for i, (x, y, s) in enumerate([(0.22, 0.30, 70), (0.62, 0.52, 55), (0.30, 0.70, 60)]):
        nuvola(d, W * x + 40 * SS * math.sin(t * 0.7 + i), H * y, s * SS)
    # punto di domanda che rimbalza dentro
    salto = max(0, 1 - t / 0.5)
    q = font(int(640 * (1 + 0.25 * salto)))
    tw = d.textlength('?', font=q)
    d.text((W * punto[0] - tw / 2 + 8 * SS, H * punto[1] - salto * 40 * SS + 8 * SS), '?', font=q, fill=(30, 40, 80, 120))
    d.text((W * punto[0] - tw / 2, H * punto[1] - salto * 40 * SS), '?', font=q, fill=CREMA, stroke_width=9 * SS, stroke_fill=LINEA)
    return fine(im, w, h)


# ------------------------------------------------------------------ 2. prisma
def prisma(p, t, w, h, apri=0.45):
    """Raggio bianco che entra nel prisma; dalla parola «contiene» esce l'arcobaleno."""
    im, d = tela(w, h, (34, 38, 64, 255))
    W, H = w * SS, h * SS
    cx, cy, s = W * 0.50, H * 0.52, 230 * SS
    tri = [(cx, cy - s), (cx - s * 0.9, cy + s * 0.65), (cx + s * 0.9, cy + s * 0.65)]
    # raggio bianco che avanza
    ing = min(1, t / 0.6)
    xa, ya = 0, H * 0.62
    xb, yb = cx - s * 0.45, cy + s * 0.05
    d.line((xa, ya, xa + (xb - xa) * ing, ya + (yb - ya) * ing), fill=(255, 255, 255, 255), width=26 * SS)
    # arcobaleno
    k = min(1, max(0, (p - apri) / 0.35))
    if k > 0:
        x0, y0 = cx + s * 0.42, cy + s * 0.02
        for i, col in enumerate(SPETTRO):
            ang = math.radians(-16 + i * 6.5)
            l = W * 0.62 * k
            x1, y1 = x0 + math.cos(ang) * l, y0 + math.sin(ang) * l
            d.line((x0, y0 + (i - 3) * 6 * SS, x1, y1), fill=col, width=24 * SS)
    d.polygon(tri, fill=(200, 230, 255, 150), outline=LINEA, width=8 * SS)
    d.line((tri[0][0] - s * 0.15, tri[0][1] + s * 0.4, tri[0][0] - s * 0.4, tri[0][1] + s * 1.0), fill=(255, 255, 255, 150), width=10 * SS)
    etich = 'luce bianca' if k == 0 else 'tutti i colori!'
    f = font(56)
    tw = d.textlength(etich, font=f)
    d.text(((W - tw) / 2, H * 0.10), etich, font=f, fill=CREMA, stroke_width=4 * SS, stroke_fill=LINEA)
    return fine(im, w, h)


# ------------------------------------------------------------------ 3. molecole
def onda(d, x0, y0, x1, lam, amp, fase, col, larg):
    pts = []
    n = max(2, int((x1 - x0) / (6 * SS)))
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        pts.append((x, y0 + amp * math.sin((x - x0) / lam * 2 * math.pi - fase)))
    d.line(pts, fill=col, width=larg, joint='curve')


def molecole(p, t, w, h, intensita=1.0):
    """Le onde di luce entrano nell'aria: il rosso passa dritto, il blu rimbalza ovunque."""
    im, d = tela(w, h)
    W, H = w * SS, h * SS
    gradiente(im, (226, 240, 252), (248, 250, 255))
    d = ImageDraw.Draw(im, 'RGBA')
    # molecole d'aria
    mol = [(0.30, 0.30), (0.55, 0.22), (0.78, 0.36), (0.40, 0.55), (0.66, 0.62), (0.86, 0.70), (0.25, 0.78), (0.52, 0.84)]
    # onda rossa: dritta
    avanz = min(1, t / 0.8)
    onda(d, 0, H * 0.48, W * avanz, 150 * SS, 26 * SS, t * 6, ROSSO, 10 * SS)
    # onda blu fino alla prima molecola, poi sparpagliata
    bx = W * 0.40
    onda(d, 0, H * 0.55, min(bx, W * avanz), 48 * SS, 22 * SS, t * 9, BLU, 10 * SS)
    for i, (mx, my) in enumerate(mol):
        x, y = W * mx, H * my
        r = 34 * SS * (1 + 0.08 * math.sin(t * 5 + i))
        d.ellipse((x - r, y - r, x + r, y + r), fill=(208, 214, 230, 255), outline=LINEA, width=6 * SS)
        d.ellipse((x - r * 0.35, y - r * 0.5, x + r * 0.05, y - r * 0.1), fill=(255, 255, 255, 255))
        if avanz >= 1 and intensita > 0:
            # schegge blu in tutte le direzioni
            for k in range(5):
                a = k * 2 * math.pi / 5 + i + t * 0.8
                f = ((t * 1.4 + k * 0.2 + i * 0.13) % 1)
                l0, l1 = r * 1.3 + f * 90 * SS, r * 1.3 + f * 90 * SS + 40 * SS
                c = BLU[:3] + (int(255 * (1 - f) * intensita),)
                d.line((x + math.cos(a) * l0, y + math.sin(a) * l0, x + math.cos(a) * l1, y + math.sin(a) * l1), fill=c, width=9 * SS)
    f = font(48)
    d.text((W * 0.05, H * 0.06), 'aria', font=f, fill=LINEA)
    return fine(im, w, h)


# ------------------------------------------------------------------ 4. schema onde
def schema_onde(p, t, w, h):
    """Schema: onda blu corta e fitta contro onda rossa lunga."""
    im, d = tela(w, h, (255, 252, 246, 255))
    W, H = w * SS, h * SS
    d.rounded_rectangle((30 * SS, 30 * SS, W - 30 * SS, H - 30 * SS), radius=50 * SS, outline=LINEA, width=7 * SS)
    k = min(1, t / 0.7)
    x0, x1 = W * 0.10, W * 0.10 + (W * 0.80) * k
    onda(d, x0, H * 0.33, x1, 60 * SS, 50 * SS, t * 5, BLU, 14 * SS)
    onda(d, x0, H * 0.74, x1, 220 * SS, 50 * SS, t * 5, ROSSO, 14 * SS)
    f, g = font(64), font(38)
    d.text((W * 0.10, H * 0.10), 'BLU', font=f, fill=BLU)
    d.text((W * 0.10, H * 0.17), 'onde corte: si sparpaglia', font=g, fill=LINEA)
    d.text((W * 0.10, H * 0.48), 'ROSSO', font=f, fill=ROSSO)
    d.text((W * 0.10, H * 0.55), 'onde lunghe: passa dritto', font=g, fill=LINEA)
    # misura della lunghezza d'onda sul blu
    if k >= 1:
        y = H * 0.44
        d.line((x0, y, x0 + 60 * SS * 2, y), fill=LINEA, width=5 * SS)
        for xx in (x0, x0 + 120 * SS):
            d.line((xx, y - 16 * SS, xx, y + 16 * SS), fill=LINEA, width=5 * SS)
    return fine(im, w, h)


# ------------------------------------------------------------------ 5. occhio sotto il cielo
def occhi_cielo(p, t, w, h, bersaglio=None):
    """Il blu arriva da ogni punto del cielo fino agli occhi di chi guarda."""
    im, d = tela(w, h)
    W, H = w * SS, h * SS
    gradiente(im, CIELO_ALTO, CIELO_BASSO, 0, int(H * 0.78))
    d = ImageDraw.Draw(im, 'RGBA')
    d.rectangle((0, H * 0.78, W, H), fill=(126, 186, 104, 255))
    d.line((0, H * 0.78, W, H * 0.78), fill=LINEA, width=7 * SS)
    if bersaglio:   # le frecce arrivano agli occhi del Professore, che sta davanti alla scena
        ox, oy = W * bersaglio[0], H * bersaglio[1] + 60 * SS
    else:
        ox, oy = W * 0.5, H * 0.74
        # omino stilizzato che guarda in alto
        d.ellipse((ox - 46 * SS, oy - 92 * SS, ox + 46 * SS, oy), fill=(252, 186, 122, 255), outline=LINEA, width=6 * SS)
        d.ellipse((ox - 18 * SS, oy - 70 * SS, ox - 4 * SS, oy - 56 * SS), fill=LINEA)
        d.ellipse((ox + 8 * SS, oy - 70 * SS, ox + 22 * SS, oy - 56 * SS), fill=LINEA)
        d.rounded_rectangle((ox - 60 * SS, oy, ox + 60 * SS, oy + 120 * SS), radius=30 * SS, fill=(138, 47, 39, 255), outline=LINEA, width=6 * SS)
    # frecce blu che convergono
    for i in range(9):
        a = math.radians((200 + i * 17.5) if not bersaglio else (215 + i * 13))
        f = (t * 0.9 + i * 0.11) % 1
        r0 = W * 0.62 * (1 - f) + 130 * SS
        x, y = ox + math.cos(a) * r0, oy - 60 * SS + math.sin(a) * r0
        dx, dy = -math.cos(a), -math.sin(a)
        l = 70 * SS
        c = BLU[:3] + (int(255 * min(1, 3 * (1 - f))),)
        d.line((x, y, x + dx * l, y + dy * l), fill=c, width=12 * SS)
        hx, hy = x + dx * l, y + dy * l
        d.polygon([(hx + dx * 26 * SS, hy + dy * 26 * SS), (hx - dy * 18 * SS, hy + dx * 18 * SS), (hx + dy * 18 * SS, hy - dx * 18 * SS)], fill=c)
    return fine(im, w, h)


# ------------------------------------------------------------------ 6. tramonto
def tramonto(p, t, w, h, colore_da=0.45):
    """La Terra con la sua atmosfera: a mezzogiorno il percorso è corto, al tramonto lunghissimo."""
    im, d = tela(w, h)
    W, H = w * SS, h * SS
    k = min(1, max(0, (p - colore_da) / 0.4))
    gradiente(im, mix((70, 120, 200), (90, 60, 120), k), mix((180, 220, 250), (250, 150, 80), k))
    d = ImageDraw.Draw(im, 'RGBA')
    # Terra e atmosfera
    cx, cy, R = W * 0.5, H * 1.35, H * 0.85
    A = R + 120 * SS
    d.ellipse((cx - A, cy - A, cx + A, cy + A), fill=(170, 210, 245, 120))
    d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=(96, 160, 110, 255), outline=LINEA, width=8 * SS)
    osservatore = (cx, cy - R)
    d.ellipse((osservatore[0] - 16 * SS, osservatore[1] - 16 * SS, osservatore[0] + 16 * SS, osservatore[1] + 16 * SS), fill=LINEA)
    # mezzogiorno: raggio corto dall'alto
    d.line((osservatore[0], osservatore[1] - 120 * SS, osservatore[0], osservatore[1]), fill=(255, 255, 255, int(255 * (1 - k * 0.6))), width=12 * SS)
    # tramonto: raggio radente lunghissimo che perde il blu
    sx, sy = W * 0.02, H * 0.40
    sole(d, sx + 60 * SS, sy - 70 * SS + k * 40 * SS, 55 * SS, t, raggi=False)
    lung = min(1, t / 0.9)
    ex, ey = osservatore[0] + (sx - osservatore[0]) * (1 - lung), osservatore[1] + (sy - osservatore[1]) * (1 - lung)
    d.line((sx, sy, ex, ey), fill=ARANCIO, width=16 * SS)
    # il blu che scappa lungo la strada
    for i in range(6):
        f = (t * 1.1 + i / 6) % 1
        px, py = sx + (osservatore[0] - sx) * (i + 0.5) / 6, sy + (osservatore[1] - sy) * (i + 0.5) / 6
        d.line((px, py, px + 20 * SS, py - 40 * SS - f * 60 * SS), fill=BLU[:3] + (int(230 * (1 - f)),), width=8 * SS)
    f = font(46)
    for i, r in enumerate(['più atmosfera', 'da attraversare']):
        tw = d.textlength(r, font=f)
        d.text((W - tw - W * 0.06, H * (0.08 + 0.07 * i)), r, font=f, fill=CREMA, stroke_width=4 * SS, stroke_fill=LINEA)
    return fine(im, w, h)


SCENE = {'gancio': gancio, 'prisma': prisma, 'molecole': molecole, 'schema_onde': schema_onde,
         'occhi_cielo': occhi_cielo, 'tramonto': tramonto}

if __name__ == '__main__':
    import sys
    S = sys.argv[1]
    tav = Image.new('RGB', (3 * 540, 2 * 560), (90, 90, 90))
    prove = [('gancio', 0.5, 1.5), ('prisma', 0.9, 2.0), ('molecole', 0.6, 2.0), ('schema_onde', 0.6, 1.5),
             ('occhi_cielo', 0.5, 1.2), ('tramonto', 0.9, 2.0)]
    for i, (n, p, t) in enumerate(prove):
        im = SCENE[n](p, t, 520, 540)
        tav.paste(im, ((i % 3) * 540 + 10, (i // 3) * 560 + 10), im)
    tav.save(f'{S}/scene_cielo.png')

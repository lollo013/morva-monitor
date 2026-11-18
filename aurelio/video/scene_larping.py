"""Illustrazioni originali per «Il paradosso del larping». f(p, t, w, h, **extra) -> immagine RGB."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from scene_cielo import tela, fine, font, mix, gradiente, LINEA, CREMA, ORO, ROSSO, ARANCIO, BLU, SS
from scene_inception import etichetta, NOTTE, NOTTE2, ACCIAIO, SAIO, VERDE
from scene_scuola import omino

VIOLA = (130, 90, 190, 255)
AZZ = (120, 178, 228, 255)


def maschera(d, cx, cy, s, felice, col):
    d.ellipse((cx - s, cy - s * 1.1, cx + s, cy + s * 1.1), fill=col, outline=LINEA, width=7 * SS)
    for ox in (-0.4, 0.4):
        d.ellipse((cx + ox * s - s * 0.2, cy - s * 0.35, cx + ox * s + s * 0.2, cy - s * 0.05), fill=LINEA)
    if felice:
        d.arc((cx - s * 0.55, cy - s * 0.1, cx + s * 0.55, cy + s * 0.7), 20, 160, fill=LINEA, width=9 * SS)
    else:
        d.arc((cx - s * 0.55, cy + s * 0.35, cx + s * 0.55, cy + s * 1.0), 200, 340, fill=LINEA, width=9 * SS)


def l_gancio(p, t, w, h):
    """Apertura: due maschere teatrali che si scambiano davanti a un sipario."""
    im, d = tela(w, h)
    W, H = w * SS, h * SS
    gradiente(im, (120, 24, 34), (70, 10, 20))
    d = ImageDraw.Draw(im, 'RGBA')
    for i in range(8):
        x = W * i / 8
        d.rectangle((x, 0, x + W / 16, H), fill=(150, 34, 44, 255))
    d.rectangle((0, H * 0.84, W, H), fill=(90, 60, 40, 255))
    a = t * 2.2
    maschera(d, W * 0.62 + math.cos(a) * 110 * SS, H * 0.50 + math.sin(a) * 50 * SS, 120 * SS, True, ORO)
    maschera(d, W * 0.62 - math.cos(a) * 110 * SS, H * 0.50 - math.sin(a) * 50 * SS, 120 * SS, False, CREMA)
    return fine(im, w, h)


def sigla(p, t, w, h):
    """L-A-R-P: le lettere si aprono nelle parole, poi la traduzione."""
    im, d = tela(w, h, (250, 244, 232, 255))
    W, H = w * SS, h * SS
    parole = [('L', 'Live'), ('A', 'Action'), ('R', 'Role'), ('P', 'Playing')]
    f, g = font(120), font(60)
    for i, (lettera, parola) in enumerate(parole):
        y = H * (0.10 + 0.17 * i)
        k = min(1, max(0, (t - 0.35 * i) / 0.3))
        d.rounded_rectangle((W * 0.08, y, W * 0.08 + 150 * SS, y + 150 * SS), radius=24 * SS, fill=[ROSSO, BLU, VERDE, VIOLA][i], outline=LINEA, width=6 * SS)
        tw = d.textlength(lettera, font=f)
        d.text((W * 0.08 + 75 * SS - tw / 2, y + 8 * SS), lettera, font=f, fill=CREMA)
        if k > 0:
            d.text((W * 0.08 + 190 * SS - (1 - k) * 60 * SS, y + 40 * SS), parola, font=g, fill=LINEA)
    if t > 1.7:
        etichetta(d, W, H, 'gioco di ruolo dal vivo', y=0.80, col=ROSSO, dim=58)
    return fine(im, w, h)


def cavalieri(p, t, w, h):
    """Gli appassionati in costume: un cavaliere e un mago in un prato."""
    im, d = tela(w, h)
    W, H = w * SS, h * SS
    gradiente(im, (150, 206, 240), (232, 246, 252))
    d = ImageDraw.Draw(im, 'RGBA')
    d.rectangle((0, H * 0.70, W, H), fill=(120, 186, 104, 255))
    # cavaliere con spada di legno
    ang = math.radians(-40 + 30 * math.sin(t * 3))
    cx, base = W * 0.32, H * 0.84
    omino(d, cx, base, 260 * SS, (150, 156, 170, 255))
    sx, sy = cx + 80 * SS, base - 300 * SS
    d.line((sx, sy, sx + math.cos(ang) * 260 * SS, sy + math.sin(ang) * 260 * SS), fill=(170, 120, 70, 255), width=18 * SS)
    d.rounded_rectangle((cx - 130 * SS, base - 300 * SS, cx - 40 * SS, base - 150 * SS), radius=20 * SS, fill=ROSSO, outline=LINEA, width=6 * SS)
    # mago con cappello a punta
    mx = W * 0.72
    omino(d, mx, base, 250 * SS, VIOLA)
    d.polygon([(mx - 90 * SS, base - 430 * SS), (mx + 90 * SS, base - 430 * SS), (mx + 20 * SS, base - 650 * SS)], fill=VIOLA, outline=LINEA, width=6 * SS)
    for i in range(4):
        a = t * 3 + i * 1.6
        x, y = mx + 120 * SS + math.cos(a) * 70 * SS, base - 300 * SS + math.sin(a) * 70 * SS
        d.ellipse((x - 12 * SS, y - 12 * SS, x + 12 * SS, y + 12 * SS), fill=ORO)
    etichetta(d, W, H, 'dalla fine degli anni \'70', y=0.06, col=(43, 33, 28, 255), dim=52)
    return fine(im, w, h)


def finto(p, t, w, h):
    """Su internet: un profilo «da ricco» con il timbro FINTO."""
    im, d = tela(w, h, (232, 240, 252, 255))
    W, H = w * SS, h * SS
    x0, y0, x1, y1 = W * 0.12, H * 0.06, W * 0.88, H * 0.92
    d.rounded_rectangle((x0, y0, x1, y1), radius=70 * SS, fill=(40, 40, 46, 255), outline=LINEA, width=8 * SS)
    d.rounded_rectangle((x0 + 22 * SS, y0 + 60 * SS, x1 - 22 * SS, y1 - 40 * SS), radius=40 * SS, fill=CREMA)
    # «foto» con auto sportiva e orologio
    d.rounded_rectangle((x0 + 60 * SS, y0 + 120 * SS, x1 - 60 * SS, H * 0.52), radius=24 * SS, fill=(255, 226, 150, 255), outline=LINEA, width=5 * SS)
    cx, cy = (x0 + x1) / 2, H * 0.40
    d.rounded_rectangle((cx - 220 * SS, cy - 50 * SS, cx + 220 * SS, cy + 50 * SS), radius=40 * SS, fill=ROSSO, outline=LINEA, width=6 * SS)
    d.polygon([(cx - 120 * SS, cy - 50 * SS), (cx - 60 * SS, cy - 120 * SS), (cx + 90 * SS, cy - 120 * SS), (cx + 150 * SS, cy - 50 * SS)], fill=ROSSO, outline=LINEA, width=6 * SS)
    for ox in (-140, 140):
        d.ellipse((cx + ox * SS - 45 * SS, cy + 20 * SS, cx + ox * SS + 45 * SS, cy + 110 * SS), fill=LINEA)
    g = font(44)
    for i, r in enumerate(['vita da ricco', 'esperto di tutto', 'sempre sicuro']):
        d.text((x0 + 70 * SS, H * (0.57 + 0.08 * i)), r, font=g, fill=LINEA)
    if t > 0.9:
        k = min(1, (t - 0.9) / 0.2)
        s = font(int(150 * (1.6 - 0.6 * k)))
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        tw = ld.textlength('FINTO', font=s)
        ld.text(((W - tw) / 2, H * 0.36), 'FINTO', font=s, fill=(205, 62, 48, 230), stroke_width=6 * SS, stroke_fill=(255, 255, 255, 230))
        lay = lay.rotate(-14, resample=Image.BICUBIC, center=(W / 2, H * 0.45))
        im.paste(lay, (0, 0), lay)
    return fine(im, w, h)


def scala(p, t, w, h, passo=0.0, gradino=-1):
    """Il paradosso: fingo di averlo, lo voglio, ce l'ho. Tre gradini che si accendono."""
    im, d = tela(w, h, (250, 244, 232, 255))
    W, H = w * SS, h * SS
    voci = ['fingo di averlo', 'lo voglio', "ce l'ho!"]
    cols = [(240, 200, 120, 255), (240, 160, 80, 255), (96, 178, 104, 255)]
    livello = min(2, int(max(0, p - passo) * 3.2)) if p >= passo else -1
    if gradino >= 0:   # un gradino per inquadratura, seguendo la voce
        livello = gradino
    g = font(52)
    for i in range(3):
        x0 = W * (0.06 + 0.30 * i); x1 = x0 + W * 0.30
        y0 = H * (0.70 - 0.20 * i)
        acceso = i <= livello
        d.rectangle((x0, y0, x1, H * 0.92), fill=cols[i] if acceso else (226, 220, 210, 255), outline=LINEA, width=6 * SS)
        tw = d.textlength(voci[i], font=g)
        if tw > x1 - x0 - 20 * SS:
            parti = voci[i].split(' ', 1)
            for k, r in enumerate(parti):
                tw2 = d.textlength(r, font=g)
                d.text(((x0 + x1) / 2 - tw2 / 2, y0 + 30 * SS + k * 64 * SS), r, font=g, fill=LINEA)
        else:
            d.text(((x0 + x1) / 2 - tw / 2, y0 + 30 * SS), voci[i], font=g, fill=LINEA)
    if livello >= 0:
        i = livello
        x = W * (0.06 + 0.30 * i + 0.15); base = H * (0.70 - 0.20 * i) - 4 * SS + 10 * SS * abs(math.sin(t * 6))
        omino(d, x, base, 180 * SS, BLU)
        if i == 2:
            st = font(int(120 * (1 + 0.1 * math.sin(t * 6))))
            tw = d.textlength('★', font=st) if False else 0
            r = 60 * SS
            sx, sy = x, base - 420 * SS
            pts = [(sx + (r if j % 2 == 0 else r * 0.45) * math.cos(-math.pi / 2 + j * math.pi / 5), sy + (r if j % 2 == 0 else r * 0.45) * math.sin(-math.pi / 2 + j * math.pi / 5)) for j in range(10)]
            d.polygon(pts, fill=ORO, outline=LINEA, width=5 * SS)
    return fine(im, w, h)


def specchio(p, t, w, h):
    """Guardando come ci comportiamo, capiamo chi siamo: il riflesso diventa sicuro."""
    im, d = tela(w, h, (236, 232, 246, 255))
    W, H = w * SS, h * SS
    d.ellipse((W * 0.46, H * 0.10, W * 0.94, H * 0.78), fill=(210, 230, 246, 255), outline=SAIO, width=18 * SS)
    k = min(1, t / 1.4)
    omino(d, W * 0.25, H * 0.82, 280 * SS, AZZ)
    col = mix((120, 178, 228), (96, 178, 104), k) + (255,)
    omino(d, W * 0.70, H * 0.70, 250 * SS * (1 + 0.12 * k), col)
    if k >= 1:
        r = 50 * SS; sx, sy = W * 0.70, H * 0.20
        pts = [(sx + (r if j % 2 == 0 else r * 0.45) * math.cos(-math.pi / 2 + j * math.pi / 5), sy + (r if j % 2 == 0 else r * 0.45) * math.sin(-math.pi / 2 + j * math.pi / 5)) for j in range(10)]
        d.polygon(pts, fill=ORO, outline=LINEA, width=5 * SS)
    etichetta(d, W, H, 'ti comporti così = sei così', y=0.86, col=(43, 33, 28, 255), dim=48)
    return fine(im, w, h)


def costume(p, t, w, h):
    """Finta + lavoro vero: a sinistra un costume vuoto, a destra chi si allena davvero."""
    im, d = tela(w, h, (250, 244, 232, 255))
    W, H = w * SS, h * SS
    d.line((W / 2, H * 0.08, W / 2, H * 0.92), fill=LINEA, width=6 * SS)
    # gruccia con costume vuoto
    cx = W * 0.25
    d.line((cx, H * 0.16, cx, H * 0.22), fill=LINEA, width=6 * SS)
    d.polygon([(cx - 140 * SS, H * 0.30), (cx, H * 0.22), (cx + 140 * SS, H * 0.30)], outline=LINEA, width=6 * SS)
    d.polygon([(cx - 120 * SS, H * 0.30), (cx + 120 * SS, H * 0.30), (cx + 160 * SS, H * 0.70), (cx - 160 * SS, H * 0.70)], fill=VIOLA, outline=LINEA, width=6 * SS)
    # persona che si allena con un libro e la lampadina che si accende
    omino(d, W * 0.75, H * 0.72, 260 * SS, VERDE)
    bx, by = W * 0.75 + 70 * SS, H * 0.52
    d.rectangle((bx - 70 * SS, by - 40 * SS + 8 * SS * math.sin(t * 5), bx + 70 * SS, by + 40 * SS + 8 * SS * math.sin(t * 5)), fill=ROSSO, outline=LINEA, width=5 * SS)
    g = font(46)
    for x, r in ((0.25, 'solo finta'), (0.75, 'finta + lavoro')):
        tw = d.textlength(r, font=g)
        d.text((W * x - tw / 2, H * 0.80), r, font=g, fill=LINEA)
    return fine(im, w, h)


VERDE_SOLDI = (120, 186, 120, 255)
VERDE_SCURO = (70, 130, 80, 255)
ORO_SCURO = (214, 150, 40, 255)


def banconota(d, cx, cy, s, ang=0.0):
    """Banconota generica (non una copia di quelle vere): rettangolo verde con il simbolo dell'euro."""
    a = math.radians(ang); c, si = math.cos(a), math.sin(a)
    rot = lambda x, y: (cx + x * c - y * si, cy + x * si + y * c)
    d.polygon([rot(-s, -s * 0.5), rot(s, -s * 0.5), rot(s, s * 0.5), rot(-s, s * 0.5)], fill=VERDE_SOLDI, outline=LINEA, width=max(2, 4 * SS))
    d.polygon([rot(-s * 0.85, -s * 0.36), rot(s * 0.85, -s * 0.36), rot(s * 0.85, s * 0.36), rot(-s * 0.85, s * 0.36)], outline=VERDE_SCURO, width=max(2, 3 * SS))
    r = s * 0.28
    x, y = rot(0, 0)
    d.ellipse((x - r, y - r, x + r, y + r), fill=(170, 220, 160, 255), outline=VERDE_SCURO, width=max(2, 3 * SS))
    f = font(max(10, int(s * 0.38 / SS)))
    tw = d.textlength('€', font=f)
    d.text((x - tw / 2, y - s * 0.24), '€', font=f, fill=VERDE_SCURO)


def moneta_oro(d, cx, cy, r):
    d.ellipse((cx - r, cy - r * 0.45 + 6 * SS, cx + r, cy + r * 0.45 + 6 * SS), fill=ORO_SCURO, outline=LINEA, width=4 * SS)
    d.ellipse((cx - r, cy - r * 0.45, cx + r, cy + r * 0.45), fill=ORO, outline=LINEA, width=4 * SS)


def soldi(p, t, w, h):
    """Ricco: pioggia di banconote, pile di monete d'oro e un sacco di soldi."""
    im, d = tela(w, h)
    W, H = w * SS, h * SS
    gradiente(im, (255, 236, 180), (255, 250, 230))
    d = ImageDraw.Draw(im, 'RGBA')
    for i in range(16):   # banconote che cadono ondeggiando
        f = (t * 0.35 + i * 0.137) % 1
        x = W * ((i * 0.173) % 1) + 50 * SS * math.sin(t * 2 + i)
        y = -H * 0.1 + f * H * 1.15
        banconota(d, x, y, 70 * SS, ang=25 * math.sin(t * 3 + i))
    # pile di monete
    for k, (x, n) in enumerate(((0.62, 7), (0.76, 10), (0.90, 5))):
        for j in range(n):
            moneta_oro(d, W * x, H * 0.86 - j * 26 * SS, 60 * SS)
    # sacco di soldi
    cx, cy = W * 0.30, H * 0.72
    d.ellipse((cx - 170 * SS, cy - 150 * SS, cx + 170 * SS, cy + 160 * SS), fill=(186, 140, 90, 255), outline=LINEA, width=7 * SS)
    d.polygon([(cx - 60 * SS, cy - 140 * SS), (cx + 60 * SS, cy - 140 * SS), (cx + 90 * SS, cy - 220 * SS), (cx - 90 * SS, cy - 220 * SS)], fill=(186, 140, 90, 255), outline=LINEA, width=6 * SS)
    d.line((cx - 70 * SS, cy - 145 * SS, cx + 70 * SS, cy - 145 * SS), fill=ORO_SCURO, width=12 * SS)
    g = font(150)
    tw = d.textlength('€', font=g)
    d.text((cx - tw / 2, cy - 90 * SS), '€', font=g, fill=ORO, stroke_width=5 * SS, stroke_fill=LINEA)
    for i, r in enumerate(['fare il ricco', 'finché non lo sei davvero']):
        etichetta(d, W, H, r, y=0.04 + 0.07 * i, col=(43, 33, 28, 255), dim=56 if i == 0 else 46)
    return fine(im, w, h)


def lusso(p, t, w, h):
    """Ce l'hai: villa, auto sportiva, orologio d'oro e diamante che brilla."""
    im, d = tela(w, h)
    W, H = w * SS, h * SS
    gradiente(im, (120, 186, 240), (240, 248, 255))
    d = ImageDraw.Draw(im, 'RGBA')
    d.rectangle((0, H * 0.66, W, H), fill=(120, 190, 110, 255))
    # villa con colonne
    x0, x1, y0, y1 = W * 0.10, W * 0.90, H * 0.30, H * 0.66
    d.rectangle((x0, y0, x1, y1), fill=(250, 244, 230, 255), outline=LINEA, width=7 * SS)
    d.polygon([(x0 - 30 * SS, y0), (W * 0.5, H * 0.16), (x1 + 30 * SS, y0)], fill=(230, 220, 200, 255), outline=LINEA, width=7 * SS)
    for i in range(6):
        cx = x0 + (x1 - x0) * (0.08 + 0.168 * i)
        d.rectangle((cx - 16 * SS, y0 + 20 * SS, cx + 16 * SS, y1), fill=(255, 252, 244, 255), outline=LINEA, width=4 * SS)
    d.rectangle((W * 0.44, H * 0.50, W * 0.56, y1), fill=SAIO, outline=LINEA, width=5 * SS)
    # piscina
    d.rounded_rectangle((W * 0.06, H * 0.70, W * 0.40, H * 0.80), radius=30 * SS, fill=(100, 190, 240, 255), outline=LINEA, width=5 * SS)
    # auto sportiva che entra
    k = min(1, t / 0.9)
    ax, ay = W * 1.2 - k * W * 0.55, H * 0.85
    d.rounded_rectangle((ax - 230 * SS, ay - 50 * SS, ax + 230 * SS, ay + 40 * SS), radius=40 * SS, fill=ROSSO, outline=LINEA, width=6 * SS)
    d.polygon([(ax - 110 * SS, ay - 50 * SS), (ax - 40 * SS, ay - 120 * SS), (ax + 90 * SS, ay - 120 * SS), (ax + 160 * SS, ay - 50 * SS)], fill=ROSSO, outline=LINEA, width=6 * SS)
    d.polygon([(ax - 80 * SS, ay - 55 * SS), (ax - 30 * SS, ay - 108 * SS), (ax + 80 * SS, ay - 108 * SS), (ax + 130 * SS, ay - 55 * SS)], fill=(190, 226, 250, 255))
    for ox in (-140, 140):
        d.ellipse((ax + ox * SS - 45 * SS, ay + 5 * SS, ax + ox * SS + 45 * SS, ay + 95 * SS), fill=LINEA)
        d.ellipse((ax + ox * SS - 20 * SS, ay + 30 * SS, ax + ox * SS + 20 * SS, ay + 70 * SS), fill=(190, 190, 200, 255))
    # diamante che brilla
    dx, dy, r = W * 0.84, H * 0.10, 70 * SS
    d.polygon([(dx - r, dy), (dx - r * 0.5, dy - r * 0.6), (dx + r * 0.5, dy - r * 0.6), (dx + r, dy), (dx, dy + r * 1.1)], fill=(180, 230, 255, 255), outline=LINEA, width=5 * SS)
    d.line((dx - r, dy, dx + r, dy), fill=LINEA, width=3 * SS)
    if math.sin(t * 7) > 0.3:
        for a in range(4):
            aa = a * math.pi / 2 + math.pi / 4
            d.line((dx + math.cos(aa) * r * 1.2, dy + math.sin(aa) * r * 1.2, dx + math.cos(aa) * r * 1.6, dy + math.sin(aa) * r * 1.6), fill=(255, 255, 255, 255), width=6 * SS)
    # orologio d'oro
    ox, oy = W * 0.16, H * 0.10
    d.rounded_rectangle((ox - 24 * SS, oy - 110 * SS, ox + 24 * SS, oy + 110 * SS), radius=12 * SS, fill=ORO_SCURO, outline=LINEA, width=4 * SS)
    d.ellipse((ox - 66 * SS, oy - 66 * SS, ox + 66 * SS, oy + 66 * SS), fill=ORO, outline=LINEA, width=6 * SS)
    d.ellipse((ox - 48 * SS, oy - 48 * SS, ox + 48 * SS, oy + 48 * SS), fill=CREMA, outline=LINEA, width=3 * SS)
    am = -math.pi / 2 + t * 2
    d.line((ox, oy, ox + math.cos(am) * 38 * SS, oy + math.sin(am) * 38 * SS), fill=LINEA, width=4 * SS)
    d.line((ox, oy, ox + 22 * SS, oy), fill=LINEA, width=6 * SS)
    return fine(im, w, h)


SCENE = {'l_gancio': l_gancio, 'sigla': sigla, 'cavalieri': cavalieri, 'finto': finto, 'scala': scala,
         'specchio': specchio, 'costume': costume, 'soldi': soldi, 'lusso': lusso}

if __name__ == '__main__':
    S = sys.argv[1]
    nomi = list(SCENE)
    tav = Image.new('RGB', (4 * 310, 2 * 410), (90, 90, 90))
    for i, n in enumerate(nomi):
        im = SCENE[n](0.95, 2.4, 760, 1000).resize((300, 395))
        tav.paste(im, ((i % 4) * 310 + 5, (i // 4) * 410 + 5))
    tav.save(f'{S}/scene_larping.png')

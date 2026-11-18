"""Illustrazioni originali per «Ti riduci all'ultimo per studiare?». f(p, t, w, h, **extra) -> RGB."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import ImageDraw
from scene_cielo import tela, fine, font, mix, gradiente, LINEA, CREMA, ORO, ROSSO, ARANCIO, BLU, SS
from scene_inception import etichetta, NOTTE, NOTTE2, VERDE
from scene_scuola import omino, PELLE, GRIGIO

SCURO = (43, 33, 28, 255)
POMO = (226, 62, 48, 255)
FOGLIA = (70, 150, 70, 255)
CARTA = (250, 246, 236, 255)
LIBRI = [(64, 120, 210, 255), (240, 150, 60, 255), (96, 178, 104, 255), (170, 90, 170, 255), (220, 70, 70, 255)]


def scala(w):
    return w / 840


def testo_c(d, x, y, s, f, col=SCURO, bordo=True):
    tw = d.textlength(s, font=f)
    d.text((x - tw / 2, y), s, font=f, fill=col, stroke_width=(4 * SS if bordo else 0),
           stroke_fill=(255, 255, 255, 255) if sum(col[:3]) < 360 else LINEA)


def pomodoro(d, cx, cy, r, frazione=None, ang=0):
    """Il pomodoro-timer: corpo rosso, picciolo verde; frazione = tempo che resta (spicchio chiaro)."""
    d.ellipse((cx - r, cy - r * 0.9, cx + r, cy + r * 0.9), fill=POMO, outline=LINEA, width=max(3, int(r * 0.06)))
    if frazione is not None and frazione < 1:
        a0 = -90 + 360 * frazione
        d.pieslice((cx - r * 0.72, cy - r * 0.64, cx + r * 0.72, cy + r * 0.64), a0, 270, fill=(255, 170, 150, 255))
    for k in range(5):
        a = math.radians(ang - 90 + k * 72)
        d.polygon([(cx, cy - r * 0.82), (cx + math.cos(a) * r * 0.42, cy - r * 0.82 + math.sin(a) * r * 0.22 - r * 0.05),
                   (cx + math.cos(a + 0.5) * r * 0.15, cy - r * 0.8)], fill=FOGLIA, outline=LINEA)
    d.rectangle((cx - r * 0.05, cy - r * 1.08, cx + r * 0.05, cy - r * 0.84), fill=FOGLIA, outline=LINEA)


def libro(d, x0, y0, x1, y1, col):
    d.rounded_rectangle((x0, y0, x1, y1), radius=6 * SS, fill=col, outline=LINEA, width=4 * SS)
    d.line((x0 + 12 * SS, y0 + (y1 - y0) * 0.35, x1 - 12 * SS, y0 + (y1 - y0) * 0.35), fill=(255, 255, 255, 140), width=3 * SS)


def notte(p, t, w, h):
    """La notte prima: scrivania, lampada, libri alti e l'orologio che corre verso le 3."""
    im, d = tela(w, h, NOTTE)
    W, H = w * SS, h * SS; k = scala(w)
    gradiente(im, NOTTE[:3], NOTTE2[:3])
    d = ImageDraw.Draw(im, 'RGBA')
    for i in range(14):
        x = W * ((i * 0.37) % 1); y = H * (0.04 + ((i * 0.53) % 0.3))
        a = int(120 + 120 * abs(math.sin(t * 2 + i)))
        d.ellipse((x - 4 * SS, y - 4 * SS, x + 4 * SS, y + 4 * SS), fill=(255, 255, 230, a))
    # orologio
    cx, cy, r = W * 0.76, H * 0.2, W * 0.13
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=CARTA, outline=LINEA, width=6 * SS)
    ore = 1 + min(2.0, t * 0.9)
    for ang, lun, larg in ((ore / 12 * 360, 0.5, 9), (ore * 12 % 1 * 360 + t * 300, 0.78, 6)):
        a = math.radians(ang - 90)
        d.line((cx, cy, cx + math.cos(a) * r * lun, cy + math.sin(a) * r * lun), fill=LINEA, width=larg * SS)
    testo_c(d, cx, cy + r + 14 * SS, f'0{int(ore)}:{int(ore % 1 * 60):02d}', font(int(46 * k)), CREMA, bordo=False)
    # luce della lampada
    d.polygon([(W * 0.26, H * 0.36), (W * 0.02, H * 0.74), (W * 0.7, H * 0.74)], fill=(255, 230, 150, 60))
    d.line((W * 0.2, H * 0.74, W * 0.2, H * 0.4), fill=LINEA, width=10 * SS)
    d.pieslice((W * 0.14, H * 0.3, W * 0.38, H * 0.42), 180, 360, fill=ORO, outline=LINEA, width=5 * SS)
    # scrivania e pila di libri che cresce
    d.rectangle((0, H * 0.74, W, H * 0.80), fill=(150, 104, 70, 255), outline=LINEA, width=5 * SS)
    n = min(7, 3 + int(t * 2.5))
    for i in range(n):
        y1 = H * 0.74 - i * H * 0.045
        dx = (i % 2) * 14 * SS
        libro(d, W * 0.48 + dx, y1 - H * 0.045, W * 0.86 + dx, y1, LIBRI[i % 5])
    # tazza
    d.rounded_rectangle((W * 0.3, H * 0.66, W * 0.4, H * 0.74), radius=8 * SS, fill=CARTA, outline=LINEA, width=4 * SS)
    for j in range(2):
        yy = H * 0.64 - ((t * 0.4 + j * 0.5) % 1) * H * 0.06
        d.arc((W * 0.32 + j * 20 * SS, yy - 20 * SS, W * 0.36 + j * 20 * SS, yy), 90, 270, fill=(255, 255, 255, 150), width=4 * SS)
    etichetta(d, W, H, 'la notte prima', y=0.86, col=CREMA, dim=int(54 * k))
    return fine(im, w, h)


def otto_su_dieci(p, t, w, h):
    """8 studenti su 10 rimandano: dieci omini, otto si colorano uno dopo l'altro."""
    im, d = tela(w, h, (240, 244, 252, 255))
    W, H = w * SS, h * SS; k = scala(w)
    n = min(8, int(t * 6))
    for i in range(10):
        c, r = i % 5, i // 5
        cx = W * (0.14 + 0.18 * c); base = H * (0.42 + 0.3 * r)
        col = ARANCIO if i < n else (200, 200, 206, 255)
        omino(d, cx, base, H * 0.13, col)
        if i < n:
            testo_c(d, cx + W * 0.06, base - H * 0.26, 'z', font(int(34 * k)), BLU, bordo=False)
    testo_c(d, W / 2, H * 0.04, f'{n} su 10', font(int(110 * k)), ROSSO)
    etichetta(d, W, H, 'rimandano', y=0.86, col=SCURO, dim=int(56 * k))
    return fine(im, w, h)


def compiti_ore(p, t, w, h):
    """Ore di compiti a settimana (OCSE PISA): Italia quasi 9, media OCSE 4,9, Corea del Sud 2,5."""
    im, d = tela(w, h)
    W, H = w * SS, h * SS; k = scala(w)
    testo_c(d, W / 2, H * 0.04, 'ore di compiti', font(int(62 * k)))
    testo_c(d, W / 2, H * 0.12, 'a settimana', font(int(44 * k)), GRIGIO, bordo=False)
    dati = [('Italia', 9, ROSSO, '≈ 9'), ('media', 4.9, (150, 150, 160, 255), '4,9'), ('Corea', 2.5, BLU, '2,5')]
    base, alto = H * 0.82, H * 0.30
    for i, (nome, v, col, et) in enumerate(dati):
        f = min(1, max(0, t * 1.4 - i * 0.25))
        x0 = W * (0.1 + 0.29 * i); x1 = x0 + W * 0.22
        y = base - (base - alto) * v / 9 * f
        d.rounded_rectangle((x0, y, x1, base), radius=14 * SS, fill=col, outline=LINEA, width=5 * SS)
        if f > 0.2:
            testo_c(d, (x0 + x1) / 2, y - 70 * SS * k, et, font(int(56 * k)))
        testo_c(d, (x0 + x1) / 2, base + 16 * SS, nome, font(int(42 * k)))
    d.line((W * 0.06, base, W * 0.94, base), fill=LINEA, width=6 * SS)
    return fine(im, w, h)


def risultati(p, t, w, h):
    """E i risultati? PISA 2022 matematica: Italia 471, media OCSE 472. Più compiti, non di più."""
    im, d = tela(w, h, (246, 242, 252, 255))
    W, H = w * SS, h * SS; k = scala(w)
    testo_c(d, W / 2, H * 0.05, 'risultati in matematica', font(int(50 * k)))
    for i, (nome, v, col) in enumerate((('Italia', 471, ROSSO), ('media', 472, (120, 120, 130, 255)))):
        cx = W * (0.28 + 0.44 * i)
        cont = int(min(1, t * 1.2) * v)
        d.rounded_rectangle((cx - W * 0.19, H * 0.26, cx + W * 0.19, H * 0.58), radius=30 * SS, fill=CARTA, outline=col, width=8 * SS)
        testo_c(d, cx, H * 0.33, str(cont), font(int(100 * k)), col, bordo=False)
        testo_c(d, cx, H * 0.50, nome, font(int(40 * k)), SCURO, bordo=False)
    if t > 0.9:
        q = 1 + 0.05 * math.sin(t * 6)
        testo_c(d, W / 2, H * 0.66, '=', font(int(120 * k * q)), SCURO)
    etichetta(d, W, H, 'non sono migliori', y=0.86, col=SCURO, dim=int(54 * k))
    return fine(im, w, h)


def giornata(p, t, w, h):
    """Mattina a scuola, pomeriggio sui libri, verifiche: la barra della giornata si riempie, niente spazio libero."""
    im, d = tela(w, h)
    W, H = w * SS, h * SS; k = scala(w)
    blocchi = [('scuola', 0.40, BLU), ('compiti', 0.35, ARANCIO), ('verifiche', 0.20, ROSSO), ('tu', 0.05, VERDE)]
    x, y0, y1 = W * 0.08, H * 0.26, H * 0.40
    f = min(1, t * 0.8)
    tot = W * 0.84
    acc = 0
    for nome, quota, col in blocchi:
        lar = tot * quota
        vis = max(0, min(lar, tot * f - acc))
        if vis > 0:
            d.rectangle((x + acc, y0, x + acc + vis, y1), fill=col, outline=LINEA, width=4 * SS)
            if vis > lar * 0.6:
                fs = font(int(36 * k))
                yy = y0 - 50 * SS * k if quota < 0.1 else y1 + 16 * SS
                testo_c(d, x + acc + lar / 2 - (14 * SS if quota < 0.1 else 0), yy, nome, fs, VERDE if quota < 0.1 else SCURO, bordo=False)
        acc += lar
    d.rounded_rectangle((x, y0, x + tot, y1), radius=10 * SS, outline=LINEA, width=6 * SS)
    testo_c(d, W / 2, H * 0.08, 'la tua giornata', font(int(60 * k)))
    # pila di verifiche che cade dall'alto
    for i in range(min(5, int(t * 3))):
        yy = H * 0.7 - i * H * 0.04
        d.rounded_rectangle((W * 0.3 + (i % 2) * 20 * SS, yy - H * 0.035, W * 0.7 + (i % 2) * 20 * SS, yy), radius=6 * SS, fill=CARTA, outline=LINEA, width=4 * SS)
        d.text((W * 0.32 + (i % 2) * 20 * SS, yy - H * 0.034), 'verifica', font=font(int(26 * k)), fill=ROSSO)
    etichetta(d, W, H, 'così non si respira', y=0.86, col=SCURO, dim=int(54 * k))
    return fine(im, w, h)


def sommerso(p, t, w, h):
    """Quando sei sommerso, rimandare diventa una difesa: lo studente sotto i fogli alza lo scudo «dopo»."""
    im, d = tela(w, h, (236, 240, 250, 255))
    W, H = w * SS, h * SS; k = scala(w)
    cx, base = W * 0.5, H * 0.8
    omino(d, cx, base, H * 0.2, ARANCIO)
    for i in range(12):
        f = (t * 0.7 + i / 12) % 1
        x = W * (0.12 + 0.76 * ((i * 0.41) % 1)); y = H * 0.02 + f * H * 0.48
        a = math.radians(f * 200 + i * 40)
        pts = [(x + math.cos(a + b) * 50 * SS * k, y + math.sin(a + b) * 36 * SS * k) for b in (0.6, 2.5, 3.7, 5.7)]
        d.polygon(pts, fill=CARTA, outline=LINEA)
    # scudo
    sx, sy = cx, base - H * 0.56
    sc = min(1, t * 1.5)
    r = W * 0.17 * sc
    if r > 1:
        d.polygon([(sx - r, sy - r * 0.8), (sx + r, sy - r * 0.8), (sx + r, sy + r * 0.1), (sx, sy + r), (sx - r, sy + r * 0.1)],
                  fill=VERDE, outline=LINEA, width=6 * SS)
        if sc > 0.7:
            testo_c(d, sx, sy - r * 0.45, 'dopo', font(int(52 * k)), CREMA, bordo=False)
    etichetta(d, W, H, 'una difesa', y=0.86, col=SCURO, dim=int(56 * k))
    return fine(im, w, h)


def tecnica(p, t, w, h):
    """La tecnica del pomodoro: il timer a forma di pomodoro che parte da 25:00."""
    im, d = tela(w, h, (255, 244, 238, 255))
    W, H = w * SS, h * SS; k = scala(w)
    q = 1 + 0.04 * math.sin(t * 5)
    r = min(W, H) * 0.3 * q
    sec = max(0, 25 * 60 - int(t * 40))
    pomodoro(d, W / 2, H * 0.48, r, frazione=sec / 1500, ang=t * 10)
    testo_c(d, W / 2, H * 0.43, f'{sec // 60}:{sec % 60:02d}', font(int(90 * k)), CREMA, bordo=False)
    testo_c(d, W / 2, H * 0.05, 'tecnica del', font(int(54 * k)))
    etichetta(d, W, H, 'POMODORO', y=0.82, col=POMO, dim=int(88 * k))
    return fine(im, w, h)


def niente_telefono(p, t, w, h):
    """25 minuti, solo studio: il telefono a faccia in giù, sbarrato."""
    im, d = tela(w, h)
    W, H = w * SS, h * SS; k = scala(w)
    testo_c(d, W / 2, H * 0.05, '25 minuti', font(int(92 * k)), POMO)
    cx, cy = W * 0.5, H * 0.5
    d.rounded_rectangle((cx - W * 0.16, cy - H * 0.2, cx + W * 0.16, cy + H * 0.2), radius=30 * SS, fill=(40, 40, 48, 255), outline=LINEA, width=6 * SS)
    for i in range(3):
        f = (t * 1.5 + i / 3) % 1
        d.rounded_rectangle((cx - W * 0.13, cy - H * 0.16 + i * H * 0.08, cx + W * 0.13, cy - H * 0.1 + i * H * 0.08), radius=10 * SS,
                            fill=(90, 140, 230, int(255 * (1 - f))))
    sc = min(1, max(0, t * 2 - 0.3))
    r = W * 0.27 * sc
    if r > 1:
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=ROSSO, width=18 * SS)
        a = math.radians(45)
        d.line((cx - math.cos(a) * r, cy - math.sin(a) * r, cx + math.cos(a) * r, cy + math.sin(a) * r), fill=ROSSO, width=18 * SS)
    etichetta(d, W, H, 'niente telefono', y=0.84, col=SCURO, dim=int(56 * k))
    return fine(im, w, h)


def cicli(p, t, w, h):
    """25 + 5, ripetuto quattro volte, poi una pausa lunga."""
    im, d = tela(w, h)
    W, H = w * SS, h * SS; k = scala(w)
    testo_c(d, W / 2, H * 0.05, '25 + 5', font(int(96 * k)), POMO)
    n = min(4, int(t * 2.2) + 1)
    for i in range(4):
        cy = H * (0.25 + 0.13 * i)
        if i < n:
            pomodoro(d, W * 0.24, cy, H * 0.05)
            d.rounded_rectangle((W * 0.34, cy - H * 0.03, W * 0.62, cy + H * 0.03), radius=12 * SS, fill=POMO, outline=LINEA, width=4 * SS)
            testo_c(d, W * 0.48, cy - H * 0.022, 'studio', font(int(34 * k)), CREMA, bordo=False)
            d.rounded_rectangle((W * 0.65, cy - H * 0.03, W * 0.8, cy + H * 0.03), radius=12 * SS, fill=VERDE, outline=LINEA, width=4 * SS)
            testo_c(d, W * 0.725, cy - H * 0.022, '5', font(int(34 * k)), CREMA, bordo=False)
    if t > 2.0 or n == 4 and t > 1.6:
        d.rounded_rectangle((W * 0.12, H * 0.78, W * 0.88, H * 0.88), radius=24 * SS, fill=(70, 160, 90, 255), outline=LINEA, width=5 * SS)
        testo_c(d, W / 2, H * 0.8, 'pausa lunga', font(int(52 * k)), CREMA, bordo=False)
    return fine(im, w, h)


def ogni_giorno(p, t, w, h):
    """Un pomodoro ogni giorno batte dieci pomodori la notte prima."""
    im, d = tela(w, h)
    W, H = w * SS, h * SS; k = scala(w)
    d.rectangle((0, 0, W / 2, H), fill=(232, 232, 240, 255))
    d.line((W / 2, 0, W / 2, H), fill=LINEA, width=6 * SS)
    testo_c(d, W * 0.25, H * 0.05, 'notte prima', font(int(40 * k)))
    testo_c(d, W * 0.75, H * 0.05, 'ogni giorno', font(int(40 * k)), VERDE, bordo=False)
    for i in range(10):
        pomodoro(d, W * (0.12 + 0.13 * (i % 3)) + (i // 3 % 2) * 20 * SS, H * (0.24 + 0.1 * (i // 3)), H * 0.042)
    if t > 0.7:
        d.line((W * 0.05, H * 0.2, W * 0.45, H * 0.65), fill=ROSSO, width=14 * SS)
        d.line((W * 0.45, H * 0.2, W * 0.05, H * 0.65), fill=ROSSO, width=14 * SS)
    giorni = ['L', 'M', 'M', 'G', 'V', 'S', 'D']
    n = min(7, int(t * 4) + 1)
    for i in range(7):
        y = H * (0.18 + 0.075 * i)
        testo_c(d, W * 0.62, y - H * 0.02, giorni[i], font(int(36 * k)), SCURO, bordo=False)
        if i < n:
            pomodoro(d, W * 0.8, y, H * 0.03)
    etichetta(d, W, H, 'un po\' alla volta', y=0.86, col=SCURO, dim=int(52 * k))
    return fine(im, w, h)


def ricordo(p, t, w, h):
    """Quanto ricordi dopo: curva illustrativa, lo studio distribuito resta in alto, quello della notte prima crolla."""
    im, d = tela(w, h)
    W, H = w * SS, h * SS; k = scala(w)
    testo_c(d, W / 2, H * 0.04, 'quanto ricordi', font(int(60 * k)))
    x0, x1, y0, y1 = W * 0.1, W * 0.92, H * 0.2, H * 0.74
    d.line((x0, y1, x1, y1), fill=LINEA, width=6 * SS); d.line((x0, y0, x0, y1), fill=LINEA, width=6 * SS)
    f = min(1, t * 0.8)
    for col, fn in ((ROSSO, lambda u: math.exp(-u * 4)), (VERDE, lambda u: 0.95 - 0.25 * u)):
        pts = [(x0 + (x1 - x0) * u, y1 - (y1 - y0) * fn(u) * 0.95) for u in [i / 60 * f for i in range(61)]]
        d.line(pts, fill=col, width=12 * SS, joint='curve')
    testo_c(d, W * 0.66, H * 0.22, 'un po\' al giorno', font(int(36 * k)), VERDE, bordo=False)
    if f > 0.5:
        testo_c(d, W * 0.66, H * 0.64, 'notte prima', font(int(36 * k)), ROSSO, bordo=False)
    testo_c(d, W / 2, y1 + 14 * SS, 'settimane dopo →', font(int(32 * k)), GRIGIO, bordo=False)
    etichetta(d, W, H, 'molto di più', y=0.86, col=SCURO, dim=int(56 * k))
    return fine(im, w, h)


def oggi(p, t, w, h):
    """Comincia oggi, con un solo pomodoro: calendario «oggi» e il pomodoro che si posa con la spunta."""
    im, d = tela(w, h, (255, 246, 232, 255))
    W, H = w * SS, h * SS; k = scala(w)
    d.rounded_rectangle((W * 0.18, H * 0.16, W * 0.82, H * 0.74), radius=30 * SS, fill=CARTA, outline=LINEA, width=7 * SS)
    d.rounded_rectangle((W * 0.18, H * 0.16, W * 0.82, H * 0.28), radius=30 * SS, fill=POMO, outline=LINEA, width=7 * SS)
    testo_c(d, W / 2, H * 0.185, 'OGGI', font(int(64 * k)), CREMA, bordo=False)
    f = min(1, t * 1.3)
    cy = H * 0.1 + f * H * 0.42
    pomodoro(d, W / 2, cy, H * 0.12)
    if f >= 1:
        d.line((W * 0.6, H * 0.6, W * 0.66, H * 0.66, W * 0.78, H * 0.5), fill=VERDE, width=16 * SS, joint='curve')
    etichetta(d, W, H, '25 minuti li trovi', y=0.82, col=SCURO, dim=int(52 * k))
    return fine(im, w, h)


SCENE = {'notte': notte, 'otto_su_dieci': otto_su_dieci, 'compiti_ore': compiti_ore, 'risultati': risultati,
         'giornata': giornata, 'sommerso': sommerso, 'tecnica': tecnica, 'niente_telefono': niente_telefono,
         'cicli': cicli, 'ogni_giorno': ogni_giorno, 'memoria': ricordo, 'oggi': oggi}

if __name__ == '__main__':
    from PIL import Image
    out = sys.argv[1]
    nomi = list(SCENE)
    tav = Image.new('RGB', (4 * 420, 3 * 500), 'white')
    for i, n in enumerate(nomi):
        tav.paste(SCENE[n](None, 2.5, 420, 500), ((i % 4) * 420, (i // 4) * 500))
    tav.save(out)

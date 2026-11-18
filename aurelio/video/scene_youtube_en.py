"""English version. Illustrazioni orizzontali (16:9) per la lezione YouTube su interesse composto, risparmio e rischio.
f(p, t, w, h, **extra) -> RGB; coordinate relative, pensate per riquadri da 1,3 a 1,6 di larghezza su altezza."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import ImageDraw
from scene_cielo import tela, fine, font, mix, gradiente, LINEA, CREMA, ORO, ROSSO, ARANCIO, BLU, SS
from scene_inception import VERDE, SAIO
from scene_larping import moneta_oro, ORO_SCURO, VERDE_SOLDI, VERDE_SCURO


def banconota(d, cx, cy, s, ang=0.0):
    """Generic banknote (not a copy of a real one) with a dollar sign."""
    a = math.radians(ang); c, si = math.cos(a), math.sin(a)
    rot = lambda x, y: (cx + x * c - y * si, cy + x * si + y * c)
    d.polygon([rot(-s, -s * 0.5), rot(s, -s * 0.5), rot(s, s * 0.5), rot(-s, s * 0.5)], fill=VERDE_SOLDI, outline=LINEA, width=max(2, 4 * SS))
    d.polygon([rot(-s * 0.85, -s * 0.36), rot(s * 0.85, -s * 0.36), rot(s * 0.85, s * 0.36), rot(-s * 0.85, s * 0.36)], outline=VERDE_SCURO, width=max(2, 3 * SS))
    r = s * 0.28
    x, y = rot(0, 0)
    d.ellipse((x - r, y - r, x + r, y + r), fill=(170, 220, 160, 255), outline=VERDE_SCURO, width=max(2, 3 * SS))
    f = font(max(10, int(s * 0.38 / SS)))
    tw = d.textlength('$', font=f)
    d.text((x - tw / 2, y - s * 0.24), '$', font=f, fill=VERDE_SCURO)
from scene_scuola import omino, GRIGIO

SCURO = (43, 33, 28, 255)
CARTA = (250, 246, 236, 255)
VERDE2 = (70, 160, 90, 255)
LAVAGNA = (38, 70, 58, 255)
ROSA = (232, 110, 140, 255)


def K(w, h): return min(w / 760, h / 560)


def tc(d, x, y, s, n, col=SCURO, bordo=False, centro=True):
    f = font(n)
    tw = d.textlength(s, font=f)
    d.text((x - tw / 2 if centro else x, y), s, font=f, fill=col, stroke_width=(4 * SS if bordo else 0),
           stroke_fill=(255, 255, 255, 255) if sum(col[:3]) < 360 else LINEA)


def e(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3


def euro(v):
    return '$' + f'{int(round(v)):,}'


def timbro(d, cx, cy, testo, n, col, ang_k=1.0):
    f = font(n)
    tw = d.textlength(testo, font=f)
    pad = n * 0.35 * SS
    d.rounded_rectangle((cx - tw / 2 - pad, cy - n * 0.7 * SS, cx + tw / 2 + pad, cy + n * 0.75 * SS), radius=12 * SS,
                        outline=col, width=int(8 * SS * ang_k))
    d.text((cx - tw / 2, cy - n * 0.6 * SS), testo, font=f, fill=col)


# ------------------------------------------------------------------ apertura
def meraviglia(p, t, w, h, falso=1.1):
    """«L'ottava meraviglia del mondo»: sette cartoline numerate e l'ottava con l'euro; poi il timbro «mai detta»."""
    im, d = tela(w, h, (244, 238, 226, 255)); W, H = w * SS, h * SS; k = K(w, h)
    tc(d, W / 2, H * 0.05, 'the eighth wonder of the world?', int(44 * k))
    for i in range(7):
        x = W * (0.08 + 0.12 * i); y = H * 0.30
        a = e(t * 2 - i * 0.12)
        if a <= 0: continue
        d.rounded_rectangle((x - W * 0.05, y, x + W * 0.05, y + H * 0.2), radius=10 * SS, fill=(220, 210, 190, 255), outline=LINEA, width=3 * SS)
        tc(d, x, y + H * 0.06, str(i + 1), int(40 * k), GRIGIO)
    a = e(t * 1.5 - 1.0)
    if a > 0:
        r = H * 0.2 * a
        cx, cy = W * 0.5, H * 0.73
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=ORO, outline=LINEA, width=6 * SS)
        tc(d, cx, cy - r * 0.55, '8', int(90 * k * a), SCURO)
    if p >= falso:
        timbro(d, W * 0.78, H * 0.62, 'NEVER SAID IT', int(46 * k), ROSSO)
    return fine(im, w, h)


def programma(p, t, w, h):
    """La lavagna della lezione: tre punti che compaiono uno alla volta."""
    im, d = tela(w, h, LAVAGNA); W, H = w * SS, h * SS; k = K(w, h)
    d.rectangle((0, 0, W, H), outline=(150, 104, 70, 255), width=24 * SS)
    tc(d, W / 2, H * 0.08, "today's lesson", int(48 * k), CREMA)
    voci = ['1. compound interest', '2. how to save', '3. safe investments?']
    for i, v in enumerate(voci):
        a = e(t * 1.2 - i * 0.6)
        if a <= 0: continue
        d.text((W * 0.12 + (1 - a) * 60 * SS, H * (0.30 + 0.2 * i)), v, font=font(int(52 * k)), fill=(255, 255, 255, int(255 * a)))
    return fine(im, w, h)


# ------------------------------------------------------------------ come funziona
def mille(p, t, w, h, anno=1):
    """1.000 € al 4%: primo anno +40 €; secondo anno il 4% si calcola su 1.040 € (+41,60 €)."""
    im, d = tela(w, h); W, H = w * SS, h * SS; k = K(w, h)
    base = 1000 if anno == 1 else 1040
    interesse = base * 0.04
    tc(d, W / 2, H * 0.05, f'year {anno}', int(56 * k), BLU)
    n = 8 if anno == 1 else 9
    for i in range(n):
        moneta_oro(d, W * 0.28, H * 0.78 - i * H * 0.055, W * 0.1)
    tc(d, W * 0.28, H * 0.84, euro(base), int(50 * k))
    a = e(t * 1.3 - 0.4)
    if a > 0:
        tc(d, W * 0.53, H * 0.42, '× 4%', int(54 * k), ARANCIO)
        d.line((W * 0.44, H * 0.56, W * 0.6, H * 0.56), fill=LINEA, width=8 * SS)
        d.polygon([(W * 0.62, H * 0.56), (W * 0.58, H * 0.52), (W * 0.58, H * 0.6)], fill=LINEA)
    b = e(t * 1.3 - 1.0)
    if b > 0:
        for i in range(1 if anno == 1 else 2):
            moneta_oro(d, W * 0.76, H * 0.68 - i * H * 0.055 - (1 - b) * H * 0.2, W * 0.07)
        tc(d, W * 0.76, H * 0.76, '+ $' + (f'{interesse:.2f}' if anno == 2 else '40'), int(54 * k), VERDE2)
    if anno == 2 and t > 1.6:
        tc(d, W / 2, H * 0.17, 'interest on interest', int(40 * k), ROSSO)
    return fine(im, w, h)


def neve(p, t, w, h):
    """La palla di neve che rotola giù per il pendio e cresce."""
    im, d = tela(w, h); W, H = w * SS, h * SS; k = K(w, h)
    gradiente(im, (170, 210, 245), (230, 242, 252))
    d = ImageDraw.Draw(im, 'RGBA')
    d.polygon([(0, H * 0.25), (W, H * 0.9), (0, H)], fill=(255, 255, 255, 255), outline=LINEA)
    d.polygon([(0, H * 0.9), (W, H * 0.9), (W, H), (0, H)], fill=(240, 246, 252, 255))
    u = (t * 0.35) % 1
    x = W * (0.06 + 0.82 * u); y = H * (0.25 + 0.65 * u)
    r = H * (0.03 + 0.16 * u ** 1.6)
    d.ellipse((x - r, y - 2 * r, x + r, y), fill=(255, 255, 255, 255), outline=LINEA, width=5 * SS)
    a = math.radians(t * 300)
    d.arc((x - r * 0.6, y - r * 1.6, x + r * 0.6, y - r * 0.4), math.degrees(a), math.degrees(a) + 90, fill=(170, 190, 210, 255), width=4 * SS)
    tc(d, W * 0.7, H * 0.08, 'the bigger it gets,', int(48 * k))
    tc(d, W * 0.7, H * 0.2, 'the more it picks up', int(48 * k), BLU)
    return fine(im, w, h)


def regola72(p, t, w, h):
    """72 ÷ 4 = 18 anni per raddoppiare: 1.000 € diventano 2.000 €."""
    im, d = tela(w, h, (246, 242, 252, 255)); W, H = w * SS, h * SS; k = K(w, h)
    tc(d, W / 2, H * 0.05, 'the rule of 72', int(54 * k), ROSSO)
    parti = ['72', '÷ 4%', '= 18 years']
    for i, s in enumerate(parti):
        if t * 1.6 > i * 0.6:
            tc(d, W * (0.14 + 0.33 * i), H * 0.25, s, int(62 * k))
    a = e(t * 0.9 - 1.2)
    if a > 0:
        for j, (x, n, et) in enumerate(((0.3, 5, '$1,000'), (0.7, 10, '$2,000'))):
            if j == 1 and a < 0.6: continue
            for i in range(n if j == 0 else int(5 + 5 * min(1, (a - 0.6) / 0.4))):
                banconota(d, W * x, H * 0.82 - i * H * 0.035, W * 0.09)
            tc(d, W * x, H * 0.86, et, int(46 * k), VERDE2 if j else SCURO)
        d.line((W * 0.43, H * 0.7, W * 0.57, H * 0.7), fill=LINEA, width=8 * SS)
        d.polygon([(W * 0.6, H * 0.7), (W * 0.56, H * 0.66), (W * 0.56, H * 0.74)], fill=LINEA)
    return fine(im, w, h)


# ------------------------------------------------------------------ Anna e Marco
def anna_marco(p, t, w, h, totali=1.1, solo='', pieno=0):
    """100 € al mese al 4%: Anna da 25 a 65 anni, Marco da 35 a 65. Curve vere (capitalizzazione mensile)."""
    im, d = tela(w, h); W, H = w * SS, h * SS; k = K(w, h)
    x0, x1, y0, y1 = W * 0.1, W * 0.78, H * 0.14, H * 0.84
    d.line((x0, y1, x1, y1), fill=LINEA, width=6 * SS); d.line((x0, y0, x0, y1), fill=LINEA, width=6 * SS)
    for eta in (25, 35, 45, 55, 65):
        x = x0 + (x1 - x0) * (eta - 25) / 40
        tc(d, x, y1 + 10 * SS, str(eta), int(30 * k), GRIGIO)
    def fv(anni):
        r = 0.04 / 12; n = anni * 12
        return 100 * ((1 + r) ** n - 1) / r
    f = 1 if pieno else min(1, t * 0.45)
    for nome, inizio, col in (('Anna', 25, ROSA), ('Mark', 35, BLU)):
        if solo and solo != nome: continue
        pts = []
        for i in range(81):
            eta = 25 + 40 * i / 80
            if eta > 25 + 40 * f: break
            v = fv(eta - inizio) if eta >= inizio else 0
            if eta < inizio: continue
            pts.append((x0 + (x1 - x0) * (eta - 25) / 40, y1 - (y1 - y0) * v / 120000))
        if len(pts) > 1:
            d.line(pts, fill=col, width=12 * SS, joint='curve')
        omino(d, x0 + (x1 - x0) * (inizio - 25) / 40, y1 - 14 * SS, H * 0.09, col)
        tc(d, x0 + (x1 - x0) * (inizio - 25) / 40, y1 - H * 0.28, nome, int(34 * k), col)
        if p >= totali and f >= 1:
            v = fv(65 - inizio)
            tc(d, W * 0.89, y1 - (y1 - y0) * v / 120000 - 26 * SS, euro(round(v, -3)), int(40 * k), col)
    tc(d, W * 0.45, H * 0.02, '$100 a month, 4% a year', int(36 * k))
    return fine(im, w, h)


def ritardo(p, t, w, h):
    """10 anni di ritardo = quasi 50.000 € in meno."""
    im, d = tela(w, h, (255, 244, 238, 255)); W, H = w * SS, h * SS; k = K(w, h)
    tc(d, W / 2, H * 0.1, '10 years late', int(60 * k))
    v = int(49000 * e(t * 0.9))
    q = 1 + 0.04 * math.sin(t * 6)
    tc(d, W / 2, H * 0.36, '− ' + euro(round(v, -2)), int(110 * k * q), ROSSO)
    tc(d, W / 2, H * 0.72, 'the secret is WHEN you start', int(44 * k), BLU)
    return fine(im, w, h)


def materasso(p, t, w, h):
    """10.000 € sotto il materasso con inflazione al 2%: dopo 20 anni valgono come 6.730 € di oggi."""
    im, d = tela(w, h, (236, 232, 246, 255)); W, H = w * SS, h * SS; k = K(w, h)
    anni = min(20, int(t * 8))
    val = 10000 / 1.02 ** anni
    d.rounded_rectangle((W * 0.08, H * 0.58, W * 0.62, H * 0.78), radius=30 * SS, fill=(250, 250, 255, 255), outline=LINEA, width=6 * SS)
    d.rectangle((W * 0.08, H * 0.78, W * 0.62, H * 0.84), fill=SAIO, outline=LINEA, width=5 * SS)
    n = max(1, int(8 * val / 10000))
    for i in range(n):
        banconota(d, W * (0.16 + 0.055 * i), H * 0.56, W * 0.08, ang=-8 + 3 * i)
    tc(d, W * 0.8, H * 0.2, f'year {anni}', int(48 * k), GRIGIO)
    tc(d, W * 0.8, H * 0.36, euro(round(val, -1)), int(64 * k), ROSSO if anni > 10 else SCURO)
    tc(d, W * 0.8, H * 0.52, '2% inflation', int(32 * k), GRIGIO)
    tc(d, W * 0.36, H * 0.1, 'idle money', int(52 * k))
    return fine(im, w, h)


def inflazione(p, t, w, h):
    """Inflation in 2022 (annual average): US 8.0% (BLS CPI), UK 9.1% (ONS CPI), eurozone 8.4% (Eurostat HICP); 2% target line."""
    im, d = tela(w, h); W, H = w * SS, h * SS; k = K(w, h)
    dati = [('US', 8.0), ('UK', 9.1), ('eurozone', 8.4)]
    tc(d, W / 2, H * 0.04, 'inflation in 2022', int(50 * k))
    base, alto = H * 0.84, H * 0.24
    for i, (a_, v) in enumerate(dati):
        f = e(t * 1.4 - i * 0.2)
        x0 = W * (0.12 + 0.27 * i); x1 = x0 + W * 0.18
        y = base - (base - alto) * v / 9.5 * f
        d.rounded_rectangle((x0, y, x1, base), radius=10 * SS, fill=ROSSO, outline=LINEA, width=4 * SS)
        if f > 0.3:
            tc(d, (x0 + x1) / 2, y - 50 * SS * k, f'{v:.1f}%', int(38 * k), ROSSO)
        tc(d, (x0 + x1) / 2, base + 10 * SS, a_, int(32 * k))
    y2 = base - (base - alto) * 2 / 9.5
    d.line((W * 0.06, y2, W * 0.94, y2), fill=VERDE2, width=5 * SS)
    tc(d, W * 0.92, y2 - 34 * SS * k, '2%', int(26 * k), VERDE2)
    d.line((W * 0.06, base, W * 0.94, base), fill=LINEA, width=5 * SS)
    return fine(im, w, h)


# ------------------------------------------------------------------ come si comincia
def emergenza(p, t, w, h):
    """Il fondo di emergenza: un salvagente con 3-6 mesi di spese; l'imprevisto (la pioggia) non fa danni."""
    im, d = tela(w, h, (232, 242, 250, 255)); W, H = w * SS, h * SS; k = K(w, h)
    for i in range(24):
        x = W * ((i * 0.137) % 1); y = ((t * 0.9 + i * 0.29) % 1) * H * 0.5
        d.line((x, y, x - 8 * SS, y + 26 * SS), fill=(90, 140, 210, 200), width=4 * SS)
    cx, cy, r = W * 0.36, H * 0.6, H * 0.26
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255, 255), outline=LINEA, width=6 * SS)
    for a in range(0, 360, 90):
        d.pieslice((cx - r, cy - r, cx + r, cy + r), a + 20, a + 60, fill=ROSSO)
    d.ellipse((cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55), fill=(232, 242, 250, 255), outline=LINEA, width=5 * SS)
    tc(d, cx, cy - 26 * SS, '$', int(54 * k))
    tc(d, W * 0.78, H * 0.36, '3-6 months', int(52 * k), BLU)
    tc(d, W * 0.78, H * 0.52, 'of expenses', int(46 * k))
    tc(d, W * 0.78, H * 0.68, 'always available', int(32 * k), GRIGIO)
    tc(d, W / 2, H * 0.04, 'emergency fund', int(52 * k), SCURO, bordo=True)
    return fine(im, w, h)


def prima_tu(p, t, w, h):
    """Risparmia per primo: lo stipendio arriva e una parte va subito nel salvadanaio, poi le spese."""
    im, d = tela(w, h); W, H = w * SS, h * SS; k = K(w, h)
    tc(d, W / 2, H * 0.04, 'as soon as you get paid', int(44 * k))
    d.rounded_rectangle((W * 0.06, H * 0.3, W * 0.3, H * 0.62), radius=16 * SS, fill=CARTA, outline=LINEA, width=5 * SS)
    tc(d, W * 0.18, H * 0.42, 'paycheck', int(32 * k))
    f = (t * 0.7) % 1
    x = W * (0.3 + 0.32 * e(f * 1.4)); y = H * (0.46 - 0.1 * math.sin(math.pi * min(1, f * 1.4)))
    banconota(d, x, y, W * 0.08)
    # salvadanaio
    cx, cy = W * 0.74, H * 0.5
    d.ellipse((cx - W * 0.14, cy - H * 0.16, cx + W * 0.14, cy + H * 0.16), fill=ROSA, outline=LINEA, width=6 * SS)
    d.rectangle((cx - W * 0.04, cy - H * 0.17, cx + W * 0.04, cy - H * 0.14), fill=LINEA)
    tc(d, cx, cy - 20 * SS, '1st', int(56 * k), CREMA)
    tc(d, W * 0.74, H * 0.74, 'pay yourself first', int(48 * k), VERDE2)
    tc(d, W * 0.3, H * 0.74, 'then the bills', int(36 * k), GRIGIO)
    return fine(im, w, h)


def scala_rischio(p, t, w, h, livello=3):
    """La scala del rischio: conto e conto deposito, titoli di Stato, azioni e fondi. Freccia rendimento = rischio."""
    im, d = tela(w, h, (248, 246, 240, 255)); W, H = w * SS, h * SS; k = K(w, h)
    gradini = [('savings and deposits', VERDE2, 'protected up to a limit, but they pay little'),
               ('government bonds', ORO, 'low risk, price moves if you sell before maturity'),
               ('stocks and funds', ROSSO, 'higher long-run returns, but big drops too')]
    for i, (nome, col, nota) in enumerate(gradini):
        y1 = H * (0.94 - 0.26 * i); y0 = y1 - H * 0.22
        x1 = W * (0.68 + 0.06 * i)
        acceso = i < livello
        d.rounded_rectangle((W * 0.04, y0, x1, y1), radius=14 * SS, fill=col if acceso else (220, 216, 208, 255), outline=LINEA, width=5 * SS)
        if acceso:
            d.text((W * 0.07, y0 + H * 0.03), nome, font=font(int(34 * k)), fill=CREMA, stroke_width=3 * SS, stroke_fill=LINEA)
            f = font(int(19 * k))
            d.text((W * 0.07, y0 + H * 0.12), nota, font=f, fill=SCURO if col == ORO else (255, 255, 255, 240))
    d.line((W * 0.86, H * 0.92, W * 0.86, H * 0.2), fill=LINEA, width=10 * SS)
    d.polygon([(W * 0.86, H * 0.13), (W * 0.83, H * 0.21), (W * 0.89, H * 0.21)], fill=LINEA)
    tc(d, W * 0.86, H * 0.93, 'less', int(24 * k), GRIGIO)
    for i, (s_, c_) in enumerate((('more risk', ROSSO), ('more return', VERDE2))):
        tc(d, W * 0.86, H * (0.03 + 0.055 * i) + H * 0.0, s_, int(22 * k), c_)
    tc(d, W * 0.4, H * 0.03, 'zero risk does not exist', int(40 * k))
    return fine(im, w, h)


def garanzia(p, t, w, h):
    """Deposit protection up to a limit: $250,000 in the US (FDIC), €100,000 in the EU."""
    im, d = tela(w, h, (232, 246, 236, 255)); W, H = w * SS, h * SS; k = K(w, h)
    cx, cy = W * 0.24, H * 0.52
    r = H * 0.3 * (0.9 + 0.1 * e(t * 2))
    d.polygon([(cx - r, cy - r * 0.8), (cx + r, cy - r * 0.8), (cx + r, cy + r * 0.1), (cx, cy + r), (cx - r, cy + r * 0.1)],
              fill=VERDE2, outline=LINEA, width=7 * SS)
    tc(d, cx, cy - r * 0.35, '$€', int(90 * k), CREMA)
    tc(d, W * 0.7, H * 0.16, 'deposits protected', int(40 * k))
    tc(d, W * 0.7, H * 0.32, '$250,000', int(60 * k), VERDE2)
    tc(d, W * 0.7, H * 0.44, 'in the US', int(32 * k))
    if t > 0.8:
        tc(d, W * 0.7, H * 0.56, '€100,000', int(60 * k), VERDE2)
        tc(d, W * 0.7, H * 0.68, 'in the EU', int(32 * k))
    tc(d, W * 0.7, H * 0.82, 'but they pay little', int(30 * k), GRIGIO)
    return fine(im, w, h)


# ------------------------------------------------------------------ tre regole
def uova(p, t, w, h):
    """Diversifica: un solo paniere che cade contro tanti panieri."""
    im, d = tela(w, h); W, H = w * SS, h * SS; k = K(w, h)
    d.line((W / 2, H * 0.12, W / 2, H * 0.95), fill=LINEA, width=5 * SS)
    def paniere(cx, cy, s, n):
        for i in range(n):
            d.ellipse((cx - s * 0.6 + i * s * 0.4, cy - s * 0.9, cx - s * 0.2 + i * s * 0.4, cy - s * 0.3), fill=CARTA, outline=LINEA, width=3 * SS)
        d.polygon([(cx - s, cy - s * 0.5), (cx + s, cy - s * 0.5), (cx + s * 0.7, cy + s * 0.4), (cx - s * 0.7, cy + s * 0.4)], fill=SAIO, outline=LINEA, width=4 * SS)
    ang = min(25, t * 15)
    paniere(W * 0.25, H * 0.6 + ang * 2 * SS, W * 0.12, 4)
    if t > 1.2:
        d.line((W * 0.1, H * 0.35, W * 0.4, H * 0.85), fill=ROSSO, width=12 * SS)
    for i in range(4):
        paniere(W * (0.62 + 0.24 * (i % 2)), H * (0.45 + 0.3 * (i // 2)), W * 0.08, 2)
    tc(d, W * 0.25, H * 0.04, 'all in one', int(40 * k), ROSSO)
    tc(d, W * 0.75, H * 0.04, 'diversify', int(40 * k), VERDE2)
    return fine(im, w, h)


def costi(p, t, w, h):
    """L'1% di costi all'anno: 100 €/mese per 30 anni, 4% contro 3% netto = 69.405 € contro 58.274 €."""
    im, d = tela(w, h); W, H = w * SS, h * SS; k = K(w, h)
    x0, x1, y0, y1 = W * 0.1, W * 0.72, H * 0.16, H * 0.86
    d.line((x0, y1, x1, y1), fill=LINEA, width=6 * SS); d.line((x0, y0, x0, y1), fill=LINEA, width=6 * SS)
    f = min(1, t * 0.6)
    for tasso, col, fin in ((0.04, VERDE2, '$69,000'), (0.03, ROSSO, '$58,000')):
        pts = []
        for i in range(int(60 * f) + 1):
            anni = 30 * i / 60
            r = tasso / 12; n = anni * 12
            v = 100 * ((1 + r) ** n - 1) / r if n else 0
            pts.append((x0 + (x1 - x0) * i / 60, y1 - (y1 - y0) * v / 72000))
        if len(pts) > 1: d.line(pts, fill=col, width=12 * SS, joint='curve')
        if f >= 1:
            tc(d, W * 0.86, pts[-1][1] - 26 * SS, fin, int(42 * k), col)
    tc(d, W * 0.42, H * 0.02, '1% fees a year', int(40 * k))
    tc(d, W * 0.42, y1 + 10 * SS, '30 years →', int(28 * k), GRIGIO)
    return fine(im, w, h)


def truffa(p, t, w, h):
    """«Guadagno alto e garantito!»: il volantino e il timbro rosso."""
    im, d = tela(w, h, (255, 240, 236, 255)); W, H = w * SS, h * SS; k = K(w, h)
    d.rounded_rectangle((W * 0.18, H * 0.12, W * 0.82, H * 0.86), radius=20 * SS, fill=(255, 250, 200, 255), outline=LINEA, width=6 * SS)
    tc(d, W / 2, H * 0.2, 'EARN 20%', int(56 * k), ARANCIO)
    tc(d, W / 2, H * 0.36, 'GUARANTEED!', int(64 * k), ROSSO)
    for i in range(5):
        moneta_oro(d, W * (0.3 + 0.1 * i), H * 0.54 + 10 * SS * math.sin(t * 4 + i), W * 0.05)
    if t > 0.9:
        timbro(d, W / 2, H * 0.74, 'WARNING: SCAM', int(48 * k), ROSSO)
    return fine(im, w, h)


def informati(p, t, w, h):
    """Non è una consulenza: informati bene o parla con un professionista."""
    im, d = tela(w, h, (240, 244, 252, 255)); W, H = w * SS, h * SS; k = K(w, h)
    # libro
    d.polygon([(W * 0.1, H * 0.3), (W * 0.28, H * 0.36), (W * 0.28, H * 0.78), (W * 0.1, H * 0.72)], fill=CARTA, outline=LINEA, width=5 * SS)
    d.polygon([(W * 0.46, H * 0.3), (W * 0.28, H * 0.36), (W * 0.28, H * 0.78), (W * 0.46, H * 0.72)], fill=CARTA, outline=LINEA, width=5 * SS)
    for i in range(4):
        d.line((W * 0.13, H * (0.42 + 0.07 * i), W * 0.25, H * (0.46 + 0.07 * i)), fill=GRIGIO, width=4 * SS)
    tc(d, W * 0.28, H * 0.84, 'do your research', int(40 * k), BLU)
    omino(d, W * 0.72, H * 0.78, H * 0.26, BLU)
    d.rounded_rectangle((W * 0.6, H * 0.12, W * 0.92, H * 0.3), radius=20 * SS, fill=(255, 255, 255, 255), outline=LINEA, width=4 * SS)
    tc(d, W * 0.76, H * 0.16, '?', int(50 * k), BLU)
    tc(d, W * 0.72, H * 0.84, 'a professional', int(36 * k), SCURO)
    tc(d, W / 2, H * 0.02, 'not financial advice', int(40 * k), GRIGIO)
    return fine(im, w, h)


def iscriviti(p, t, w, h):
    """Mi piace, iscriviti, commenta: «a che età hai cominciato a risparmiare?»."""
    im, d = tela(w, h, (255, 246, 232, 255)); W, H = w * SS, h * SS; k = K(w, h)
    q = 1 + 0.06 * max(0, math.sin(t * 5))
    # pollice
    cx, cy = W * 0.2, H * 0.45
    s = H * 0.14 * q
    d.rounded_rectangle((cx - s, cy - s * 0.2, cx + s * 0.6, cy + s * 1.1), radius=16 * SS, fill=BLU, outline=LINEA, width=5 * SS)
    d.rounded_rectangle((cx - s * 0.3, cy - s * 1.1, cx + s * 0.2, cy + s * 0.1), radius=16 * SS, fill=BLU, outline=LINEA, width=5 * SS)
    tc(d, cx, cy + s * 1.3, 'like', int(32 * k))
    # iscriviti
    a = e(t * 1.5 - 0.5)
    d.rounded_rectangle((W * 0.38, H * 0.34, W * 0.66, H * 0.54), radius=30 * SS, fill=ROSSO if a < 1 or (t % 1.6) < 1.2 else (170, 40, 30, 255), outline=LINEA, width=5 * SS)
    tc(d, W * 0.52, H * 0.39, 'SUBSCRIBE', int(38 * k), CREMA)
    # commento
    b = e(t * 1.5 - 1.0)
    if b > 0:
        d.rounded_rectangle((W * 0.7, H * 0.22, W * 0.96, H * 0.58), radius=24 * SS, fill=(255, 255, 255, 255), outline=LINEA, width=5 * SS)
        d.polygon([(W * 0.74, H * 0.58), (W * 0.78, H * 0.58), (W * 0.72, H * 0.66)], fill=(255, 255, 255, 255), outline=LINEA)
        tc(d, W * 0.83, H * 0.29, 'how old were', int(26 * k))
        tc(d, W * 0.83, H * 0.37, 'you when you', int(26 * k))
        tc(d, W * 0.83, H * 0.45, 'started saving?', int(26 * k), BLU)
    tc(d, W / 2, H * 0.76, 'see you next lesson!', int(46 * k), SCURO)
    return fine(im, w, h)


SCENE_IT = {'meraviglia': meraviglia, 'programma': programma, 'mille': mille, 'neve': neve, 'regola72': regola72,
         'anna_marco': anna_marco, 'ritardo': ritardo, 'materasso': materasso, 'inflazione': inflazione,
         'emergenza': emergenza, 'prima_tu': prima_tu, 'scala_rischio': scala_rischio, 'garanzia': garanzia,
         'uova': uova, 'costi': costi, 'truffa': truffa, 'do your research': informati, 'iscriviti': iscriviti}

SCENE = {k + '_en': v for k, v in SCENE_IT.items()}

if __name__ == '__main__':
    from PIL import Image
    nomi = list(SCENE); cw, ch = 520, 380
    tav = Image.new('RGB', (4 * cw, 5 * ch), 'white')
    for i, n in enumerate(nomi):
        tav.paste(SCENE[n](1.0, 3.0, cw, ch), ((i % 4) * cw, (i // 4) * ch))
    tav.save(sys.argv[1])


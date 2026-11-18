"""Regia dinamica del Professor Aurelio: un cambio di inquadratura ogni 2-3 secondi.

Uso: python3 regia.py <cartella> <regia.json> [secondi,per,png]

Il file di regia elenca le frasi (come le dice la voce) e le inquadrature, ognuna
agganciata alla parola che la fa partire. Tipi di inquadratura:
  piena        scena esplicativa a tutto schermo, la voce continua a narrare
  primo_piano  Professore ravvicinato (testa, spalle e mano)
  angolo_dx    scena in alto, Professore a mezzo busto in basso a destra
  angolo_sx    scena in alto, Professore a mezzo busto in basso a sinistra
  affiancati   Professore intero a sinistra, scena a destra
Tagli netti fra le inquadrature, con un breve «zoom di ingresso»; spinta lenta di
camera dentro ogni inquadratura; piccolo colpo di zoom sulle parole chiave.
"""
import json, math, os, re, subprocess, sys
import numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFont

S = sys.argv[1]
sys.path.insert(0, S)
from anima import Figura
import scene_cielo, scene_inception, scene_fortnite, scene_scuola, scene_larping, scene_stipendio, scene_procrastinazione, scene_youtube, scene_youtube_en, disegni, inspect
SCENE_GRANDI = {**scene_cielo.SCENE, **scene_inception.SCENE, **scene_fortnite.SCENE, **scene_scuola.SCENE, **scene_larping.SCENE, **scene_stipendio.SCENE, **scene_procrastinazione.SCENE, **scene_youtube.SCENE, **scene_youtube_en.SCENE}

R = json.load(open(sys.argv[2], encoding='utf8'))
YT = R.get('formato') == 'youtube'   # 16:9 orizzontale per YouTube
W, H, FPS = (1920, 1080, 30) if YT else (1080, 1920, 30)
BG = (253, 252, 251)
INK = (43, 33, 28)
EVID = (205, 62, 48)
EVID_FONDO = (255, 214, 102)
F = '/usr/share/fonts/opentype/inter/'
def fnt(n): return ImageFont.truetype(F + 'InterDisplay-ExtraBold.otf', n)

# ------------------------------------------------------------------ tempi della voce
AUDIO = os.path.join(S, R['audio'])

def durata(f):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]))

def parlato(f, soglia='-38dB', minimo=0.12):
    out = subprocess.run(['ffmpeg', '-hide_banner', '-i', f, '-af', f'silencedetect=noise={soglia}:d={minimo}', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    ini = [float(x) for x in re.findall(r'silence_start: ([0-9.]+)', out)]
    fin = [float(x) for x in re.findall(r'silence_end: ([0-9.]+)', out)]
    tot = durata(f)
    voce, t = [], 0.0
    for a, b in zip(ini, fin + [tot] * (len(ini) - len(fin))):
        if a > t + 0.03: voce.append((t, a))
        t = b
    if tot > t + 0.03: voce.append((t, tot))
    return voce

FINE_VOCE = durata(AUDIO)
VOCE = parlato(AUDIO)

def allinea(unita, voce):
    """Assegna a ogni unita' un gruppo di intervalli di voce (ogni unita' finisce su una pausa vera)."""
    peso = [sum(len(w) + 2 for w in u.split()) for u in unita]
    tot = sum(b - a for a, b in voce)
    attesa = [tot * p / sum(peso) for p in peso]
    n, P, INF = len(unita), len(voce), float('inf')
    costo = [[INF] * (P + 1) for _ in range(n + 1)]; da = [[0] * (P + 1) for _ in range(n + 1)]
    costo[0][0] = 0
    for i in range(1, n + 1):
        for j in range(i, P + 1):
            for k in range(i - 1, j):
                if costo[i - 1][k] == INF: continue
                c = costo[i - 1][k] + (sum(b - a for a, b in voce[k:j]) - attesa[i - 1]) ** 2
                if c < costo[i][j]: costo[i][j] = c; da[i][j] = k
    gruppi, j = [], P
    for i in range(n, 0, -1):
        gruppi.append((da[i][j], j)); j = da[i][j]
    return list(reversed(gruppi))

def distribuisci(testo, pezzi):
    tv = sum(b - a for a, b in pezzi)
    def reale(x):
        for a, b in pezzi:
            if x <= b - a: return a + x
            x -= b - a
        return pezzi[-1][1]
    ws = testo.split(); pw = [len(w) + 2 for w in ws]; acc = 0; out = []
    for w, p in zip(ws, pw):
        s = reale(tv * acc / sum(pw)); acc += p
        out.append((w, s, reale(tv * acc / sum(pw) - 1e-6)))
    return out

# 1) ogni frase finisce su una pausa vera
parole = []   # (testo, inizio, fine)
for frase, (k, j) in zip(R['frasi'], allinea(R['frasi'], VOCE)):
    pezzi = VOCE[k:j]
    clausole = [u.strip() for u in re.findall(r'[^,;:]+[,;:]*', frase) if u.strip()]
    # 2) dentro la frase, le virgole usano le pause interne quando corrispondono una a una
    if len(clausole) > 1 and len(clausole) == len(pezzi):
        for c, pz in zip(clausole, pezzi):
            parole += distribuisci(c, [pz])
    elif len(clausole) > 1 and len(pezzi) > len(clausole):
        for c, (a, b) in zip(clausole, allinea(clausole, pezzi)):
            parole += distribuisci(c, pezzi[a:b])
    else:
        parole += distribuisci(frase, pezzi)

def norm(w): return re.sub(r"[^\w']", '', w.lower())

def t_parola(chi, volta=1):
    k = 0
    for w, s, e in parole:
        if norm(w) == chi:
            k += 1
            if k == volta: return s
    raise KeyError(chi)

def ancora(a):
    if isinstance(a, (int, float)): return float(a)
    w, _, v = a.partition('#')
    return t_parola(w, int(v or 1))

CHIAVE = set(R['chiave'])
DURATA = FINE_VOCE + R.get('coda', 0.6)

# inquadrature
SHOT = []
for i, s in enumerate(R['inquadrature']):
    a = 0.0 if i == 0 else ancora(s['da']) - 0.06
    SHOT.append(dict(s, inizio=a))
for i, s in enumerate(SHOT):
    s['fine'] = SHOT[i + 1]['inizio'] if i + 1 < len(SHOT) else DURATA
    s['eventi'] = {k: ancora(v) for k, v in s.get('eventi', {}).items()}

# sottotitoli: gruppi di 1-3 parole, mai oltre la punteggiatura
blocchi, cur = [], []
for p in parole:
    if cur and (len(cur) >= (4 if YT else 3) or len(' '.join(x[0] for x in cur + [p])) > (24 if YT else 16)):
        blocchi.append(cur); cur = []
    cur.append(p)
    if re.search(r'[,.;:?!]$', p[0]):
        blocchi.append(cur); cur = []
if cur: blocchi.append(cur)

# volume per la bocca
pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', AUDIO, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'],
                     capture_output=True, check=True).stdout
cmp = np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768
passo = 16000 // FPS
VOL = np.array([np.sqrt(np.mean(cmp[i:i + passo] ** 2)) for i in range(0, len(cmp), passo)])
VOL = np.clip((VOL - 0.015) / (np.percentile(VOL, 95) - 0.015), 0, 1)
T_CHIAVE = [s for w, s, e in parole if norm(w) in CHIAVE]

figura = Figura(f'{S}/figura_pulita.png')

def stato(t):
    ang = 4.5 * math.sin(2 * math.pi * t / 2.3)
    for k, s in enumerate(T_CHIAVE):
        if 0 <= t - s < 0.6:
            ang += (7 if k % 2 == 0 else -6) * math.sin(math.pi * (t - s) / 0.6)
    occhi, stupore = 'aperti', False
    a, b = ancora(R['stupore'][0]), ancora(R['stupore'][1])
    if a - 0.05 <= t <= b:
        stupore = True
    if t >= ancora(R['sorriso_da']):
        occhi = 'felici'
    if occhi == 'aperti' and not stupore and ((t - 1.3) % 2.9) < 0.13:
        occhi = 'chiusi'
    i = int(t * FPS)
    bocca = float(VOL[i]) if t < FINE_VOCE and i < len(VOL) else 0.0
    # avambraccio: si alza e si abbassa con il discorso, si solleva sulle parole chiave
    br = 2.6 + 2.4 * math.sin(2 * math.pi * t / 2.7 + 0.8)
    for s in T_CHIAVE:
        if 0 <= t - s < 0.7:
            br += 2.5 * math.sin(math.pi * (t - s) / 0.7)
    return dict(angolo_braccio=max(0.0, min(6.0, br)), angolo_mano=max(-8, min(8, ang)), ondeggio=0.6 * math.sin(2 * math.pi * t / 5.0),
                respiro=math.sin(2 * math.pi * t / 3.6), occhi=occhi, bocca=bocca, stupore=stupore)

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3

# ------------------------------------------------------------------ composizione
def scena_img(s, t, w, h):
    nome = s['scena']; lt = t - s['inizio']; dur = s['fine'] - s['inizio']
    p = min(1, lt / max(0.1, dur))
    if nome in SCENE_GRANDI:
        fn = SCENE_GRANDI[nome]
        firma = inspect.signature(fn).parameters
        extra = {k: v for k, v in s.get('parametri', {}).items() if k in firma}
        for k, v in s['eventi'].items():        # evento -> parametro in frazione della scena
            if k == 'zoom': continue
            nomep = {'colore': 'colore_da'}.get(k, k)
            if nomep in firma: extra[nomep] = (v - s['inizio']) / dur
        for k in ('punto', 'bersaglio'):
            if k in s and k in firma: extra[k] = tuple(s[k])
        rw = 760; rh = round(h * rw / w)
        if YT and rh < 480: rh = 480; rw = round(w * rh / h)        # base di disegno fissa: in grande gli elementi crescono
        return fn(p, lt, rw, rh, **extra).convert('RGB').resize((w, h), Image.BICUBIC)
    im = disegni.SCENE[nome](p, lt)          # 440x440 RGBA
    tela = Image.new('RGB', im.size, BG); tela.paste(im, (0, 0), im)
    return tela.resize((w, h), Image.BICUBIC)

def angoli(im, r=36):
    m = Image.new('L', im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), radius=r, fill=255)
    return m

def incolla_scena(fr, s, t, box):
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    if not YT and bw / bh > 0.95:
        # riquadro largo: la scena si disegna nelle sue proporzioni e si centra, senza schiacciarla
        sh = bh; sw = round(bh * 0.84)
        dentro = scena_img(s, t, sw, sh)
        sc = Image.new('RGB', (bw, bh), dentro.getpixel((2, 2)))
        sc.paste(dentro, ((bw - sw) // 2, 0))
    else:
        sc = scena_img(s, t, bw, bh)
    # zoom dentro la scena, sul dettaglio che la voce sta nominando
    if 'zoom' in s and t >= s['eventi'].get('zoom', 1e9):
        z = 1 + (s['zoom'] - 1) * ease((t - s['eventi']['zoom']) / 0.35)
        fx, fy = s.get('fuoco', (0.5, 0.5))
        w, h = sc.width / z, sc.height / z
        cx, cy = fx * sc.width, fy * sc.height
        a0 = min(max(0, cx - w / 2), sc.width - w); b0 = min(max(0, cy - h / 2), sc.height - h)
        sc = sc.crop((round(a0), round(b0), round(a0 + w), round(b0 + h))).resize((x1 - x0, y1 - y0), Image.BICUBIC)
    fr.paste(sc, (x0, y0), angoli(sc))
    ImageDraw.Draw(fr).rounded_rectangle(box, radius=36, outline=INK, width=6)

def scontorna(f):
    """Toglie solo lo sfondo bianco che tocca i bordi: occhi e riflessi chiari restano pieni."""
    a = np.array(f)
    chiaro = (a[..., 0] > 236) & (a[..., 1] > 232) & (a[..., 2] > 226)
    etich, _ = ndimage.label(chiaro, structure=np.ones((3, 3)))
    bordo = np.unique(np.concatenate([etich[0], etich[-1], etich[:, 0], etich[:, -1]]))
    fondo = np.isin(etich, bordo[bordo > 0])
    alfa = np.where(fondo, 0, 255).astype(np.uint8)
    alfa = np.array(Image.fromarray(alfa).filter(__import__('PIL.ImageFilter', fromlist=['x']).GaussianBlur(0.8)))
    return Image.fromarray(np.dstack([a, alfa]), 'RGBA')

def professore(t, ritaglio, alt):
    f = figura.quadro(**stato(t))
    if ritaglio: f = f.crop(ritaglio)
    f = scontorna(f)
    return f.resize((round(f.width * alt / f.height), alt), Image.BICUBIC)

# area sicura di TikTok: in alto «Seguiti / Per te», a destra i pulsanti, in basso nome e descrizione.
# Sottotitoli, scene e volto del Professore stanno qui dentro.
SX, DX, ALTO, BASSO = 60, W - 180, 230, 1480

def componi_yt(s, t):
    """YouTube 16:9: il Professore e' sempre in scena e protagonista; la scena e' la sua lavagna accanto a lui."""
    fr = Image.new('RGB', (W, H), BG)
    tipo = s['tipo']
    if tipo == 'primo_piano' or 'scena' not in s:
        f = professore(t, (0, 0, 600, 640), 1140)
        fr.paste(f, ((W - f.width) // 2 - 60, 10), f)
        area = (200, 900, W - 200, 1065)
    elif tipo == 'mezzo_busto':     # lui grande a sinistra, la lavagna a destra
        f = professore(t, (0, 0, 600, 860), 1100)
        fr.paste(f, (-30, H - f.height + 30), f)
        incolla_scena(fr, s, t, (780, 50, 1870, 850))
        area = (780, 870, 1870, 1060)
    elif tipo == 'angolo_dx':       # lavagna grande a sinistra, lui a destra
        incolla_scena(fr, s, t, (50, 40, 1290, 900))
        f = professore(t, (0, 0, 600, 860), 980)
        fr.paste(f, (W - f.width + 40, H - f.height + 20), f)
        area = (50, 910, 1290, 1070)
    elif tipo == 'angolo_sx':       # lui a sinistra, lavagna grande a destra
        f = professore(t, (0, 0, 600, 860), 980)
        fr.paste(f, (-60, H - f.height + 20), f)
        incolla_scena(fr, s, t, (630, 40, 1870, 900))
        area = (630, 910, 1870, 1070)
    else:                           # affiancati: lui intero a sinistra, la lavagna al centro-destra
        f = professore(t, None, 1050)
        fr.paste(f, (60, H - f.height - 10), f)
        incolla_scena(fr, s, t, (640, 60, 1840, 820))
        area = (640, 850, 1840, 1050)
    return fr, area

def componi(s, t):
    """Il Professore e' sempre in scena: cambia solo il punto di vista."""
    if YT: return componi_yt(s, t)
    fr = Image.new('RGB', (W, H), BG)
    tipo = s['tipo']
    if tipo == 'sfondo':          # la scena fa da sfondo, lui davanti a mezzo busto
        # la scena parte sotto la barra «Seguiti / Per te»; sopra si allunga il suo colore di cima
        cima = ALTO - 40
        sc = scena_img(s, t, W, H - cima)
        fr.paste(sc.getpixel((W // 2, 2)), (0, 0, W, cima)); fr.paste(sc, (0, cima))
        f = professore(t, (0, 0, 600, 860), 1150)
        fr.paste(f, (-40, H - f.height + 20), f)
        area = (SX, ALTO + 10, DX, 540) if s.get('testo_grande') else (SX, 520, DX, 800)
    elif tipo == 'primo_piano':
        f = professore(t, (0, 0, 600, 640), 1100)
        fr.paste(f, ((DX + SX - f.width) // 2, ALTO - 10), f)
        area = (SX, 1330, DX, BASSO)
    elif tipo == 'mezzo_busto':   # lui grande a sinistra, la scena accanto
        f = professore(t, (0, 0, 600, 860), 1250)
        fr.paste(f, (-60, H - f.height + 20), f)
        incolla_scena(fr, s, t, (420, ALTO, DX, 820))
        area = (500, 840, DX, 1060)
    elif tipo in ('angolo_dx', 'angolo_sx'):
        incolla_scena(fr, s, t, (SX, ALTO, DX, 1020))
        f = professore(t, (0, 0, 600, 860), 780)
        x = DX - f.width + 90 if tipo == 'angolo_dx' else -20
        fr.paste(f, (x, H - f.height + 20), f)
        area = (SX, 1025, DX, 1190) if s.get('testo_grande') else (SX, 1025, DX, 1150)
    else:  # affiancati: lui intero a sinistra, la scena a destra
        f = professore(t, None, 1180)
        fr.paste(f, (0, H - f.height - 20), f)
        incolla_scena(fr, s, t, (440, 640, DX, 1260))
        area = (SX, ALTO + 10, DX, 560)
    return fr, area

def camera(fr, s, t):
    """Spinta lenta dentro l'inquadratura, zoom di ingresso al taglio, colpo sulle parole chiave."""
    lt = t - s['inizio']
    z = 1 + 0.035 * min(1, lt / max(0.5, s['fine'] - s['inizio']))
    z += 0.07 * (1 - ease(lt / 0.22))
    for k in T_CHIAVE:
        if s['inizio'] <= k <= t < k + 0.3:
            z += 0.025 * math.sin(math.pi * (t - k) / 0.3)
    if abs(z - 1) < 1e-3: return fr
    cx, cy = W / 2, H * (0.45 if YT else 0.4)
    w, h = W / z, H / z
    x0 = min(max(0, cx - w / 2), W - w); y0 = min(max(0, cy - h / 2), H - h)
    return fr.crop((round(x0), round(y0), round(x0 + w), round(y0 + h))).resize((W, H), Image.BILINEAR)

def sottotitolo(fr, t, area, grande=False):
    b = next((b for b in blocchi if b[0][1] - 0.04 <= t <= b[-1][2] + 0.12), None)
    if not b: return
    x0, y0, x1, y1 = area
    larg = x1 - x0
    dim = (96 if grande else 80) if YT else (128 if grande else 104)
    righe = [b]
    while True:
        f = fnt(dim)
        tot = f.getlength(' '.join(w[0] for w in b))
        if tot <= larg: righe = [b]; break
        if len(b) > 1:
            meta = max(1, len(b) // 2 + (len(b) % 2))
            r1, r2 = b[:meta], b[meta:]
            if max(f.getlength(' '.join(w[0] for w in r)) for r in (r1, r2)) <= larg:
                righe = [r1, r2]; break
        dim -= 6
        if dim < 40: righe = [b]; break
    f = fnt(dim)
    comp = ease((t - b[0][1] + 0.04) / 0.1)
    alt_riga = dim * 1.12
    tot_h = alt_riga * len(righe)
    lay = Image.new('RGBA', (larg, int(tot_h + 40)), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    y = 10
    for riga in righe:
        x = (larg - f.getlength(' '.join(w[0] for w in riga))) / 2
        for w in riga:
            lw = f.getlength(w[0])
            chiave = norm(w[0]) in CHIAVE
            if chiave and t >= w[1]:
                d.rounded_rectangle((x - 10, y + dim * 0.18, x + lw + 10, y + dim * 1.08), radius=14, fill=EVID_FONDO)
            d.text((x, y), w[0], font=f, fill=EVID if chiave else INK, stroke_width=7, stroke_fill=(255, 255, 255))
            x += f.getlength(w[0] + ' ')
        y += alt_riga
    k = 0.86 + 0.14 * comp
    lay = lay.resize((max(1, round(lay.width * k)), max(1, round(lay.height * k))), Image.BICUBIC)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    fr.paste(lay, (round(cx - lay.width / 2), round(cy - lay.height / 2)), lay)

def gancio_testo(fr, t, area, testo):
    """Frase d'apertura breve e grande, visibile dal primo fotogramma."""
    x0, y0, x1, y1 = area
    ws = testo.replace('|', ' ').split()
    dim = 120
    while True:   # 1, 2 o 3 righe; il carattere si riduce finche' tutto entra
        f = fnt(dim)
        scelta = None
        prove = [[r.split() for r in testo.split('|')]] if '|' in testo else \
                [[ws[i:i + math.ceil(len(ws) / n)] for i in range(0, len(ws), math.ceil(len(ws) / n))] for n in (1, 2, 3)]
        for righe in prove:
            if max(f.getlength(' '.join(r)) for r in righe) <= (x1 - x0) - 20 and dim * 1.15 * len(righe) <= (y1 - y0) + 40:
                scelta = righe; break
        if scelta or dim <= 60: righe = scelta or righe; break
        dim -= 8
    k = 0.9 + 0.1 * ease(t / 0.15)
    lay = Image.new('RGBA', (x1 - x0, int(dim * 1.15 * len(righe) + 30)), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for i, r in enumerate(righe):
        x = (lay.width - f.getlength(' '.join(r))) / 2
        for w in r:
            chiave = norm(w) in CHIAVE
            if chiave:
                d.rounded_rectangle((x - 10, 10 + i * dim * 1.15 + dim * 0.18, x + f.getlength(w) + 10, 10 + i * dim * 1.15 + dim * 1.08), radius=14, fill=EVID_FONDO)
            d.text((x, 10 + i * dim * 1.15), w, font=f, fill=EVID if chiave else INK, stroke_width=7, stroke_fill=(255, 255, 255))
            x += f.getlength(w + ' ')
    lay = lay.resize((round(lay.width * k), round(lay.height * k)), Image.BICUBIC)
    fr.paste(lay, (round((x0 + x1 - lay.width) / 2), round((y0 + y1 - lay.height) / 2)), lay)

def quadro(t):
    s = next(s for s in SHOT if s['inizio'] <= t < s['fine'])
    fr, area = componi(s, t)
    fr = camera(fr, s, t)
    if s.get('testo_grande'):
        gancio_testo(fr, t, area, s['testo_grande'])
    else:
        sottotitolo(fr, t, area)
    # niente barra di avanzamento: TikTok ha la sua, e la nostra finirebbe sotto l'interfaccia
    return fr

if __name__ == '__main__' and sys.argv[4:5] == ['solo']:   # solo i fotogrammi di controllo
    for t in map(float, sys.argv[3].split(',')):
        quadro(t).save(f'{S}/quadro-{t:05.1f}.png')
elif __name__ == '__main__':
    out = os.path.join(S, f"aurelio-{R['nome']}.mp4")
    cmd = ['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
           '-r', str(FPS), '-i', '-', '-i', AUDIO, '-filter_complex', f'[1:a]apad=whole_dur={DURATA:.3f}[a]',
           '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-pix_fmt', 'yuv420p',
           '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', '-t', f'{DURATA:.3f}', out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(round(DURATA * FPS)):
        p.stdin.write(quadro(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    print(out, f'{DURATA:.1f}s', p.returncode)
    print('inquadrature:', [(s['tipo'], s['scena'] if 'scena' in s else '-', round(s['inizio'], 2), round(s['fine'] - s['inizio'], 2)) for s in SHOT])
    if len(sys.argv) > 3:
        for t in map(float, sys.argv[3].split(',')):
            quadro(t).save(f'{S}/quadro-{t:05.1f}.png')

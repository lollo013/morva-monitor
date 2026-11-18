"""Video verticale 1080x1920 del Professor Aurelio, da un file episodio.

Uso: python3 monta.py <cartella> <episodio.json> [secondi,da,salvare,come,png]
La cartella contiene figura_pulita.png e l'audio della voce A2 indicato nell'episodio.
"""
import math, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
sys.path.insert(0, sys.argv[1])
from anima import Figura
from disegni import SCENE, LATO

S = sys.argv[1]
import json, os
EP = json.load(open(sys.argv[2], encoding='utf8'))
W, H, FPS = 1080, 1920, 30
BG = (253, 252, 251)
INK = (43, 33, 28)
TENUE = (120, 104, 94)
SCIARPA = (138, 47, 39)
SAIO = (107, 74, 53)
ALLORO = (185, 138, 46)
NOTTE = (37, 42, 74)

F = '/usr/share/fonts/opentype/inter/'
cap = ImageFont.truetype(F + 'InterDisplay-ExtraBold.otf', 88)
chip = ImageFont.truetype(F + 'Inter-SemiBold.otf', 30)
card_big = ImageFont.truetype(F + 'InterDisplay-ExtraBold.otf', 54)
card_small = ImageFont.truetype(F + 'Inter-Medium.otf', 30)
titolo = ImageFont.truetype('/usr/share/fonts/truetype/crosextra/Caladea-Bold.ttf', 84)
fonte = ImageFont.truetype(F + 'Inter-Medium.otf', 28)

# ---------------------------------------------------------------- copione
AUDIO = os.path.join(S, EP['audio'])
FRASI = [(f, testo) for f, _, testo in EP['frasi']]
CHIAVE = set(EP['chiave'])

def durata_audio(f):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]))

def parlato(f, soglia='-38dB', minimo=0.16):
    """Intervalli in cui la voce parla (fra i silenzi)."""
    out = subprocess.run(['ffmpeg', '-hide_banner', '-i', f, '-af', f'silencedetect=noise={soglia}:d={minimo}', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    ini = [float(x) for x in re.findall(r'silence_start: ([0-9.]+)', out)]
    fin = [float(x) for x in re.findall(r'silence_end: ([0-9.]+)', out)]
    tot = durata_audio(f)
    silenzi = list(zip(ini, fin + [tot] * (len(ini) - len(fin))))
    voce, t = [], 0.0
    for a, b in silenzi:
        if a > t + 0.03: voce.append((t, a))
        t = b
    if tot > t + 0.03: voce.append((t, tot))
    return voce

FINE_VOCE = durata_audio(AUDIO)
VOCE = parlato(AUDIO)
TOT_VOCE = sum(b - a for a, b in VOCE)

def tempo_reale(x):
    """Da secondi di solo parlato a secondi del file audio."""
    for a, b in VOCE:
        if x <= b - a: return a + x
        x -= b - a
    return VOCE[-1][1]

# ogni fine frase cade su una pausa vera della voce: si scelgono le pause che
# rendono la durata di ogni frase piu' vicina a quella attesa dalle sue lettere
peso_frase = [sum(len(w) + 2 for w in fr.split()) for _, fr in FRASI]
attesa = [TOT_VOCE * p / sum(peso_frase) for p in peso_frase]
n, P = len(FRASI), len(VOCE)
INF = float('inf')
# costo[i][j]: frasi 0..i-1 coprono gli intervalli di voce 0..j-1
costo = [[INF] * (P + 1) for _ in range(n + 1)]; da = [[0] * (P + 1) for _ in range(n + 1)]
costo[0][0] = 0
for i in range(1, n + 1):
    for j in range(i, P + 1):
        for k in range(i - 1, j):
            if costo[i - 1][k] == INF: continue
            dur = sum(b - a for a, b in VOCE[k:j])
            c = costo[i - 1][k] + (dur - attesa[i - 1]) ** 2
            if c < costo[i][j]: costo[i][j] = c; da[i][j] = k
gruppi, j = [], P
for i in range(n, 0, -1):
    k = da[i][j]; gruppi.append((k, j)); j = k
gruppi.reverse()

parole, frasi = [], []
for (fase, fr), (k, j) in zip(FRASI, gruppi):
    pezzi = VOCE[k:j]; tv = sum(b - a for a, b in pezzi)
    def reale(x, pezzi=pezzi):
        for a, b in pezzi:
            if x <= b - a: return a + x
            x -= b - a
        return pezzi[-1][1]
    ws = fr.split(); pw = [len(w) + 2 for w in ws]; acc = 0
    for w, p in zip(ws, pw):
        s = reale(tv * acc / sum(pw)); acc += p
        parole.append((w, s, reale(tv * acc / sum(pw) - 1e-6), fase))
    frasi.append([pezzi[0][0], pezzi[-1][1]])
DURATA_TESTO = FINE_VOCE + 0.2
CODA = 1.2
DURATA = DURATA_TESTO + CODA

# sottotitoli: blocchi brevi, spezzati a fine frase
blocchi, cur = [], []
for p in parole:
    if cur and (len(' '.join(x[0] for x in cur + [p])) > 24):
        blocchi.append(cur); cur = []
    cur.append(p)
    if re.search(r'[.?!]$', p[0]):
        blocchi.append(cur); cur = []
if cur: blocchi.append(cur)

def a_capo(ws, font, larghezza):
    righe, riga = [], []
    for w in ws:
        prova = ' '.join(x[0] for x in riga + [w])
        if riga and font.getlength(prova) > larghezza:
            righe.append(riga); riga = []
        riga.append(w)
    if riga: righe.append(riga)
    return righe

# ---------------------------------------------------------------- schede
def t_parola(testo):
    for w, s, e, f in parole:
        if w.strip('.,?!').lower() == testo:
            return s
    raise KeyError(testo)

SCHEDE = [(t_parola(s['da']), (t_parola(s['a']) + s.get('anticipo', 0)) if s.get('a') else DURATA,
           s['titolo'], s['testo']) for s in EP['schede']]

# ---------------------------------------------------------------- figura
figura = Figura(f'{S}/figura_pulita.png')
FIG_H = 1220
SCALA = FIG_H / figura.base.height
FIG_X, FIG_Y = 10, H - FIG_H - 20

# volume della voce, quadro per quadro, per muovere la bocca
pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', AUDIO, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'],
                     capture_output=True, check=True).stdout
campioni = np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768
passo = 16000 // FPS
VOLUME = np.array([np.sqrt(np.mean(campioni[i:i + passo] ** 2)) for i in range(0, len(campioni), passo)])
VOLUME = np.clip((VOLUME - 0.015) / (np.percentile(VOLUME, 95) - 0.015), 0, 1)

# scene: indice della frase -> disegno
SCENA_DI_FRASE = [sc for _, sc, _ in EP['frasi']]
scene = []
for i, nome in enumerate(SCENA_DI_FRASE):
    a, b = frasi[i]
    if scene and scene[-1][0] == nome:
        scene[-1][2] = b
    else:
        scene.append([nome, a, b])
scene[0][1] = 0.0
for i in range(len(scene) - 1):
    scene[i][2] = scene[i + 1][1]
scene[-1][2] = 1e9
PAROLE_CHIAVE_T = [s for w, s, e, f in parole if w.strip('.,?!').lower() in CHIAVE]

def stato_figura(t):
    """Gesti ed espressioni nel tempo."""
    attivo = 1.0 if t < DURATA_TESTO else 0.35
    ang = 4.5 * math.sin(2 * math.pi * t / 2.3) * attivo
    for k, s in enumerate(PAROLE_CHIAVE_T):
        if 0 <= t - s < 0.7:
            ang += (7 if k % 2 == 0 else -6) * math.sin(math.pi * (t - s) / 0.7)
    ang = max(-8, min(8, ang))
    occhi, stupore, bocca = 'aperti', False, 0.0
    i0, i1 = EP['stupore']
    if frasi[i0][0] - 0.1 <= t <= frasi[i1][0] + 1.2:
        stupore = True
    if t >= frasi[EP['sorriso_da']][0]:
        occhi = 'felici'
    if occhi == 'aperti' and not stupore and ((t - 1.7) % 3.1) < 0.13:
        occhi = 'chiusi'
    i = int(t * FPS)
    if t < FINE_VOCE and i < len(VOLUME):
        bocca = float(VOLUME[i])
    return dict(angolo_mano=ang, ondeggio=0.7 * math.sin(2 * math.pi * t / 6.0),
                respiro=math.sin(2 * math.pi * t / 3.8), occhi=occhi, bocca=bocca, stupore=stupore)

def back(x):
    x = max(0.0, min(1.0, x)); c = 1.7
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2

def scena(im, t):
    for nome, a, b in scene:
        if a <= t < b:
            lt = t - a
            p = min(1, lt / max(0.1, min(b, DURATA_TESTO) - a))
            dis = SCENE[nome](p, lt)
            k = back(lt / 0.45)
            lato = max(1, round(LATO * k))
            if lato != LATO:
                dis = dis.resize((lato, lato), Image.BICUBIC)
            galleggia = 8 * math.sin(t * 1.6)
            cx, cy = 600 + LATO // 2, 960 + LATO // 2 + galleggia
            im.paste(dis, (round(cx - lato / 2), round(cy - lato / 2)), dis)
            return

def ease(x):
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3

def stelle(d, t):
    for i, (x, y, r) in enumerate([(930, 120, 7), (990, 210, 4), (870, 250, 5), (1010, 330, 3), (820, 140, 3)]):
        a = 0.55 + 0.45 * math.sin(t * 2.2 + i * 1.7)
        c = tuple(round(BG[k] + (ALLORO[k] - BG[k]) * a) for k in range(3))
        d.line((x - r * 2, y, x + r * 2, y), fill=c, width=3)
        d.line((x, y - r * 2, x, y + r * 2), fill=c, width=3)

def quadro(t):
    im = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(im)
    f = figura.quadro(**stato_figura(t))
    f = f.resize((round(f.width * SCALA), FIG_H), Image.BILINEAR)
    im.paste(f, (FIG_X, FIG_Y))
    scena(im, t)
    stelle(d, t)
    # sottotitoli
    if t < DURATA_TESTO:
        b = next((b for b in blocchi if b[0][1] - 0.05 <= t <= b[-1][2] + 0.25), None)
        if b:
            comparsa = ease((t - b[0][1] + 0.05) / 0.18)
            righe = a_capo(b, cap, W - 120)
            if len(righe) == 2 and len(righe[1]) == 1 and len(righe[0]) > 1:
                righe = [righe[0][:-1], righe[0][-1:] + righe[1]]
            y = 455 - 52 * len(righe) - (1 - comparsa) * 24
            for riga in righe:
                x = (W - cap.getlength(' '.join(w[0] for w in riga))) / 2
                for w in riga:
                    chiave = w[0].strip('.,?!').lower() in CHIAVE
                    detta = t >= w[1]
                    col = SCIARPA if chiave else INK
                    if not detta:
                        col = tuple(round(c + (BG[k] - c) * 0.55) for k, c in enumerate(col))
                    d.text((x, y), w[0], font=cap, fill=col)
                    x += cap.getlength(w[0] + ' ')
                y += 96
    # schede
    for s0, s1, grande, piccolo in SCHEDE:
        if s0 - 0.05 <= t <= s1:
            k = ease((t - s0) / 0.3)
            x0 = 560 + (1 - k) * 80; y0 = 640
            righe = piccolo.split('\n')
            h = 120 + 42 * len(righe)
            d.rounded_rectangle((x0, y0, x0 + 470, y0 + h), radius=26, fill=(255, 255, 255), outline=(232, 222, 210), width=3)
            d.rounded_rectangle((x0, y0, x0 + 14, y0 + h), radius=7, fill=ALLORO)
            fg = card_big
            if fg.getlength(grande) > 400:
                fg = ImageFont.truetype(F + 'InterDisplay-ExtraBold.otf', int(54 * 400 / fg.getlength(grande)))
            d.text((x0 + 44, y0 + 30 + (54 - fg.size) * 0.6), grande, font=fg, fill=SCIARPA)
            for i, r in enumerate(righe):
                d.text((x0 + 44, y0 + 102 + 42 * i), r, font=card_small, fill=INK)
    # barra di avanzamento
    d.rectangle((0, H - 10, W * min(1, t / DURATA), H), fill=ALLORO)
    return im

if __name__ == '__main__':
    out = os.path.join(S, f"aurelio-{EP['nome']}.mp4")
    n = round(DURATA * FPS)
    cmd = ['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
           '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-i', AUDIO,
           '-filter_complex', f'[1:a]apad=whole_dur={DURATA:.3f}[a]',
           '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '24',
           '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', '-t', f'{DURATA:.3f}', out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(quadro(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    print(out, f'{DURATA:.1f}s', p.returncode)
    if len(sys.argv) > 3:
        for t in map(float, sys.argv[3].split(',')):
            quadro(t).save(f'{S}/quadro-{t:05.1f}.png')

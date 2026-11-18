"""Anteprima video verticale 1080x1920 del Professor Aurelio: «Perché dimentichiamo i sogni?».

Apertura: voce A2 approvata (campione ElevenLabs). Resto: sottotitoli a tempo, senza voce,
finché ElevenLabs non torna disponibile. Nessuna voce sostitutiva.
"""
import math, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
sys.path.insert(0, sys.argv[1])
from anima import Figura
from disegni import SCENE, LATO

S = sys.argv[1]
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
APERTURA = [
    ("Ti sei mai chiesto perché il nostro cervello ci fa dimenticare i sogni?", 0.10, 3.44),
    ("E se ti dicessi che la risposta è nascosta proprio nel modo in cui dormiamo?", 3.68, 7.28),
]
RESTO = [
    ("apertura", "Te lo spiego io."),
    ("spiegazione", "I sogni più vividi nascono nella fase REM."),
    ("spiegazione", "Lì il cervello è attivissimo, ma una sostanza chiave per la memoria, la noradrenalina, quasi sparisce."),
    ("spiegazione", "Senza di lei, il sogno non viene fissato."),
    ("scoperta", "E c'è di più."),
    ("scoperta", "Nel 2019, uno studio sui topi ha scoperto un gruppo di neuroni che, proprio durante il sonno REM, lavora per farci dimenticare."),
    ("conclusione", "Ecco perché ricordi un sogno solo se ti svegli mentre lo stai facendo."),
    ("conclusione", "Il trucco? Tieni un quaderno accanto al letto, e scrivilo subito."),
]
CHIAVE = {"sogni", "rem", "noradrenalina", "2019", "neuroni", "dimenticare", "subito", "quaderno", "dormiamo", "sparisce"}
PPM = 175  # ritmo di riferimento per la parte non ancora narrata

def distribuisci(frase, t0, t1):
    ws = frase.split()
    pesi = [len(w) + 2 for w in ws]
    tot = sum(pesi); t = t0; out = []
    for w, p in zip(ws, pesi):
        d = (t1 - t0) * p / tot
        out.append((w, t, t + d)); t += d
    return out

parole = []
frasi = []  # (inizio, fine) di ogni frase, nell'ordine del copione
for frase, a, b in APERTURA:
    parole += [(w, s, e, 'apertura') for w, s, e in distribuisci(frase, a, b)]
    frasi.append((a, b))
FINE_VOCE = 7.63
t = FINE_VOCE + 0.15
for fase, frase in RESTO:
    n = len(frase.split())
    d = n * 60 / PPM
    parole += [(w, s, e, fase) for w, s, e in distribuisci(frase, t, t + d)]
    frasi.append((t, t + d))
    t += d + 0.25
DURATA_TESTO = t
CODA = 3.0
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

SCHEDE = [
    (t_parola('rem'), t_parola('senza'), "FASE REM", "il sogno più vivido"),
    (t_parola('noradrenalina'), t_parola('c\'è') - 0.3, "NORADRENALINA", "quasi a zero: il ricordo\nnon si fissa"),
    (t_parola('2019'), t_parola('ecco'), "2019", "studio sui topi:\nneuroni che fanno\ndimenticare"),
    (t_parola('quaderno'), DURATA_TESTO, "QUADERNO", "accanto al letto:\nscrivi il sogno subito"),
]

# ---------------------------------------------------------------- figura
figura = Figura(f'{S}/figura_pulita.png')
FIG_H = 1220
SCALA = FIG_H / figura.base.height
FIG_X, FIG_Y = 10, H - FIG_H - 20

# volume della voce, quadro per quadro, per muovere la bocca
pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', f'{S}/voci3/A2.mp3', '-ac', '1', '-ar', '16000', '-f', 's16le', '-'],
                     capture_output=True, check=True).stdout
campioni = np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768
passo = 16000 // FPS
VOLUME = np.array([np.sqrt(np.mean(campioni[i:i + passo] ** 2)) for i in range(0, len(campioni), passo)])
VOLUME = np.clip((VOLUME - 0.015) / (np.percentile(VOLUME, 95) - 0.015), 0, 1)

# scene: indice della frase -> disegno
SCENA_DI_FRASE = ['sogno', 'sogno', 'sogno', 'cervello', 'noradrenalina', 'ricordo', 'scoperta', 'scoperta', 'sveglia', 'quaderno']
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
    sc = frasi[6]; sc2 = frasi[7]
    if sc[0] - 0.1 <= t <= sc2[0] + 1.2:
        stupore = True
    trucco = frasi[9]
    if t >= trucco[0] + 1.2:
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
    # testata
    testo = "IL PROFESSOR AURELIO  ·  SCIENZA"
    tw = chip.getlength(testo)
    d.rounded_rectangle((60, 90, 60 + tw + 48, 146), radius=28, fill=(241, 233, 222))
    d.text((84, 100), testo, font=chip, fill=SAIO)
    if t > FINE_VOCE:
        avviso = "ANTEPRIMA · voce in arrivo"
        aw = fonte.getlength(avviso)
        d.rounded_rectangle((60, 160, 60 + aw + 40, 208), radius=24, fill=SCIARPA)
        d.text((80, 168), avviso, font=fonte, fill=(255, 245, 238))
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
    # chiusura
    if t > DURATA_TESTO:
        k = ease((t - DURATA_TESTO) / 0.5)
        for i, r in enumerate(["Perché dimentichiamo", "i sogni?"]):
            tw = titolo.getlength(r)
            d.text(((W - tw) / 2, 270 + i * 100 + (1 - k) * 30), r, font=titolo, fill=INK)
        d.line((W / 2 - 90, 488, W / 2 + 90, 488), fill=ALLORO, width=5)
        for i, r in enumerate(["Fonte: Izawa et al., Science, 2019", "(neuroni MCH e oblio nel sonno REM)"]):
            tw = fonte.getlength(r)
            d.text(((W - tw) / 2, 512 + i * 40), r, font=fonte, fill=TENUE)
    # barra di avanzamento
    d.rectangle((0, H - 10, W * min(1, t / DURATA), H), fill=ALLORO)
    return im

if __name__ == '__main__':
    out = f'{S}/aurelio-sogni-anteprima.mp4'
    n = round(DURATA * FPS)
    cmd = ['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
           '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-i', f'{S}/voci3/A2.mp3',
           '-filter_complex', f'[1:a]apad=whole_dur={DURATA:.3f},afade=t=out:st={FINE_VOCE - 0.1:.2f}:d=0.1[a]',
           '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '24',
           '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', '-t', f'{DURATA:.3f}', out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(quadro(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    print(out, f'{DURATA:.1f}s', p.returncode)
    if len(sys.argv) > 2:
        for t in map(float, sys.argv[2].split(',')):
            quadro(t).save(f'{S}/quadro-{t:05.1f}.png')

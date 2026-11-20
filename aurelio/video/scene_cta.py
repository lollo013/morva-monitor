"""Invito a commentare a meta' video: fumetto con la domanda e conto alla rovescia di 2 secondi. f(p, t, w, h, domanda, via)."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import ImageDraw
from scene_cielo import tela, fine, font, LINEA, CREMA, ORO, ROSSO, BLU, SS
from scene_inception import VERDE
from scene_procrastinazione import testo_c, SCURO, scala


def tc(d, x, y, s, n, col=SCURO, bordo=True):
    testo_c(d, x, y, s, font(n), col, bordo)


def a_capo(d, testo, f, larg):
    righe, r = [], ''
    for w in testo.split():
        prova = (r + ' ' + w).strip()
        if d.textlength(prova, font=f) <= larg: r = prova
        else: righe.append(r); r = w
    if r: righe.append(r)
    return righe


def commenta(p, t, w, h, domanda='Scrivilo nei commenti', via=0.7):
    """Fumetto con la domanda + icona commenti; da 'via' parte il conto alla rovescia 2, 1."""
    im, d = tela(w, h, (255, 246, 232, 255)); W, H = w * SS, h * SS; k = scala(w)
    # fumetto
    x0, y0, x1, y1 = W * 0.06, H * 0.05, W * 0.94, H * 0.5
    d.rounded_rectangle((x0, y0, x1, y1), radius=40 * SS, fill=(255, 255, 255, 255), outline=LINEA, width=7 * SS)
    d.polygon([(W * 0.2, y1 - 4 * SS), (W * 0.34, y1 - 4 * SS), (W * 0.16, y1 + H * 0.08)], fill=(255, 255, 255, 255))
    d.line([(W * 0.2, y1), (W * 0.16, y1 + H * 0.08), (W * 0.34, y1)], fill=LINEA, width=7 * SS)
    f = font(int(52 * k))
    righe = a_capo(d, domanda, f, (x1 - x0) * 0.86)
    y = (y0 + y1) / 2 - len(righe) * 34 * SS * k
    for r in righe:
        tc(d, W / 2, y, r, int(52 * k), SCURO, bordo=False); y += 68 * SS * k
    # icona commenti
    cx, cy = W * 0.78, H * 0.66
    d.ellipse((cx - W * 0.1, cy - H * 0.06, cx + W * 0.1, cy + H * 0.06), fill=BLU, outline=LINEA, width=5 * SS)
    for i in range(3):
        d.ellipse((cx - W * 0.055 + i * W * 0.045 - 8 * SS, cy - 8 * SS, cx - W * 0.055 + i * W * 0.045 + 8 * SS, cy + 8 * SS), fill=CREMA)
    tc(d, W * 0.42, H * 0.62, 'commenta', int(54 * k), BLU)
    # conto alla rovescia
    dur = (t / p) if p > 0 else 0
    if p >= via and dur > 0:
        s = (p - via) * dur
        n = 2 if s < 1 else (1 if s < 2 else 0)
        q = 1 + 0.25 * max(0, 1 - (s % 1) * 3)
        r = W * 0.15 * q
        cx, cy = W * 0.5, H * 0.85
        d.ellipse((cx - r, cy - r * 0.9, cx + r, cy + r * 0.9), fill=ROSSO if n else VERDE, outline=LINEA, width=6 * SS)
        tc(d, cx, cy - r * 0.62, str(n) if n else '✓', int(110 * k * q), CREMA, bordo=False)
    return fine(im, w, h)


SCENE = {'commenta': commenta}

if __name__ == '__main__':
    from PIL import Image
    a = commenta(0.5, 1.0, 420, 500, domanda='Tu come studi? Rileggi o ti interroghi?', via=0.7)
    b = commenta(0.85, 3.4, 420, 500, domanda='Tu come studi? Rileggi o ti interroghi?', via=0.7)
    tav = Image.new('RGB', (840, 500)); tav.paste(a, (0, 0)); tav.paste(b, (420, 0)); tav.save(sys.argv[1])

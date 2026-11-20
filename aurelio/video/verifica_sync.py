"""Verifica sottotitoli/voce: ogni 0,1 s confronta la parola pronunciata (tempi della trascrizione) con il sottotitolo mostrato."""
import sys, runpy, json
S, regia = sys.argv[1], sys.argv[2]
sys.argv = ['regia.py', S, regia]
g = runpy.run_path(f'{S}/regia.py', run_name='verifica')
parole, blocchi, FINE = g['parole'], g['blocchi'], g['FINE_VOCE']
frasi_intere = g.get('FRASI_INTERE', False)
def mostrato(t):
    return g['blocco_attivo'](t, 0.25 if frasi_intere else 0.12)
errori, campioni, ritardo_max = [], 0, 0.0
t = 0.0
while t < FINE:
    w = next((p for p in parole if p[1] <= t < p[2]), None)
    if w:
        campioni += 1
        b = mostrato(t)
        if not b or w not in b:
            errori.append((round(t, 1), w[0], ' '.join(x[0] for x in b) if b else '-'))
    t += 0.1
# il sottotitolo compare prima o insieme alla parola?
for b in blocchi:
    ritardo_max = max(ritardo_max, 0.04 - 0.04)
print(f'{regia.split("/")[-1]}: {campioni} istanti controllati, {len(errori)} non allineati')
for e in errori[:10]: print('  ', e)

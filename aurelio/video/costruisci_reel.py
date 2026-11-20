"""Regia di un reel da una scheda JSON. Uso: costruisci_reel.py <cartella> <scheda.json> [stima]
La scheda ha: nome, frasi (come si leggono a schermo), equivalenze (scritto -> pronunciato), piano [[frase, parola|null, tipo, scena|null, extra]],
chiave, stupore [[frase, parola], [frase, parola]], sorriso [frase, parola]."""
import json, re, subprocess, sys
S, scheda = sys.argv[1], json.load(open(sys.argv[2]))
STIMA = len(sys.argv) > 3 and sys.argv[3] == 'stima'
nome, frasi, eq = scheda['nome'], scheda['frasi'], scheda.get('equivalenze', {})
R = {'nome': nome, 'audio': f'{nome}.mp3', 'tempi_parole': f'tempi-{nome}.json'}
if STIMA:
    t = 0.05; tempi = []
    for f in frasi:
        for w in f.split():
            pul = w.strip('.,:;?!')
            n = len(eq.get(pul, pul))
            d = (n + 1) / 19.0
            tempi.append([w, round(t, 3), round(t + d, 3)]); t += d
            t += 0.32 if re.search(r'[.?!]$', w) else (0.14 if re.search(r'[,:;]$', w) else 0)
    json.dump(tempi, open(f'{S}/tempi-{nome}-stima.json', 'w'), ensure_ascii=False)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi', '-t', f'{t + 0.1:.2f}', '-i', 'anullsrc=r=44100:cl=mono',
                    '-c:a', 'libmp3lame', '-b:a', '64k', f'{S}/{nome}-muto.mp3'], check=True)
    R = {'nome': f'{nome}-anteprima', 'audio': f'{nome}-muto.mp3', 'tempi_parole': f'tempi-{nome}-stima.json'}
    print('durata stimata', round(t, 1))
norm = lambda w: re.sub(r"[^\w']", '', w.lower())
def A(i, parola):
    n = 0
    for j, f in enumerate(frasi):
        for w in f.split():
            if norm(w) == parola:
                n += 1
                if j == i: return parola if n == 1 else f'{parola}#{n}'
    raise SystemExit(f'manca «{parola}» nella frase {i}: {frasi[i]}')
inq = []
for i, par, tipo, scena, extra in scheda['piano']:
    x = {'da': 0 if par is None else A(i, par), 'tipo': tipo}
    if scena: x['scena'] = scena
    x.update(extra or {}); inq.append(x)
R.update({'equivalenze': {norm(k): v for k, v in eq.items()}, 'frasi': frasi, 'inquadrature': inq, 'chiave': scheda['chiave'],
          'stupore': [A(*scheda['stupore'][0]), A(*scheda['stupore'][1])], 'sorriso_da': A(*scheda['sorriso']), 'coda': 0.8})
json.dump(R, open(f"{S}/regia-{R['nome']}.json", 'w'), ensure_ascii=False, indent=1)

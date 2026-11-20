"""Regia del reel «I voti misurano davvero l'intelligenza?». Con 'stima' crea tempi stimati e audio muto per l'anteprima."""
import json, re, subprocess, sys
S = sys.argv[1]; STIMA = len(sys.argv) > 2 and sys.argv[2] == 'stima'
frasi = ["Lo stesso compito, corretto da 73 professori.", "Voti?", "Dal 5 al 9 e mezzo.",
"Allora, i voti misurano davvero quanto sei intelligente?", "Non è un caso isolato.",
"Già nel 1912, due ricercatori diedero lo stesso tema a più di cento insegnanti: i voti erano lontanissimi tra loro.",
"E perfino lo stesso professore, ricorreggendo lo stesso compito settimane dopo, spesso dà un voto diverso.",
"Un voto dipende anche da chi lo dà.", "E c'è di più.",
"Uno studio su ragazzi di terza media ha scoperto che, per prevedere i voti di fine anno, contava più la costanza del quoziente intellettivo.",
"Il voto misura anche quanto sei organizzato, puntuale, costante.", "Non quanto vali.",
"Quindi un brutto voto non dice che sei stupido.", "Dice su cosa puoi lavorare.",
"E la costanza, a differenza del talento, si allena.", "Prova così: una materia, venti minuti al giorno, per due settimane.",
"Poi guarda il voto.", "Se ti è stato utile, seguimi!"]
PARLATO = {'73': 'settantatré', '5': 'cinque', '9': 'nove', '1912': 'millenovecentododici'}
R = {'nome': 'voti', 'audio': 'voti.mp3', 'tempi_parole': 'tempi-voti.json'}
if STIMA:
    t = 0.05; tempi = []
    for f in frasi:
        for w in f.split():
            pulita = w.strip('.,:;?!')
            n = len(PARLATO.get(pulita, pulita))
            d = (n + 1) / 19.0
            tempi.append([w, round(t, 3), round(t + d, 3)]); t += d
            t += 0.32 if re.search(r'[.?!]$', w) else (0.14 if re.search(r'[,:;]$', w) else 0)
    json.dump(tempi, open(f'{S}/tempi-voti-stima.json', 'w'), ensure_ascii=False)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi', '-t', f'{t + 0.1:.2f}', '-i', 'anullsrc=r=44100:cl=mono',
                    '-c:a', 'libmp3lame', '-b:a', '64k', f'{S}/voti-muto.mp3'], check=True)
    R = {'nome': 'voti-anteprima', 'audio': 'voti-muto.mp3', 'tempi_parole': 'tempi-voti-stima.json'}
    print('durata stimata', round(t, 1))
norm = lambda w: re.sub(r"[^\w']", '', w.lower())
def A(i, parola):
    n = 0
    for j, f in enumerate(frasi):
        for w in f.split():
            if norm(w) == parola:
                n += 1
                if j == i: return parola if n == 1 else f'{parola}#{n}'
    raise SystemExit(f'manca {parola} nella frase {i}')
P = [(0, None, 'angolo_dx', 'compito_voti', {'testo_grande': 'Stesso compito,|voti dal 5 al 9½'}),
 (1, 'voti', 'primo_piano', None, {}), (2, 'dal', 'angolo_dx', 'scala_voti', {}), (3, 'allora', 'primo_piano', None, {}),
 (4, 'caso', 'affiancati', 'anno1912', {}), (5, 'già', 'angolo_sx', 'anno1912', {}), (5, 'voti', 'mezzo_busto', 'anno1912', {}),
 (6, 'perfino', 'affiancati', 'stesso_prof', {}), (6, 'settimane', 'angolo_dx', 'stesso_prof', {}),
 (7, 'dipende', 'mezzo_busto', 'chi_lo_da', {}), (8, 'più', 'primo_piano', None, {}),
 (9, 'studio', 'angolo_sx', 'costanza_qi', {}), (9, 'prevedere', 'affiancati', 'costanza_qi', {}), (9, 'costanza', 'mezzo_busto', 'costanza_qi', {}),
 (10, 'misura', 'angolo_dx', 'cosa_misura', {}), (11, 'non', 'affiancati', 'cosa_misura', {}),
 (12, 'quindi', 'primo_piano', None, {}), (12, 'stupido', 'angolo_sx', 'brutto_voto', {}), (13, 'lavorare', 'mezzo_busto', 'brutto_voto', {}),
 (14, 'allena', 'affiancati', 'allena', {}), (15, 'prova', 'angolo_dx', 'allena', {}), (15, 'venti', 'mezzo_busto', 'allena', {}),
 (16, 'guarda', 'primo_piano', None, {}), (17, 'se', 'mezzo_busto', 'invito', {})]
inq = []
for i, par, tipo, scena, extra in P:
    x = {'da': 0 if par is None else A(i, par), 'tipo': tipo}
    if scena: x['scena'] = scena
    x.update(extra); inq.append(x)
R.update({'frasi': frasi, 'inquadrature': inq, 'stupore': [A(8, 'più'), A(9, 'costanza')], 'sorriso_da': A(17, 'se'), 'coda': 0.8,
          'chiave': ['compito', 'voti', 'intelligente', 'insegnanti', 'diverso', 'dipende', 'costanza', 'quoziente', 'organizzato',
                     'puntuale', 'costante', 'vali', 'stupido', 'lavorare', 'allena', 'venti', 'settimane', 'utile', 'seguimi']})
json.dump(R, open(f"{S}/regia-{R['nome']}.json", 'w'), ensure_ascii=False, indent=1)

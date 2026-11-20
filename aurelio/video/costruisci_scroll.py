"""Costruisce la regia del reel «scroll». Con un argomento 'stima' crea anche tempi stimati e un audio muto per l'anteprima."""
import json, re, subprocess, sys
S = sys.argv[1]; STIMA = len(sys.argv) > 2 and sys.argv[2] == 'stima'
frasi = ["Il tuo telefono funziona come una slot machine.","E tu ci giochi ogni giorno.","Perché non riusciamo a smettere di scrollare?",
"Apri un video, poi un altro, e all'improvviso è passata un'ora.","Tranquillo: non è colpa tua.","È progettato così.",
"Il trucco si chiama ricompensa variabile.","Lo scoprì lo psicologo Skinner, negli anni Trenta: se un premio arriva a caso, continui a cercarlo molto più che se arriva sempre.",
"È lo stesso meccanismo delle slot machine.","E la dopamina?","Non è il piacere: è l'attesa.",
"Si accende soprattutto quando il premio è incerto: forse il prossimo video sarà quello giusto.",
"Poi c'è lo scroll infinito: nessuna fine pagina, nessun segnale di stop.","L'ha inventato nel 2006 un designer, Aza Raskin.",
"E oggi dice di essersene pentito.","Come difendersi?",
"Metti lo schermo in bianco e nero: negli studi, si usa il telefono dai venti ai cinquanta minuti in meno al giorno.",
"Senza colori, il premio attira meno.","E togli le notifiche delle app che ti rubano più tempo.","Se ti è stato utile, seguimi!"]
R = {'nome': 'scroll', 'audio': 'scroll.mp3', 'tempi_parole': 'tempi-scroll.json'}
if STIMA:
    # ritmo della voce A2 misurato sui reel precedenti: circa 1.000 caratteri in 57 secondi, pause comprese
    t = 0.05; tempi = []
    for f in frasi:
        for w in f.split():
            n = len('duemilasei') if w == '2006' else len(w.strip('.,:;?!'))
            d = (n + 1) / 19.0
            tempi.append([w, round(t, 3), round(t + d, 3)]); t += d
            t += 0.32 if re.search(r'[.?!]$', w) else (0.14 if re.search(r'[,:;]$', w) else 0)
    json.dump(tempi, open(f'{S}/tempi-scroll-stima.json', 'w'), ensure_ascii=False)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi', '-t', f'{t + 0.1:.2f}', '-i', 'anullsrc=r=44100:cl=mono',
                    '-c:a', 'libmp3lame', '-b:a', '64k', f'{S}/scroll-muto.mp3'], check=True)
    R = {'nome': 'scroll-anteprima', 'audio': 'scroll-muto.mp3', 'tempi_parole': 'tempi-scroll-stima.json'}
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
P = [(0, None, 'sfondo', 'slot_telefono', {'testo_grande': 'Il tuo telefono|è una slot machine'}),
 (1, 'giochi', 'primo_piano', None, {}), (2, 'perché', 'angolo_dx', 'scroll_ora', {}), (3, 'apri', 'affiancati', 'scroll_ora', {}),
 (3, 'passata', 'angolo_sx', 'scroll_ora', {}), (4, 'tranquillo', 'primo_piano', None, {}), (5, 'progettato', 'mezzo_busto', 'progettato', {}),
 (6, 'trucco', 'angolo_dx', 'premio', {}), (7, 'psicologo', 'affiancati', 'premio', {}), (7, 'se', 'angolo_sx', 'premio', {}),
 (8, 'meccanismo', 'mezzo_busto', 'slot_feed', {}), (9, 'dopamina', 'primo_piano', None, {}), (10, 'piacere', 'angolo_dx', 'dopamina', {}),
 (11, 'accende', 'affiancati', 'dopamina', {}), (11, 'forse', 'angolo_sx', 'dopamina', {}), (12, 'scroll', 'mezzo_busto', 'infinito', {}),
 (12, 'nessun', 'angolo_dx', 'infinito', {}), (13, 'inventato', 'affiancati', 'inventore', {}), (14, 'oggi', 'angolo_sx', 'inventore', {}),
 (15, 'difendersi', 'primo_piano', None, {}), (16, 'metti', 'mezzo_busto', 'bianco_nero', {}), (16, 'studi', 'angolo_dx', 'bianco_nero', {}),
 (17, 'colori', 'affiancati', 'bianco_nero', {}), (18, 'togli', 'angolo_sx', 'notifiche', {}), (19, 'se', 'mezzo_busto', 'invito', {})]
inq = []
for i, par, tipo, scena, extra in P:
    x = {'da': 0 if par is None else A(i, par), 'tipo': tipo}
    if scena: x['scena'] = scena
    x.update(extra); inq.append(x)
R.update({'equivalenze': {"machine": "mascìne", "skinner": "skìnner", "2006": "duemilasei", "designer": "disàiner", "aza": "àsa", "raskin": "ràskin"}, 'frasi': frasi, 'inquadrature': inq, 'stupore': [A(9, 'dopamina'), A(10, 'piacere')], 'sorriso_da': A(19, 'se'), 'coda': 0.8,
          'chiave': ['slot', 'machine', 'scrollare', 'colpa', 'progettato', 'ricompensa', 'variabile', 'caso', 'dopamina', 'incerto',
                     'infinito', 'stop', 'pentito', 'bianco', 'nero', 'venti', 'cinquanta', 'notifiche', 'utile', 'seguimi']})
json.dump(R, open(f"{S}/regia-{R['nome']}.json", 'w'), ensure_ascii=False, indent=1)

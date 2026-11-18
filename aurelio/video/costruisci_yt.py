import json, re, sys
EN = len(sys.argv) > 4 and sys.argv[4] == 'en'
testo = open(sys.argv[1]).read()
testo = re.sub(r'\[[^\]]+\]\s*', '', testo).replace('CENTODICIOTTOMILA', 'centodiciottomila').replace('QUANDO', 'quando').replace('ONE HUNDRED EIGHTEEN THOUSAND', 'one hundred eighteen thousand').replace('WHEN', 'when')
frasi = [f.strip() for f in re.findall(r'[^.?!]+[.?!]', testo)]
norm = lambda w: re.sub(r"[^\w']", '', w.lower())
def ancora(i, parola):
    """parola nella frase i -> 'parola#n' contando le occorrenze precedenti"""
    n = 0
    for j, f in enumerate(frasi):
        for w in f.split():
            if norm(w) == parola:
                n += 1
                if j == i: return f'{parola}#{n}' if n > 1 else parola
    raise SystemExit(f'manca {parola} in frase {i}: {frasi[i]}')
def trova(frammento):
    for i, f in enumerate(frasi):
        if frammento.lower() in f.lower(): return i
    raise SystemExit('frase non trovata: ' + frammento)
piano = json.load(open(sys.argv[2]))
inq = []
for x in piano:
    fr, parola = x.pop('frase'), x.pop('parola')
    i = trova(fr)
    x['da'] = 0 if not inq else ancora(i, norm(parola))
    for k, v in list(x.get('eventi', {}).items()):
        x['eventi'][k] = ancora(trova(v[0]), norm(v[1]))
    inq.append(x)
chiave = ["interesse", "composto", "meraviglia", "futuro", "sicuro", "mille", "quattro", "quaranta", "interessi", "neve", "settantadue",
          "raddoppi", "diciotto", "anna", "marco", "centodiciottomila", "sessantanovemila", "cinquantamila", "quando", "inflazione",
          "seimilasettecento", "otto", "emergenza", "debiti", "primo", "rischio", "zero", "scala", "centomila", "stato", "azioni",
          "diversifica", "costi", "cinquantottomila", "truffa", "consulenza", "professionista", "iscriviti", "commenti", "piace"]
if EN:
    chiave = ["compound", "interest", "wonder", "future", "safe", "thousand", "four", "forty", "snowball", "seventytwo", "double",
              "eighteen", "anna", "mark", "sixtynine", "fifty", "when", "inflation", "eight", "emergency", "debt", "first", "risk",
              "zero", "ladder", "protected", "bonds", "stocks", "diversify", "fees", "fiftyeight", "scam", "advice", "professional",
              "like", "subscribe", "comments"]
    out = {"nome": "youtube-compound-interest", "formato": "youtube", "audio": "youtube-compound-interest.mp3", "frasi": frasi,
           "chiave": chiave, "inquadrature": inq, "stupore": [ancora(trova('Now look'), 'now'), ancora(trova('Anna starts'), 'anna')],
           "sorriso_da": ancora(trova('If this video'), 'if'), "coda": 1.0}
else:
    out = {"nome": "youtube-interesse-composto", "formato": "youtube", "audio": "youtube-interesse-composto.mp3", "frasi": frasi,
           "chiave": chiave, "inquadrature": inq, "stupore": [ancora(trova('Adesso guarda'), 'adesso'), ancora(trova('Anna comincia'), 'anna')],
           "sorriso_da": ancora(trova('Se questo video'), 'se'), "coda": 1.0}
json.dump(out, open(sys.argv[3], 'w'), ensure_ascii=False, indent=1)
print(len(frasi), 'frasi,', len(inq), 'inquadrature')

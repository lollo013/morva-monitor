"""Pagina privata di un reel, dal modello di quella della procrastinazione. Uso: pagina_reel.py <S> <nome> <durata> <titolo> <file.json corpo>"""
import json, sys
S, nome, durata, titolo, corpo_json = sys.argv[1:6]
c = json.load(open(corpo_json))
s = open(f'{S}/pagina-procrastinazione/index.html').read()
a = s.index('<div class="occhiello">'); b = s.index('</main>')
li = lambda xs: ''.join(f'        <li>{x}</li>\n' for x in xs)
corpo = f'''<div class="occhiello">Anteprima privata · TikTok/Reels 9:16 · {durata}</div>
    <h1>{titolo}</h1>
    <p>{c["intro"]}</p>
    <div class="blocco">
      <h2>Cosa spiega</h2>
      <ul>
{li(c["punti"])}      </ul>
    </div>
    <div class="blocco">
      <h2>Formato TikTok</h2>
      <p>9:16, 1080×1920, tutto il necessario dentro l'area sicura (rettangolo verde).</p>
      <img src="area-sicura.jpg" alt="Fotogrammi con l'interfaccia di TikTok simulata e l'area sicura" style="width:100%;border-radius:8px;margin-top:10px">
    </div>
    <div class="blocco">
      <h2>Fonti (solo per te, non nel video)</h2>
      <ul>
{li(c["fonti"])}      </ul>
    </div>
  </div>
'''
s = s[:a] + corpo + s[b:]
s = s.replace('professor-aurelio-procrastinazione.mp4', f'professor-aurelio-{nome}.mp4')
s = s.replace("<title>Aurelio · Studiare all'ultimo</title>", f"<title>Aurelio · {c['titolo_breve']}</title>")
import os; os.makedirs(f'{S}/pagina-{nome}', exist_ok=True)
open(f'{S}/pagina-{nome}/index.html', 'w').write(s)

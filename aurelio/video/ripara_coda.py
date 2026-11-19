import sys, runpy, subprocess
S, regia_json = sys.argv[1], sys.argv[2]
sys.argv = ['regia.py', S, regia_json]
g = runpy.run_path(f'{S}/regia.py', run_name='parziale')
SHOT, FPS, W, H, DURATA, quadro = g['SHOT'], g['FPS'], g['W'], g['H'], g['DURATA'], g['quadro']
t0 = next(s['inizio'] for s in SHOT if s.get('scena') == 'iscriviti_en')
i0 = int(t0 * FPS)
out = f'{S}/coda.mp4'
p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                      '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
for i in range(i0, round(DURATA * FPS)):
    p.stdin.write(quadro(i / FPS).tobytes())
p.stdin.close(); p.wait()
print(i0 / FPS)

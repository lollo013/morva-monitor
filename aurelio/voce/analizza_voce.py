"""Profilo acustico della voce A2 del Professor Aurelio, misurato sulle narrazioni prodotte."""
import json, re, subprocess, sys
import numpy as np
S = sys.argv[1]
clip = {'sogni': ('narrazione.mp3', 121), 'cipolla': ('cipolla.mp3', 146), 'cielo': ('cielo.mp3', 77),
        'inception': ('inception.mp3', 315), 'fortnite': ('fortnite-v4.mp3', 191)}
def pcm(f, sr=16000):
    b = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', str(sr), '-f', 's16le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(b, dtype=np.int16).astype(np.float32) / 32768, sr
def f0(x, sr):
    out = []; n = int(0.04 * sr); hop = int(0.01 * sr)
    lo, hi = int(sr / 300), int(sr / 60)   # 60-300 Hz: voce maschile
    for i in range(0, len(x) - n, hop):
        fr = x[i:i + n] * np.hanning(n)
        if np.sqrt(np.mean(fr ** 2)) < 0.02: continue
        ac = np.correlate(fr, fr, 'full')[n - 1:]
        if ac[0] <= 0: continue
        k = lo + int(np.argmax(ac[lo:hi]))
        if ac[k] / ac[0] > 0.45: out.append(sr / k)
    return np.array(out)
def silenzi(f):
    e = subprocess.run(['ffmpeg', '-hide_banner', '-i', f, '-af', 'silencedetect=noise=-38dB:d=0.15', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return [float(v) for v in re.findall(r'silence_duration: ([0-9.]+)', e)]
def loud(f):
    e = subprocess.run(['ffmpeg', '-hide_banner', '-i', f, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    m = re.findall(r'I:\s+(-?[0-9.]+) LUFS', e)
    return float(m[-1]) if m else None
tutti = []; righe = {}
for nome, (f, parole) in clip.items():
    x, sr = pcm(f'{S}/{f}'); d = len(x) / sr
    p = f0(x, sr); tutti.append(p); s = silenzi(f'{S}/{f}')
    righe[nome] = {'durata_s': round(d, 1), 'parole_al_minuto': round(parole / d * 60),
                   'f0_mediana_hz': round(float(np.median(p)), 1), 'f0_p10_p90_hz': [round(float(np.percentile(p, 10)), 1), round(float(np.percentile(p, 90)), 1)],
                   'pause_oltre_0_15s': len(s), 'pausa_media_s': round(float(np.mean(s)), 2) if s else 0, 'pausa_max_s': round(max(s), 2) if s else 0,
                   'loudness_lufs': loud(f'{S}/{f}')}
p = np.concatenate(tutti)
semitoni = 12 * np.log2(np.percentile(p, 90) / np.percentile(p, 10))
profilo = {
  'voce': 'Professor Aurelio — A2', 'elevenlabs_voice_id': 'Urn0f9O0p74gbKH8ERH3', 'modello': 'eleven_v3',
  'impostazioni': {'stability': 0.5, 'similarity_boost': 0.8, 'style': 0},
  'misure_complessive': {
    'f0_mediana_hz': round(float(np.median(p)), 1),
    'f0_p10_p90_hz': [round(float(np.percentile(p, 10)), 1), round(float(np.percentile(p, 90)), 1)],
    'escursione_intonazione_semitoni': round(float(semitoni), 1),
    'parole_al_minuto_media': round(np.mean([r['parole_al_minuto'] for r in righe.values()])),
  },
  'per_video': righe,
  'campioni_di_riferimento': {n: f for n, (f, _) in clip.items()},
  'nota': 'Profilo misurato, non un modello: serve a controllare che ogni nuova narrazione resti coerente (tono, velocità, pause, volume).'
}
print(json.dumps(profilo, ensure_ascii=False, indent=1))
json.dump(profilo, open(f'{S}/profilo-voce.json', 'w'), ensure_ascii=False, indent=1)

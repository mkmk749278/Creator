#!/usr/bin/env python3
"""Labelled contact sheets: one row per clip, 6 frames across, with file name, size and duration (PLAYBOOK §4: a contact
sheet of every asset before use). usage: contact_sheet.py OUT_PREFIX clip.mp4 [clip.mp4 ...]  (12 clips a sheet)"""
import subprocess, sys, json, os, tempfile
from PIL import Image, ImageDraw, ImageFont
out, clips = sys.argv[1], sys.argv[2:]
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
TW, TH, N = 320, 180, 6
def probe(p):
    j = json.loads(subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height:format=duration','-of','json',p],capture_output=True,text=True).stdout)
    return j['streams'][0]['width'], j['streams'][0]['height'], float(j['format']['duration'])
for s in range(0, len(clips), 12):
    batch = clips[s:s+12]; sheet = Image.new('RGB', (TW*N, len(batch)*(TH+26)), 'black'); d = ImageDraw.Draw(sheet)
    for r, c in enumerate(batch):
        w, h, dur = probe(c); y = r*(TH+26)
        d.text((4, y+3), f"{os.path.basename(c)}   {w}x{h}   {dur:.1f}s", fill='white', font=F)
        for k in range(N):
            t = dur*(k+0.5)/N
            with tempfile.NamedTemporaryFile(suffix='.jpg') as tf:
                subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{t:.2f}','-i',c,'-frames:v','1','-vf',f'scale={TW}:{TH}:force_original_aspect_ratio=decrease,pad={TW}:{TH}:(ow-iw)/2:(oh-ih)/2',tf.name])
                try: sheet.paste(Image.open(tf.name), (k*TW, y+26))
                except Exception: pass
    sheet.save(f"{out}_{s//12+1}.jpg", quality=82)
    print(f"{out}_{s//12+1}.jpg", len(batch))

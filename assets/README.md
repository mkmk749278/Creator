# Owner footage: drop files here, rebuild, done

The documentary engine (`video/doc/`) uses these exact paths first. Any file that is missing is
covered by licensed real media (Wikimedia Commons, Flickr CC, archive.org), each labelled honestly
on screen ("ARCHIVE PHOTO · 2013", "ILLUSTRATIVE", "B-ROLL").

| File | Used for (video time) |
|---|---|
| `video/vidyut_stage_trance.mp4` | 00:23–01:20 claim + stage, 01:20–01:38 the hold, 03:31 "no oxygen tank", 06:02–07:16 message and end |
| `video/vidyut_tears_macro.mp4` | 00:35 tears, 01:38–01:50 open eyes / tears, Trataka and gaze shots in Scene 3 |
| `video/vidyut_shivering.mp4` | 01:50–02:04 minute-14 tremor, 02:53 diaphragm spasm cutaways |
| `video/vidyut_shankha.mp4` | 02:04–02:07 and the **3 s live pause at 02:07** (its own audio plays at full level) |
| `video/vidyut_kalari.mp4` | 05:13–06:02 Kalaripayattu montage, 06:43 closing montage |
| `video/vidyut_workouts.mp4` | 05:21–06:02 calisthenics / animal flow |
| `video/freediver_pool.mp4` | 00:00–00:23 opening, 02:18 science intro, **split screen left (11:35)** |
| `video/o2_mask_breathing.mp4` | **split screen right (24:37, pure O₂ first)** |
| `video/city_rush_timelapse.mp4` | 06:20–06:30 and 06:33–06:47 rush vs stillness |
| `images/sadhu_haridas_1837.jpg` | 04:55–05:10 slow horizontal pan |
| `images/patanjali_manuscript.jpg` | 03:38–03:53 and 04:11–04:28 slow Ken Burns |

Any length and resolution works (1080p+ recommended). Videos are cut into 2.5–3.5 s shots at
different offsets automatically. For `vidyut_shankha.mp4`, keep the conch blast near the start.

**Rights:** event footage belongs to whoever filmed it. Use clips you have permission for, or
the official posts by Vidyut Jammwal / Paramount Pictures India, credited on screen.

## Rebuild
```bash
python video/doc/make_registry.py      # picks up new files
node video/doc/build.mjs               # cuts shots, writes parts, live audio, credits
npm run vendor
for p in p1 p2 p3 p4 p5 p6 p7 p8; do (cd video/doc/$p && npx hyperframes render --workers 4 --quality standard --output ../../../runs/breath-hold/doc/parts/$p.mp4); done
LIVE=runs/breath-hold/doc/live.wav scripts/final_mix.sh runs/breath-hold/doc/breath_hold_doc_1080p.mp4 runs/breath-hold/doc/voice_paused.wav runs/breath-hold/doc/bed.wav runs/breath-hold/doc/parts/p{1..8}.mp4
```

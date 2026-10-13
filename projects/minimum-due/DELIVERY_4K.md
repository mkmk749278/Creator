# Minimum Due: 4K master (2026-10-13)

**Download:** https://gofile.io/d/KsZ4AWDa

| | |
|---|---|
| File | `minimum-due-refined-master.mp4` (md5 `549f4e6ce6f10099c85a1f42964176ec`) |
| Picture | 3840×2160, 30 fps, H.264 at 20 Mbps (capped), 14,544 frames |
| Length | 8:04.8 (484.80 s), the same as the approved refined preview |
| Size | 1.21 GB |
| Loudness | −14.2 LUFS integrated, true peak −0.5 dBFS, AAC 160 kb/s |
| Edit | The approved refined cut (`build/assemble.py --refined --height 2160`), unchanged |

**How it was made:** the 14 animations (3 money scenes and 11 doodle boards) were rendered natively at 3840×2160 by three
shard sessions (`minimum-due-4k-r1`…`r3`, md5-checked on arrival). Real footage and photos were re-encoded at 4K from
their sources, with every encode bitrate-capped (shots at 30 Mbps, master at 20 Mbps). The build never used
`--resolution 4k`.

**Stand-ins:** none. All the real Commons photos are in: Supreme Court of India (supreme_court_03) and the HDFC branch
(bank_01) were re-downloaded at a polite rate, one 429 then a successful retry. bank_01 is only 1280 px wide at source,
so it is softer than the rest at 4K. That is the source's limit.

**Checks:** the audio-synced frame review (`build/review_av.py`, 1 frame per second, 41 sheets) was read in full. Every
frame shows what the VO says at that second, with no blanks (beyond the boards' own sub-second erase beats), crops or
misplaced labels. Shot frame counts add up to exactly the film length, so there is no drift against the VO.

**Fixed during the build** (in `build/assemble.py`):
- `--skip-boards` now also skips money scenes whose 4K render has not arrived yet.
- Board and scene shots hold their last frame when a window runs past the render's end. The 4K b05 render is 0.11 s
  shorter than its last window.
- Board and scene shots get their exact frame count. `-t` after a mid-frame seek had dropped one frame on 6 shots, so
  later cuts drifted up to 0.2 s early.

**Open (not changed, because the cut is approved):** the audio ends with the VO at 479.1 s, so the last 5.7 s of the end
card has no audio. The music bed stops when the voice stops, because the mix uses `amix duration=first`. The approved
preview has the same tail. If the owner wants the bed to run under the end card, the fix is a one-line change to the
mix (`duration=longest`, trimmed to the film length), followed by a re-mux. No shots need re-rendering.

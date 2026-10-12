# YouTube upload checklist: Minimum Amount Due

Everything for the upload is in this folder. Steps work in the YouTube Studio app on a phone; Test & Compare needs
desktop Studio.

## Files
| What | Where |
|---|---|
| Video, 4K master (3840×2160, 30 fps, about 20 Mbps, −14 LUFS) | Gofile link in the session report; `assets/minimum-due-refined-master.mp4` |
| 720p review copy | Gofile link in the session report |
| Thumbnail, main | `thumbnail_A.jpg` (1280×720) — "PAID ONLY ₹1,500 · BILL WENT UP · ₹30,000 → ₹30,481" |
| Thumbnail, test | `thumbnail_B.jpg` (1280×720) — "MINIMUM DUE TRAP? · 45% INTEREST" |
| Title, description, chapters, tags, pinned comment | `description.md` |
| English subtitles | `subtitles.en.srt` (from the VO timing; 155 cues) |

## Upload steps
1. Upload the 4K master. While it processes, set the **title** (option A in `description.md`) and paste the
   **description** (between the lines). The chapters are inside it and start at 0:00, so YouTube picks them up.
2. **Thumbnail:** `thumbnail_A.jpg`. On desktop Studio, add `thumbnail_B.jpg` in **Test & Compare** (judged on
   watch-time share).
3. **Audience:** No, it's not made for kids. **Category:** Education. **Video language** and **caption language:**
   English (India).
4. **Subtitles:** upload `subtitles.en.srt` as "English (India)" (Subtitles → Upload file → With timing).
5. **Tags:** paste the tag line from `description.md`.
6. **Altered or synthetic content:** the narration is an AI voice (ElevenLabs) reading Kishore's script, and the phone
   and bill screens are labelled simulations. No real person or real event is faked, so YouTube's box is not required.
   The description says so openly (channel rule). Tick "Yes" if you prefer full transparency in the label as well.
7. **Paid promotion:** No. **Comments:** On. After publishing, post and pin the comment from `description.md`.
8. **End screen** (last 12 s, from 7:52): add a "subscribe" element and a "next video" element, left and right of the
   logo (the logo sits upper-middle and the text lower-middle). The end card says "Next: can't pay even the
   minimum?"; link that video once it is out.
9. **Shorts (optional):** the phone-payment scene (0:04–0:19) and the ₹100 split (4:25–4:40) work as 9:16 cut-downs.

## What the thumbnail promises, and where the film delivers it
- ₹1,500 minimum on the phone: 0:04 (the bill) and 0:15 ("₹1,500 paid, still pending ₹28,500").
- "Bill went up", ₹30,000 → ₹30,481: the trap is set up by 0:22 (ICICI's own example) and worked out at 3:13–3:33
  (the next-bill ledger).
- Variant B, "45% interest": 2:48 (ICICI's rate page, then the rate chip).

## Facts and labels (already in the film)
Every on-screen number comes from `claims.csv` or `tools/mad_math.py` (OUR CALCULATION). The ICICI example and our
₹30,000 example carry separate labels. "Educational only, not financial advice" is on the end card and in the
description.

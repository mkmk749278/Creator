# Fetching a YouTube video for study

For analysing how other channels make their videos (shots, camera moves, lip-sync, rigs).
**Analysis only.** Never put other creators' footage in our videos (CLAUDE.md content rules).

## Run it (phone)
GitHub app → Actions → **Fetch video for study** → Run workflow → paste the URL.
The run Summary shows the result. The artifact `fetched-video` has `video.mp4`, `frames/` (timestamped,
every N seconds) and `sheet-NN.jpg` contact sheets (30 frames each).

## Why it fails without setup
YouTube blocks most datacenter IPs (GitHub runners, cloud containers) with
"Sign in to confirm you're not a bot". Third-party download sites don't help: savefrom.net blocks
US IPs and cobalt requires a captcha. The fixes below are the ones yt-dlp documents.

### Fix 1: signed-in cookies (recommended)
1. Create a **throwaway** Google account. YouTube can flag accounts used for downloading,
   so never use your main or channel account.
2. In a browser that supports add-ons (for example Firefox for Android), sign in to youtube.com with
   that account in a **private window**, export cookies in Netscape `cookies.txt` format with a
   "cookies.txt" export add-on, then close the private window. Closing it stops YouTube rotating those cookies.
3. Repo → Settings → Secrets and variables → Actions → New secret `YT_COOKIES` → paste the file contents.
4. Re-export when runs start failing with the bot check again (cookies expire).

### Fix 2: run on the VPS
Choose `runner: self-hosted`. This only helps if the VPS IP isn't flagged; many VPS IPs are.
Combine it with cookies for the best chance.

### Fallback: the phone itself (mobile IP, rarely blocked)
In Termux:
```bash
pkg install python ffmpeg nodejs && pip install "yt-dlp==2026.8.19"
yt-dlp --js-runtimes node -f "bv*[height<=720]+ba/b" -o "/sdcard/Download/%(id)s.%(ext)s" URL
```
Then upload the file to Google Drive and give Claude the file name.

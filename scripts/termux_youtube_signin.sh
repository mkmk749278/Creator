#!/data/data/com.termux/files/usr/bin/bash
# Sign a YouTube channel in again on the owner's phone and print a new refresh token with the full scope set:
# manage the channel (upload, edit, captions, playlists, comments), read YouTube Analytics and the Reporting API,
# and read revenue once the channel is in the Partner Programme. The token is shown on the phone only; the owner
# pastes it into the cloud environment's settings (never into a chat or git).
#
# One command in Termux:
#   curl -sL https://raw.githubusercontent.com/mkmk749278/Creator/main/scripts/termux_youtube_signin.sh | bash
#
# It asks for the OAuth client ID and secret (Google Cloud Console, APIs & Services, Credentials: the same values as
# YT_CLIENT_ID and YT_CLIENT_SECRET), opens Google's sign-in in the phone browser, catches the reply on
# http://localhost:8765 inside Termux, checks which channel and scopes the token has, and prints the refresh token.
# A "Web application" client needs http://localhost:8765/ in its Authorized redirect URIs; a "Desktop" client needs nothing.
set -uo pipefail
command -v python3 >/dev/null || pkg install -y python
exec 3</dev/tty   # the script arrives on stdin through the pipe, so questions are read from the terminal
read -r -p "OAuth client ID: " CID <&3
read -r -s -p "OAuth client secret (hidden): " CSEC <&3; echo
[[ -n "$CID" && -n "$CSEC" ]] || { echo "client ID and secret are both needed" >&2; exit 2; }
CID="$CID" CSEC="$CSEC" python3 -I - <<'PY'
import base64, hashlib, http.server, json, os, secrets, subprocess, urllib.error, urllib.parse, urllib.request

CID, CSEC = os.environ["CID"].strip(), os.environ["CSEC"].strip()
REDIRECT = "http://localhost:8765/"
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl",
          "https://www.googleapis.com/auth/yt-analytics.readonly",
          "https://www.googleapis.com/auth/yt-analytics-monetary.readonly"]
verifier = secrets.token_urlsafe(64)
challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
state = secrets.token_urlsafe(16)
url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
    "client_id": CID, "redirect_uri": REDIRECT, "response_type": "code", "scope": " ".join(SCOPES),
    "access_type": "offline", "prompt": "consent select_account", "state": state,
    "code_challenge": challenge, "code_challenge_method": "S256"})
got = {}

class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        if "code" in q or "error" in q:
            got.update({k: v[0] for k, v in q.items()})
        self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.end_headers()
        self.wfile.write("<h2>Done. Go back to Termux.</h2>".encode())
    def log_message(self, *a):
        pass

srv = http.server.HTTPServer(("127.0.0.1", 8765), H)
print("\nIn the browser: pick the account, then the channel BE PRACTICAL with Kishore, and tick every box.")
print("If Google says the app is unverified: Advanced, then Go to (app name).")
print("If the browser does not open, copy this link into it:\n" + url + "\n")
try:
    subprocess.run(["termux-open-url", url], check=False)
except FileNotFoundError:
    pass
while not got:
    srv.handle_request()
if "error" in got:
    raise SystemExit("Google said: " + got["error"])
if got.get("state") != state:
    raise SystemExit("the reply did not match this sign-in; run the command again")

data = urllib.parse.urlencode({"client_id": CID, "client_secret": CSEC, "code": got["code"],
                               "redirect_uri": REDIRECT, "grant_type": "authorization_code",
                               "code_verifier": verifier}).encode()
try:
    tok = json.load(urllib.request.urlopen("https://oauth2.googleapis.com/token", data))
except urllib.error.HTTPError as e:
    raise SystemExit("token exchange failed: " + e.read().decode()[:300])
granted = set(tok.get("scope", "").split())
req = urllib.request.Request("https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&mine=true",
                             headers={"Authorization": "Bearer " + tok["access_token"]})
ch = json.load(urllib.request.urlopen(req)).get("items", [])
print("\nChannel:", ch[0]["snippet"]["title"].replace("\n", " ") if ch else "NONE (wrong account picked)")
for s in SCOPES:
    print(("  OK      " if s in granted else "  MISSING ") + s.rsplit("/", 1)[1])
if "refresh_token" not in tok:
    raise SystemExit("No refresh token came back. Remove the app at myaccount.google.com/permissions and run again.")
if not ch or not all(s in granted for s in SCOPES):
    print("\nNot complete: run the command again, pick the right channel and tick every box.")
print("\nRefresh token (paste it as YT_REFRESH_TOKEN_BEPRACTICALWITHKISHORE in the environment settings):\n")
print(tok["refresh_token"] + "\n")
PY

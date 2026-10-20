# Audience review prompt, v1 (owner, 2026-10-20; PLAYBOOK §4a-11)

Paste into a **new cloud session with no repository attached** (`create_session` without `source_url`), replacing
`{TITLE}` and `{NARRATION}` (one beat per line, exactly as it will be recorded). The session must not see our rules,
research or earlier drafts: it only hears the script, as a viewer would.

---

You are an independent test audience for a YouTube video narration. You have NOT seen the project, its rules or its
research, and you must not look anything up. React only as real Indian viewers would, hearing this once, on a phone,
with no picture.

Play these five viewers, each honestly and in their own voice:
1. Priya, 21, engineering student in Hyderabad, watches tech explainers at 1.25x, impatient.
2. Ramesh, 44, runs a kirana shop in Lucknow, uses PhonePe daily, English is his second language.
3. Lakshmi, 58, retired teacher in Chennai, pays bills on Google Pay, cautious with money apps.
4. Arjun, 30, software engineer in Pune, knows the subject a bit, dislikes oversimplified or wrong content.
5. Fatima, 26, call-centre employee in Kolkata, watches in a noisy bus with earphones.

The narration below is the full audio of a video titled "{TITLE}". It is read by an Indian English AI voice. Each
line is one beat.

--- NARRATION START ---
{NARRATION}
--- NARRATION END ---

For each viewer, answer briefly and honestly:
a) After the first two lines (about 10 seconds), do you know what this video is about, and would you keep watching?
b) The exact moment (quote the line) you would get bored, confused or swipe away, if any.
c) In your own words, the core idea the video promised to explain. (If you can't say it, the video failed you.)
d) The practical answer: what would you now do in this situation? (Your own words.)
e) Which lines sound like a robot, a textbook, or a non-Indian speaker? Which words would you not understand?
f) Did the jokes and examples land? Any that felt cringe?
g) What question is still in your head after watching?
h) Score 1-10: clarity, interest, trust, would-share.

Then, as a panel, give:
- The top 5 problems, ranked, each with the exact line and a rewritten line in simple everyday Indian English (same
  facts, no new facts).
- A rewritten first 10 seconds (two lines) that would make all five of you stay.
- A one-line verdict: ready to record, or not.

Write the whole answer as your final message. Do not create files, do not open any repository, do not browse.

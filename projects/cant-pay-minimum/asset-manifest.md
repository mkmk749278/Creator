# Can't Pay Even the Minimum: asset manifest (B-roll, F shots)

Sourced 2026-10-13 from the Pixabay API (`scripts/stock_fetch.py`, AI-tagged results hidden). Licence: Pixabay Content
License (commercial use, no attribution required; we credit). Files in `assets/broll/` (gitignored), rows in
`media_manifest.csv`. Candidate contact sheets (frames at 20/50/80% of each clip, labelled with the Pixabay id):
`qa/sourcing/bNN_*.jpg`, with the search hits in the matching `.tsv`.

In/out = the best 3-6 s window (`ss` = start second, `dur` = seconds), read from 2 s timecoded sheets of the downloaded file.
"ILLUS" = needs the permanent ILLUSTRATIVE FOOTAGE tag (a stand-in that could pass as the real event).

## B01 · C001-C002 night, phone
| File | What it shows | ss | dur | ILLUS | Notes |
|---|---|---|---|---|---|
| broll/pixabay_169445.mp4 (4K, 25 s) | Smartphone flat on a dark table at night, blue screen glow, a finger taps and scrolls; no readable text | 1 | 5 | no | Best "a message comes on your phone" shot; hands only, so no foreign face. Any 5 s works (consistent). |
| broll/pixabay_202987.mp4 (4K, 15 s) | Two hands typing on a phone in a dark room beside a wooden table, warm low light | 2 | 5 | no | "Then another message" cut; hands only. |
| broll/pixabay_107264.mp4 (1080p, 8 s) | Man in a dark hoodie reads a sheet, then holds his head in his hands | 4 | 4 | no | **Backup only**: Western room/door, flat light. Use 4-8 s (head down, face hidden) if at all. |

Gap: no Pixabay clip of an Indian person at home at night with a phone. The plan's DESK shots carry C001-C002, so footage
here is only a cutaway.

## B02 · C005 salary stopped / hospital bill
| File | What it shows | ss | dur | ILLUS | Notes |
|---|---|---|---|---|---|
| broll/pixabay_262440.mp4 (4096×2160, 15 s) | Young Indian man typing at a laptop at an office desk, small Indian flag on the desk, bright white room | 3 | 5 | no | "Maybe your salary stopped": the salaried worker. Push in during the edit. Laptop shows a VAIO wordmark (small, not a bank). |
| broll/coverr_iv-in-hospital-room-5485.mp4 (1920×1012, 11 s) | IV drip bag and tubing in a dim hospital room, wall medical-gas outlets | 2 | 5 | no | "Maybe a hospital bill came first". Scale to fill 1080 (crop 34 px). Coverr licence. |
| broll/pixabay_49813.mp4 (1080p, 12 s) | Gloved hand writing on a clipboard chart, patient in a hospital bed blurred behind | 1 | 5 | no | Second hospital beat (paperwork = the bill). Patient's face not visible. |

Gaps: no usable ATM, empty-wallet or "salary SMS" footage on Pixabay or Coverr (results were US dollars, cartoons or
Europe). The salary SMS is better done as a DESK/PAGE phone screen (ours, `SIMULATION`).

## B03 · C006 police / salary / family (and C063)
| File | What it shows | ss | dur | ILLUS | Notes |
|---|---|---|---|---|---|
| broll/pixabay_230083.mp4 (1080p, 7 s) | Indian police officer in khaki and a black beret at a station desk, picks up a landline and talks | 2 | 5 | **yes** | "Will the police come home?" Also usable at C063. Name tag unreadable. Stand-in, not a real case. |
| broll/pixabay_201109.mp4 (2560×1440, 57 s) | High angle over a Bengaluru road checkpoint: police in khaki and volunteers in hi-vis stop two-wheelers, green-yellow autos, cars | 5 | 6 | **yes** | Real Indian police presence (it is a traffic/lockdown check, not a debt case), so tag it. Number plates are small; blur if any reads at full res. |

Rejected: pixabay 7315 (blue flash for 0.5 s, then a black frame). Police "jeep" clips on Pixabay/Coverr are all US/EU
cars or cartoons.
Gap: **no Indian family at dinner/home** on Pixabay or Coverr (only Western families, AI-looking cartoons or food
close-ups). Suggest a DESK/PAGE beat (a family photo prop face down beside the phone) or an owner-shot clip.
"Will they take my salary?" reuses B02's office worker (262440, a different 5 s window: ss 9, dur 5).

## B04 · C009 "the reality on the ground" (busy Indian city)
| File | What it shows | ss | dur | ILLUS | Notes |
|---|---|---|---|---|---|
| broll/pixabay_8698.mp4 (1080p, 39 s) | Busy North Indian crossroads at dusk: bus, autos, bikes, pedestrians, Hindi shop signs | 10 | 5 | no | Locked-off wide; lots of motion. 13-18 s also good. Generic street, no claim. |
| broll/pixabay_1643.mp4 (1080p, 14 s) | Crowded market lane, shoppers and vendors, Hindi signboards, an old gate at the end | 6 | 5 | no | Good second cut. Faces pass close to camera (fine for B-roll). |
| broll/pixabay_84224.mp4 (4K, 8 s) | Auto-rickshaws packed in a jam on a city road | 1 | 5 | no | Short, tight; use as a 2.5-3 s insert. |
| broll/pixabay_200435.mp4 (4K, 21 s) | Drone over Hyderabad: Durgam Cheruvu cable bridge, lake and IT towers, hazy daylight | 2 | 6 | no | Also the "Hyderabad" pin in C038 and the "city room address" in C037. |
| broll/coverr_inside-of-a-car-driving-in-india-1526.mp4 (1080p, 14 s) | From the back seat: Indian city traffic through the windscreen, driver's arm on the wheel, hatchbacks and a yellow school van ahead | 3 | 5 | no | Kerala plates (KL) readable at 1080: blur or keep soft. Also fits C039 "long trip" (city leg). Coverr licence. |

## B05 · C032 call centres
| File | What it shows | ss | dur | ILLUS | Notes |
|---|---|---|---|---|---|
| broll/pixabay_141672.mp4 (4096×2160, 13 s) | Close-up from behind: an agent's ear and black headset, a bright screen blurred in front | 1 | 5 | no | Anonymous, no face, no logo. Best fit. |
| broll/pixabay_370570.mp4 (4K, 11 s) | Bearded man in a headset with a boom mic, talking, looking down at a screen | 3 | 4 | no | Clearly a European face: use short (2.5-3 s) or crop tight on the headset/mouth. |
| broll/pixabay_95123.mp4 (4K, 29 s) | Indian office: man in a white shirt at a laptop rubs his forehead in worry, colleague beside him | 9 | 5 | no | Not a call centre. Spare for C005/C006 worry ("will they take my salary?"); 1-7 s is calm work. |

Rejected: pixabay 137186 (looked Indian in the 3-frame strip, but it is a European office with a Cyrillic poster).
Gap: **no Indian call-centre / BPO floor** on Pixabay or Coverr. If the owner wants the real thing, a PIB/DD News clip
of an Indian BPO via the Fetch-media workflow is the next step (§8.4).

## B06 · C037-C039 the far village and the long trip
| File | What it shows | ss | dur | ILLUS | Notes |
|---|---|---|---|---|---|
| broll/pixabay_53958.mp4 (1080p, 11 s) | Dirt lane through an Indian village, whitewashed and stone houses, a man rides a motorbike toward camera, then a slow pan across a house front | 0 | 5 | no | "Your family lives in a village, far away". 6-11 s = the rural house front alone. |
| broll/pixabay_276582.mp4 (1080p, 9 s) | Drone over hazy flat farmland, one long road running to a far village | 1 | 6 | no | "A long trip to a far village". Slow descending drone move. |
| broll/pixabay_111161.mp4 (4K, 15 s) | Camera moves forward along an empty, narrow tarred village road between scrub and a rocky hill | 2 | 5 | no | The trip itself; pairs with the plan's dashed map road. |
| broll/pixabay_139232.mp4 (1080p, 11 s) | Farmer in a white dhoti works the soil at the edge of a ploughed field | 1 | 5 | no | Spare rural cutaway (C037/C039). |
| broll/pixabay_200435.mp4 | (see B04) Hyderabad drone | 8 | 5 | no | For the "Hyderabad" pin in C038 / "room address in the city" in C037; use a different window from C009. |

Gap: **no Indian highway or long-distance bus** footage on Pixabay (all hits were Europe, Korea, US). The Coverr car ride
(B04) covers "travel" inside a city. If wanted, an APSRTC/TSRTC bus clip is an owner fetch (DD/PIB YouTube) per §8.4.

## B07 · C041-C042 court
| File | What it shows | ss | dur | ILLUS | Notes |
|---|---|---|---|---|---|
| photos/commons_telangana_high_court_imahesh.jpg (1920×1280 photo) | High Court of Telangana, Hyderabad: red domes, Indo-Saracenic facade, palms | — | 3-4 | no | **Still**: slow push 1.00→1.12 or parallax. CC BY-SA 4.0, credit iMahesh. Caption it honestly (TELANGANA HIGH COURT · HYDERABAD). |
| photos/commons_telangana_high_court_river_kck.jpg (1920×1440 photo) | The same High Court across the Musi river, leaves in the foreground | — | 3 | no | Foreground leaves = a natural 2.5D parallax layer. CC BY-SA 4.0, credit Kavali Chandrakanth KCK. |
| broll/pixabay_198896.mp4 (4K, 24 s) | Bronze Lady Justice with scales in front of old law books (almost static) | 4 | 5 | no | Symbolic only; add a slow push. |

Accuracy note: a ₹10,000 card recovery suit would go to a civil court or a commercial/small-causes court, not the High
Court; the HC photo works as "a court" symbol only if no caption claims that is where the case goes.
Rejected: every gavel clip (Indian courts do not use gavels; it would read as American), the US courthouse 72883.
Gap: **no moving footage of an Indian court or lawyers in black coats/bands** on Pixabay/Coverr.

## B08 · C063 the night fear (door / shadow)
| File | What it shows | ss | dur | ILLUS | Notes |
|---|---|---|---|---|---|
| broll/pixabay_28237.mp4 (1080p, 68 s) | Pitch-dark room; a door slowly opens a crack, cold light and an empty hallway beyond | 5 | 6 | no | "Will the police arrest you?": the door opening is the fear, no one appears. Very dark: lift blacks slightly, keep it moody. Sync the plan's knock-like thud to ~6 s when the light first shows. |
| broll/pixabay_40797.mp4 (4K, 16 s) | Silhouette of a man at a dark window at night, city traffic streaming below; he raises a hand to the glass | 2 | 6 | no | Anonymous silhouette (could be anyone). Also a cutaway for C001-C002 night worry. Skyline is not Indian but is out of focus. |

Gap: no "knock on a door" or "shadow under the door" clip on Pixabay (hits were cartoons, CGI portals, horror). The plan's
DESK thud + phone light carries the knock.

## B09 · C072 call the bank, write to them, keep every message
| File | What it shows | ss | dur | ILLUS | Notes |
|---|---|---|---|---|---|
| broll/pixabay_86866.mp4 (1080p, 10 s) | Man in a yellow armchair at home, laptop on his lap, talks on the phone, looking out of the window | 1 | 5 | no | "Call the bank". Western face; serious, not panicked. A mug reads "HARLEM" (small). |
| broll/pixabay_12040.mp4 (1080p, 10 s) | A hand writes with a blue pen in a squared notebook resting on a thick open book | 2 | 5 | no | "And also write to them". No readable text. |
| broll/pixabay_134872.mp4 (1080p, 12 s) | Close-up of brown hands holding smartphones, thumbs typing and scrolling | 1 | 5 | no | "Keep every message". Screens unreadable. |

Rejected: pixabay 117 (laptop typing, soft and upscaled), Coverr phone-call clips (European lads in kitchens; no better
than 86866). Gap: no Indian person on a calm phone call.

## B10 · C077 pay only through the bank's own channel (UPI / phone payment)
| File | What it shows | ss | dur | ILLUS | Notes |
|---|---|---|---|---|---|
| broll/pixabay_134872.mp4 | (see B09) hands on phones | 6 | 4 | no | Only as a generic "pay from your phone" cutaway, a different window from C072. |

Gap: **no real UPI / QR / phone-payment footage** on Pixabay or Coverr (only green-screen cartoons, Apple Pay in a café,
crypto graphics). The plan already shows C077 as a PAGE phone-screen prop (ours, `SIMULATION`); keep it that way.
Never use a real UPI app's or bank's screen.

## B11 · generic: bank branch, ATM, salaried workers commuting
| File | What it shows | ss | dur | ILLUS | Notes |
|---|---|---|---|---|---|
| broll/pixabay_154195.mp4 (4K, 28 s) | Mumbai arterial road from a skywalk: morning traffic, black-and-yellow autos, a yellow school bus, flyover, apartment blocks | 12 | 5 | no | Salaried city life / commute. One hoarding is small and unreadable. |
| broll/pixabay_271463.mp4 (4K, 16 s) | Indian woman worker in a blue uniform and hairnet at a machine on a textile factory floor | 2 | 5 | no | The blue-collar salary earner. Alternative to 262440 for "maybe your salary stopped". |
| broll/pixabay_139848.mp4 (4K, 22 s) | Through the wire-mesh window of a moving Mumbai local train, tracks and scrub rushing past (soft focus) | 6 | 5 | no | Commute; also a "long trip" texture for C039. |
| broll/pixabay_262440.mp4 | (see B02) Indian office worker at a laptop | 9 | 5 | no | Office worker. |

Gap: **no Indian bank branch exterior and no ATM** on Pixabay or Coverr (only cartoons, US dollar counting, a Bank of
America tower). Options: a Commons photo of a generic Indian bank street frontage with every logo blurred, or a PAGE prop
(the plan's look already supports this).

## Summary (2026-10-13)
31 assets: 29 video clips (27 Pixabay, 2 Coverr) and 2 Commons photos. Every pick was checked on 2 s timecoded sheets of
the downloaded file. Rejected after download: pixabay 7315 (black), 137186 (European office), 117 (soft). No AI-tagged
item was used; the tool hides those.
Strong (Indian, literal): B04 city streets, B06 village, B03 police (ILLUS), B07 Telangana High Court photos.
Weak or missing: Indian family at home (none), Indian call-centre floor (none), highway/bus (none), ATM/bank branch
(none), UPI payment (none, keep as a PAGE prop), knock at the door (none), an Indian person at night with a phone (hands
only). For a real Indian BPO, bus or bank clip, the next step is an owner fetch of DD/PIB footage (PLAYBOOK §8.4).

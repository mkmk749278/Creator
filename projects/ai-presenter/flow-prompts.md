# Google Flow prompts for the AI presenter (copy-paste from the phone)

About 25 minutes of tapping, done once. Each prompt is in a grey box: long-press → copy → paste into Flow.

## Settings (check once)
- Video model: **Veo 3.1** (or the newest Veo in the menu). Use **Fast** for a first try of each prompt; regenerate the
  ones you like on **Quality** only if Fast looks soft.
- Aspect ratio **16:9**. Outputs per prompt: **2**. Download at **1080p** (choose "Upscaled" if Flow offers it).
- Name each download exactly as written (e.g. `G04_A.mp4`), then put all files in one Google Drive folder.

---

## Step 1: three still images (Flow → image generation)

### 1a. Camera A rest still (medium shot). Generate 4, pick the best face, download as `rest_A.png`
```
Photorealistic cinematic still, medium shot, eye level, 16:9. An original, ordinary-looking South Indian man about 35 years old, not resembling any actor or celebrity: medium-brown skin, short neat black hair with a side part, short well-trimmed beard, friendly intelligent eyes, no glasses. He wears an open dark-navy overshirt over a plain heather-grey crew-neck t-shirt, dark charcoal chinos and a simple steel wristwatch on his left wrist. He sits relaxed in a dark-brown leather armchair angled slightly toward the camera, both hands resting on the armrests, looking straight into the lens with a calm, warm expression, mouth closed. Set: a modern dark premium talk-show studio at night, charcoal walls with vertical walnut slats, a tall bookshelf with real books and a small plant on the left, a warm brass floor lamp, and a large wall screen behind him on the right glowing soft teal, out of focus. Soft warm key light from camera left, gentle rim light, shallow depth of field, 35 mm film look, natural skin texture. No text, no logos, no watermark.
```

### 1b. Camera B rest still (close-up, 3/4 angle). Use `rest_A.png` as the reference image. Download as `rest_B.png`
```
Same man, same clothes, same studio and lighting as the reference image. Change only the camera: a close-up from chest up, camera placed 30 degrees to his left, so he is in a three-quarter view but turns his eyes to look into this lens. Hands resting on the armrests, calm warm expression, mouth closed. Teal wall screen and walnut slats softly out of focus behind him. Photorealistic, 16:9, no text, no logos.
```

### 1c. Wide still. Use `rest_A.png` as the reference image. Download as `rest_W.png`
```
Same man, same clothes, same studio and lighting as the reference image. Change only the camera: a wide shot showing the whole studio, the armchair, the bookshelf, the floor lamp and the teal wall screen, with him seated in the centre, hands on the armrests, looking into the lens. Photorealistic, 16:9, no text, no logos.
```

**Stop here and send me the three stills first** (Drive link). I check that the face is consistent and natural and
that he looks like nobody famous before you spend credits on video.

---

## Step 2: gesture clips (Flow → Frames to Video)
For each prompt below:
1. **First frame = `rest_A.png`, last frame = `rest_A.png`** → save the best of the two as `Gxx_A.mp4`.
2. Same prompt again with **first and last frame = `rest_B.png`** → save as `Gxx_B.mp4`.

The camera must stay locked (I add camera moves later). Ignore whatever sound Flow makes: we replace it with Bunty's
voice and redraw his lips to match.

### G01 calm explaining
```
Locked-off camera, no camera movement. The man from the frame talks to the camera in a calm, friendly, explaining way, with small natural hand movements from the armrest, a slight head nod, and natural blinking. At the end he settles back to the exact starting pose. Natural, subtle, realistic body language. No text, no music.
```
### G02 open palms
```
Locked-off camera, no camera movement. The man talks to the camera and explains a point with both palms open, hands moving apart at chest height as if laying out an idea, then returns his hands to the armrests and the exact starting pose. Natural, relaxed, realistic. No text, no music.
```
### G03 counting on fingers
```
Locked-off camera, no camera movement. The man talks to the camera while counting three points on his fingers: he raises his right hand and taps one, two, three fingers with his left index finger, then lowers his hands back to the armrests and the exact starting pose. Natural and realistic. No text, no music.
```
### G04 emphasis beat
```
Locked-off camera, no camera movement. The man talks to the camera with conviction and makes one firm downward beat with his right hand to stress a word, eyebrows slightly lowered, then relaxes back to the exact starting pose. Natural, controlled, not aggressive. No text, no music.
```
### G05 leans in, serious
```
Locked-off camera, no camera movement. The man's expression turns serious; he leans forward toward the camera, forearms on his knees, hands loosely clasped, and talks with quiet weight, then slowly sits back into the exact starting pose. Realistic and subtle. No text, no music.
```
### G06 confiding
```
Locked-off camera, no camera movement. The man leans in slightly and talks to the camera in a lowered, confiding way, as if sharing something important just with the viewer, a small hand gesture near his chest, then sits back to the exact starting pose. Subtle and realistic. No text, no music.
```
### G07 real question
```
Locked-off camera, no camera movement. The man asks the camera a genuine question: eyebrows rise, head tilts slightly, both palms turn up in a small open shrug, he holds the look for a moment, then returns to the exact starting pose. Natural and realistic. No text, no music.
```
### G08 shock
```
Locked-off camera, no camera movement. The man reacts with genuine surprise to something he is describing: eyes widen, he pulls his head back slightly, one hand lifts a little off the armrest, then he composes himself and returns to the exact starting pose. Realistic, not exaggerated. No text, no music.
```
### G09 warning finger
```
Locked-off camera, no camera movement. The man gives the camera a clear warning: he raises his right index finger at shoulder height, eyes steady and serious, talks firmly, then lowers his hand back to the armrest and the exact starting pose. Calm authority, not angry. No text, no music.
```
### G10 empathy
```
Locked-off camera, no camera movement. The man talks to the camera with empathy: he places his right hand gently on his chest, eyes soft, a small understanding nod, then returns his hand to the armrest and the exact starting pose. Warm and sincere, realistic. No text, no music.
```
### G11 hopeful smile
```
Locked-off camera, no camera movement. The man talks to the camera with a hopeful, encouraging warm smile, opening his hands slightly outward as if offering a way forward, then returns to the exact starting pose. Natural and realistic. No text, no music.
```
### G12 points to the screen behind
```
Locked-off camera, no camera movement. The man talks to the camera, then turns his head and gestures with his open right hand toward the large teal wall screen behind him, as if to say look at this, then turns back to the camera and returns to the exact starting pose. Natural and realistic. No text, no music.
```
### G13 intense stare
```
Locked-off camera, no camera movement. The man keeps very still and talks directly into the lens with intense, steady eyes and minimal movement, serious and focused, a single slow blink, ending in the exact starting pose. Realistic. No text, no music.
```
### G14 warm welcome
```
Locked-off camera, no camera movement. The man looks into the camera with a warm, friendly welcoming smile and a small nod, as if greeting a friend who just sat down, talks briefly, and ends in the exact starting pose with a light smile. Natural and realistic. No text, no music.
```
### G15 thoughtful pause
```
Locked-off camera, no camera movement. The man pauses thoughtfully with his mouth closed: he looks slightly down and to the side, tilts his head a little, touches his beard with two fingers for a moment, then looks back into the lens and returns to the exact starting pose. No talking. Realistic. No text, no music.
```
### G16 sad head shake
```
Locked-off camera, no camera movement. The man slowly shakes his head with quiet sadness and disappointment while talking softly to the camera, eyes lowered briefly, then looks back up into the lens in the exact starting pose. Restrained and realistic. No text, no music.
```
### G17 confident, sits back
```
Locked-off camera, no camera movement. The man sits back comfortably in the armchair with relaxed confidence, one hand making an easy, assured gesture as he talks to the camera, a slight knowing smile, ending in the exact starting pose. Natural and realistic. No text, no music.
```
### G18 wide opening (only with `rest_W.png` as first frame; leave the last frame empty)
```
Locked-off wide shot, no camera movement. The studio lights glow warmly and the teal wall screen flickers softly to life behind him; the man settles into the armchair, adjusts his overshirt slightly, looks up into the lens and gives a small welcoming nod. Realistic, cinematic. No text, no music.
```

---

## Checklist before you send the Drive link
- 3 stills + 34 clips (G01–G17 × A and B) + `G18_W.mp4`.
- Skip any clip where his face changes, a hand looks wrong (extra fingers, melting), or text appears. Just regenerate it.
- Not sure about a clip? Send it anyway with "?" in the name. I'll check every clip frame by frame.

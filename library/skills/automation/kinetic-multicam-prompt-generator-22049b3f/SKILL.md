---
name: "kinetic-multicam"
description: "Generate a video‑to‑video prompt that adds kinetic motion‑graphics supers and rapid camera‑whip transitions to a single talking‑head take."
---

# /kinetic-multicam: One Take → Kinetic Supers + Camera Snaps

## Overview

Turns ONE real talking‑head take into a video‑to‑video prompt (best on **Seedance 2.0 Fast**) that adds:
- Split‑second visible camera whips (motion‑blurred moves that lock into stable frames)
- Bold kinetic supers (motion‑graphics text, **not** captions) synced to speech beats.

The prompt **preserves** the uploaded source video (face, room, audio, lip sync). It never describes or regenerates the scene.

Core principle: the template is frozen; only three zones ever change – the `[Xs]` timestamps, the `"[TEXT]"` supers, and optional camera‑position descriptions.

## Input

Local video file only. If the user provides a URL, ask them to download the video locally first. If multiple local files could match, ask for clarification – never guess.

## Step 0 — Preflight (first run or on missing‑tool error)

```bash
python "<this skill's base directory>/scripts/check_env.py"
```

Verifies Python 3.8+, ffmpeg, ffprobe and Whisper. Prints missing tools with exact install commands; never installs automatically.

## Step 1 — Beats

```bash
python "<this skill's base directory>/scripts/beats.py" "<video path>"
```

Reports detected `LANGUAGE` and `DURATION`. Flags allow language override, forced re‑transcription, model selection, and custom cut count.

## Step 2 — Pick block count & refine boundaries

Block count scales with video length (≤10 s → 4 blocks, 10‑15 s → 5 blocks, >15 s → 6 blocks). Users may override at the checkpoint. Boundaries are refined to phrase starts, respect silence gaps, and obey spacing rules (≈0.7‑2.5 s per block, last block returns to original camera).

## Step 2b — Write the supers

One super every ~1.5‑2 s, extracted **directly** from spoken words in the block. Rules:
- 2‑6 contiguous spoken words, trimmed to 2‑4 meaningful words.
- Keep negations, drop filler articles/prepositions.
- Language matches video language; supers are **ALL CAPS**, no commas or final periods.
- Supers are punchy call‑outs, never full sentences.

## Step 3 — Mandatory checkpoint

Present to the user:
1. Two‑line summary of the effect.
2. Phrase table with time windows.
3. Suggested blocks with timestamps, supers (or "camera‑only"), and justification.
4. The frozen template with placeholders.

Ask the user to confirm or edit:
- Block count & timestamps
- Super texts & which blocks stay camera‑only
- Camera‑position presets
- Optional opening‑hook super (default OFF)
- Optional static‑super block if a valuable super would be dropped

Never skip this checkpoint.

## Step 4 — Fill and deliver

Replace only the `[Xs]` timestamps and `"[TEXT]"` supers (keeping brackets and quotes). Apply any user‑requested camera‑position swaps. Save as `<video basename>_kinetic_multicam_prompt.txt` next to the video.

Verify:

```bash
python "<this skill's base directory>/scripts/verify_prompt.py" "<saved .txt>"
```

The script must output `PASS`. On `FAIL`, fix and re‑run.

Deliver the final prompt in a fenced code block and instruct the user to upload the source video to **Seedance 2.0 Fast**, paste the prompt, and run the generation.

## The canonical template (FROZEN)

```
Use the uploaded video as the source. The Supers must follow the pace of the audio.
Video timing must be exactly the same as original video.

Preserve the person's face, identity, expression, clothing, body proportions, and lip sync exactly as in the original footage. Preserve the room, lighting, furniture, background, and overall environment. Do not replace, redesign, or hallucinate any part of the scene.

The only changes should be rapid cinematic camera repositioning and the addition of kinetic motion graphics.

Do not add traditional subtitles. Instead, create bold, high‑energy kinetic supers that visually reinforce the spoken message. The supers should behave like motion graphics, not captions. Use dynamic typography, scaling, rotation, perspective, masking, tracking, and creative layouts. Vary the style throughout the video so each callout feels intentional and visually engaging. The text must never cover the speaker's face. Place each super in open areas of the frame, or layer it behind the speaker's body so the person partially occludes the text — as if the words physically exist in the room behind them. The text should integrate naturally with the composition.

Camera movement should be extremely fast. Each transition should take only a split second, rapidly snapping to the new viewpoint before immediately locking into a perfectly stable frame. The camera must visibly travel to each new position — a fast, motion‑blurred whip move with a speed‑ramp feel — never an editing cut and never an invisible instant jump between angles. Do not create long continuous camera moves, floating movement, or handheld motion. Every move should feel like a fast cinematic reposition followed by a freeze.

Follow this timeline:

From [Xs] to [Xs]
Display the kinetic super:
"[TEXT]"
Whip the camera in a fast motion‑blurred orbital sweep to the left, landing in a left orbit position, then hold completely still.

From [Xs] to [Xs]
Display the kinetic super:
"[TEXT]"
Whip the camera upward in a fast motion‑blurred crane rise to a higher crane angle, then hold completely still.

From [Xs] to [Xs]
Display the kinetic super:
"[TEXT]"
Whip the camera backward in a fast motion‑blurred pull‑out to a wide position revealing the full room with the speaker centered, then hold completely still.

From [Xs] to [Xs]
Display the kinetic super:
"[TEXT]"
Whip the camera in a fast motion‑blurred sweep back to the original camera position and hold until the end.

Important requirements:

* Maintain the exact room and person throughout.
* Do not change facial features, clothing, lighting, or background.
* Preserve perfect lip sync.
* No hard cuts to different scenes.
* Every transition is a visible, motion‑blurred camera move — never an editing cut.
* No title cards.
* No subtitle‑style captions.
* Supers never cover the speaker's face — open frame areas or layered behind the body, never over it.
* Only rapid split‑second camera repositioning followed by locked‑off shots.
* Motion graphics should feel premium, modern, energetic, and social‑media optimized.
```

### Optional hook super (opt‑in at the checkpoint)

```
From [0s] to [Xs]
Display the kinetic super:
"[TEXT]"
Keep the camera in the original position and framing, completely still.
```

### Optional static‑super block (opt‑in)

```
From [Xs] to [Xs]
Display the kinetic super:
"[TEXT]"
Keep the camera locked in the same position, completely still.
```

### Camera‑only block (no super)

```
From [Xs] to [Xs]
Whip the camera ... (position line from the template or presets)
```

## Camera position presets (offered at the checkpoint)

| Preset | Template‑ready wording |
|---|---|
| Right orbit | `Whip the camera in a fast motion‑blurred orbital sweep to the right, landing in a right orbit position, then hold completely still.` |
| Low hero angle | `Whip the camera in a fast motion‑blurred drop to a low angle position looking slightly up at the speaker, then hold completely still.` |
| Top‑down overhead | `Whip the camera in a fast motion‑blurred rise to a top‑down overhead position looking down at the speaker, then hold completely still.` |
| Tight close‑up | `Whip the camera forward in a fast motion‑blurred punch‑in to a tight close‑up framing on the speaker's face, then hold completely still.` |
| Wide (room reveal) | `Whip the camera backward in a fast motion‑blurred pull‑out to a wide position revealing the full room with the speaker centered, then hold completely still.` |
| Dutch tilt | `Whip the camera in a fast motion‑blurred roll into a subtly tilted dutch angle position, then hold completely still.` |

---

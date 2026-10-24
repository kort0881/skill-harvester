---
name: "youtube-transcript"
description: "Download YouTube video transcripts, optionally translate them to Vietnamese and generate structured summaries. Organises results in a topic‑based folder hierarchy for personal knowledge bases."
---

# YouTube Transcript Skill v2.0

**Automatic extraction → Translation → Summarisation → Local storage**

## Features

| Feature | Description | CLI flag |
|---|---|---|
| Download transcript | Retrieve original subtitles (EN or VI) | `-l en` / `-l vi` |
| Translate | Convert English transcript to Vietnamese | `--translate` |
| Summarise | Generate a structured summary and analysis | `--summarise` |
| Output control | Choose destination folder | `-o <path>` |

## Quick start

```bash
# Basic download (English)
python3 scripts/yt_transcript.py "https://youtube.com/watch?v=VIDEO_ID" -l en

# Download and translate to Vietnamese
python3 scripts/yt_transcript.py "https://youtube.com/watch?v=VIDEO_ID" --translate -o ./output

# Full pipeline: download, translate, summarise
python3 scripts/yt_transcript.py "https://youtube.com/watch?v=VIDEO_ID" --translate --summarise -o ./output
```

## Output layout

*Default* (`-o ./transcripts`)
```
transcripts/
└── {video_title}.txt          # original transcript
```

*With translation*
```
output/
├── {video_title}.txt          # original transcript
└── {video_title}_vi.txt       # Vietnamese translation
```

*Full pipeline*
```
output/
├── 00_metadata.json
├── 01_original.txt
├── 02_translation.txt
└── 03_summary.md
```

## Command‑line options

```
python3 scripts/yt_transcript.py <youtube_url> [options]

Options:
  -l, --lang        en | vi | en-orig | vi-orig (default: en)
  -o, --output      Output directory (default: ./transcripts)
  -t, --translate   Translate transcript to Vietnamese
  -s, --summarise   Generate summary and analysis
  -f, --format      txt | vtt | both (default: txt)
  -k, --keep-vtt    Keep the original VTT file
  -h, --help        Show this help message
```

## Requirements

* Python 3.6+
* `yt-dlp` (installed automatically if missing)
* Optional for translation: `deep-translator` (or `googletrans` fallback)
* Optional for summarisation: `langchain` plus an LLM API key (e.g., OpenAI, Anthropic)

Install all optional dependencies with:
```bash
pip install yt-dlp deep-translator langchain
```

## Troubleshooting

*No subtitles*: Verify the video has closed captions enabled.
*yt‑dlp errors*: `pip install --upgrade yt-dlp`
*Translation quota*: Switch to the `googletrans` fallback.
*Summarisation fails*: Ensure an LLM API key is exported (e.g., `export OPENAI_API_KEY=…`).

## Typical workflows

1. **Fast learning** – download, translate and read the summary without watching the video.
2. **Knowledge‑base building** – organise multiple videos under a topic folder.
3. **Work‑related training** – store translated and summarised material for internal reference.

---

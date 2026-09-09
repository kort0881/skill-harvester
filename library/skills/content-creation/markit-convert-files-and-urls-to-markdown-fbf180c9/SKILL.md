---
name: "markit"
description: "Convert files, URLs, and GitHub resources to clean Markdown. Supports PDF, DOCX, PPTX, XLSX, HTML, EPUB, CSV, JSON, images, audio, ZIP, and more."
---

# Markit

## Overview
Markit is a Node.js‑based tool that extracts the textual content of a wide range of document formats and returns it as Markdown. It can be used from the command line or programmatically via its TypeScript SDK.

## Prerequisites
- Node.js (v14 or later)
- npm (comes with Node.js)

## Installation
```bash
npm install -g @shiftlabs/markit
```

## CLI Usage
```bash
# Convert a local file to raw markdown
npx @shiftlabs/markit report.pdf -q

# Convert a remote URL
npx @shiftlabs/markit https://en.wikipedia.org/wiki/Markdown -q

# Convert a GitHub repository, file, gist, issue, or pull request
npx @shiftlabs/markit https://github.com/owner/repo -q
npx @shiftlabs/markit https://github.com/owner/repo/issues/42 -q
npx @shiftlabs/markit https://gist.github.com/user/id -q

# Write output to a file
npx @shiftlabs/markit document.docx -q -o output.md

# Get structured JSON output (markdown + inferred title)
npx @shiftlabs/markit report.pdf --json

# List all supported input formats
npx @shiftlabs/markit formats

# Show full help
npx @shiftlabs/markit --help
```

- `-q` – Return raw markdown (no additional metadata).
- `--json` – Return a JSON object `{ "markdown": "...", "title": "..." }`.
- `-o <file>` – Write the result to the specified file.

## SDK (TypeScript) Usage
```typescript
import { Markit } from "@shiftlabs/markit";

const markit = new Markit();

// Convert a local file
const { markdown, title } = await markit.convertFile("report.pdf");

// Convert a remote URL
const { markdown: urlMd } = await markit.convertUrl("https://example.com");

// Convert a raw buffer with an explicit extension
import { readFile } from "fs/promises";
const buffer = await readFile("document.docx");
const { markdown: bufMd } = await markit.convert(buffer, { extension: ".docx" });
```

The SDK methods return a promise that resolves to an object containing at least `markdown` and, when possible, a `title`.

## Verification
After conversion, you can quickly verify the output by previewing the first few lines:
```bash
head -n 10 output.md
```
Or, when using `--json`, inspect the JSON structure:
```bash
npx @shiftlabs/markit report.pdf --json | jq '.'
```

## Limitations & Notes
- Complex layouts (e.g., multi‑column PDFs) may lose some visual fidelity.
- Binary‑only files (e.g., pure images) are converted to Markdown image links when possible.
- Large archives are processed file‑by‑file; the tool extracts each supported document inside the archive.

---

---
name: "courseforge"
description: "Generate accessible, branded course materials for programming classes, outputting dark‑themed HTML that can be converted to PDF/UA‑1 with WeasyPrint. Supports tutorials, in‑class exercises, homework, and answer keys, with a configurable theme system."
---

# CourseForge

Generate accessible, print‑ready course materials for programming classes.

## Quick Start

1. Copy `assets/theme.json` and customize colors, fonts, and branding for your course.
2. Tell the agent: "Create a Module 3 tutorial on Loops for ITP 120".
3. The agent produces an HTML file; convert it with:
   ```bash
   weasyprint file.html file.pdf --pdf-variant=pdf/ua-1
   ```

## Document Types

| Type       | Purpose          | Key Elements |
|------------|------------------|--------------|
| **Tutorial**   | Teach concepts   | Explanations, code examples, analogies, tables, vocabulary, quiz |
| **In‑Class**   | Guided practice  | Setup box, numbered exercises, hints, expected output |
| **Homework**   | Independent work | Problem descriptions, point values, expected output, rubric |
| **Answer Key** | Instructor only  | Quick‑reference table, detailed explanations per question |

Read `references/document-types.md` for the full structure of each type.

## Theme System

All styling is driven by `assets/theme.json`. Example:
```json
{
  "course": { "code": "ITP 120", "name": "Programming with Java" },
  "institution": "Northern Virginia Community College",
  "instructor": "Randy Michak",
  "colors": { "bg": "#0a0f1a", "card": "#141d2b" },
  "fonts": { "body": "Inter", "code": "Consolas" }
}
```
Override any value to change branding across all documents. The agent reads `theme.json` at generation time and injects the values into the HTML template.

## Workflow

### Single Document
1. Read `assets/theme.json` for branding.
2. Read `references/document-types.md` for the target document structure.
3. Read `assets/template-{type}.html` for the HTML skeleton.
4. Generate content following the template structure.
5. Convert to PDF:
   ```bash
   weasyprint output.html output.pdf --pdf-variant=pdf/ua-1
   ```

### Full Module (tutorial + in‑class + homework + answer keys)
1. Perform the steps above for each document type.
2. Use consistent naming: `{COURSE}-Module{NN}-{Type}.html`.
   Example: `ITP120-Module03-Tutorial.html`, `ITP120-Module03-InClass.html`.

## Accessibility Rules (Mandatory)

Every document **must** comply with WCAG 2.1 Level AA and PDF/UA‑1:
- `<html lang="en">` on every document.
- `<main role="main" aria-label="...">` wrapping all content.
- Semantic heading order (H1 → H2 → H3, no skips).
- Tables must include `<thead>` and `<th scope="col">`; **no** `<caption>` (breaks WeasyPrint PDF/UA‑1).
- ARIA labels on all boxed regions: `role="region" aria-label="..."`.
- Quiz choices container: `role="list"`; each choice: `role="listitem"`.
- Provide `alt` text for images; decorative images get `role="presentation"`.
- Minimum contrast ratio 4.5:1.
- Use sans‑serif fonts, minimum 11 pt body text.
- Apply `page-break-inside: avoid` on boxes, tables, code blocks, and quiz questions.
- Generate PDF with:
  ```bash
  weasyprint file.html file.pdf --pdf-variant=pdf/ua-1
  ```
- Include screen‑reader‑only skip links: `<div class="sr-only">`.

## Quiz Rules

- Randomize answer positions; distribution of correct letters should be roughly even.
- Verify distribution after writing; if more than three answers share the same letter, reshuffle.
- Use 5 questions for short/intro topics, 10 for standard modules.
- Test recall and understanding; avoid “All of the above”, “None of the above”, and negative phrasing.
- All answer options must be drawn from content covered in the document.

## Code Examples

- Use syntax‑highlighted `<span>` classes: `.keyword`, `.type`, `.string`, `.comment`, `.number`, `.output`.
- Follow every code block with a `.code-explain` div showing output and/or line‑by‑line explanation.
- Provide realistic, context‑relevant examples (avoid generic `foo`/`bar`).
- Show expected output for every runnable example.

## Content Guidelines

- Define terms before first use.
- Use analogies to connect new concepts to familiar ideas.
- Write short paragraphs; use numbered steps and bullet points.
- Offer multiple learning paths: text, code, tables, analogies.
- Increase complexity progressively within each section.
- Do **not** include dates or semester identifiers; keep materials reusable across terms.

## File Structure

```
courseforge/
├── SKILL.md                          # This file
├── assets/
│   ├── theme.json                    # Customizable branding/colors
│   ├── template-tutorial.html        # Tutorial HTML skeleton
│   ├── template-inclass.html         # In‑class exercise skeleton
│   ├── template-homework.html        # Homework assignment skeleton
│   └── template-answerkey.html       # Answer key skeleton
└── references/
    └── document-types.md             # Detailed structure for each document type
```

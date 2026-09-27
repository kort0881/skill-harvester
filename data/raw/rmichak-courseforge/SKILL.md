---
name: courseforge
description: >
  Generate accessible, branded course materials for programming classes: tutorials (lecture-style
  with code examples, analogies, vocabulary, quizzes), in-class exercises (guided hands-on coding),
  homework assignments (independent practice problems with expected output), and answer keys.
  Outputs dark-themed HTML that converts to PDF/UA-1 via weasyprint. Supports any programming
  language and any course. Customizable theming via theme.json. Use when asked to create tutorials,
  lectures, in-class exercises, homework, quizzes, study guides, or answer keys for a programming
  course. Also use for batch module creation, course planning, or converting existing materials
  to accessible OER format.
---

# CourseForge

Generate accessible, print-ready course materials for programming classes.

## Quick Start

1. Copy `assets/theme.json` and customize for your course (colors, fonts, branding)
2. Tell the agent: "Create a Module 3 tutorial on Loops for ITP 120"
3. Agent produces HTML → convert with `weasyprint file.html file.pdf --pdf-variant=pdf/ua-1`

## Document Types

| Type | Purpose | Key Elements |
|------|---------|-------------|
| **Tutorial** | Teach concepts | Explanations, code examples, analogies, tables, vocabulary, quiz |
| **In-Class** | Guided practice | Setup box, numbered exercises, hints, expected output |
| **Homework** | Independent work | Problem descriptions, point values, expected output, rubric |
| **Answer Key** | Instructor only | Quick-reference table, detailed explanations per question |

Read `references/document-types.md` for full structure of each type.

## Theme System

All styling is driven by `assets/theme.json`. Read it before generating any document.

```json
{
  "course": { "code": "ITP 120", "name": "Programming with Java" },
  "institution": "Northern Virginia Community College",
  "instructor": "Randy Michak",
  "colors": { "bg": "#0a0f1a", "card": "#141d2b", ... },
  "fonts": { "body": "Inter", "code": "Consolas" }
}
```

Override any value to change branding across all documents. The agent reads `theme.json` at
generation time and injects values into the HTML template.

## Workflow

### Single Document
1. Read `assets/theme.json` for branding
2. Read `references/document-types.md` for the target document structure
3. Read `assets/template-{type}.html` for the HTML skeleton
4. Generate content following the template structure
5. Convert: `weasyprint output.html output.pdf --pdf-variant=pdf/ua-1`

### Full Module (tutorial + in-class + homework + answer keys)
1. Same steps but generate all document types for the module
2. Use consistent naming: `{COURSE}-Module{NN}-{Type}.html`
3. Example: `ITP120-Module03-Tutorial.html`, `ITP120-Module03-InClass.html`

## Accessibility Rules (Mandatory)

Every document MUST comply with WCAG 2.1 Level AA + PDF/UA-1:

- `<html lang="en">` on every document
- `<main role="main" aria-label="...">` wrapping all content
- Semantic headings: H1 → H2 → H3 (no skips)
- Tables: `<thead>`, `<th scope="col">`, NO `<caption>` (breaks weasyprint pdf/ua-1)
- ARIA labels on all boxes: `role="region" aria-label="..."`
- Quiz choices: `role="list"` on container, `role="listitem"` on each choice
- Alt text on images; decorative images get `role="presentation"`
- Minimum 4.5:1 color contrast ratio
- Sans-serif fonts, minimum 11pt body text
- `page-break-inside: avoid` on all boxes, tables, code blocks, quiz questions
- PDF generated with: `weasyprint file.html file.pdf --pdf-variant=pdf/ua-1`
- Screen-reader friendly: `<div class="sr-only">` for skip content

## Quiz Rules

- **Randomize answer positions**: Correct answers must be distributed roughly equally across A, B, C, D
- After writing a quiz, verify answer distribution — if more than 3 answers share the same letter, shuffle
- 5 questions for short/intro topics, 10 questions for standard modules
- Test recall and understanding, not tricks
- Avoid: "All of the above", "None of the above", negatives ("Which is NOT...")
- All answers must come from content covered in the document

## Code Examples

- Use syntax-highlighted `<span>` classes: `.keyword`, `.type`, `.string`, `.comment`, `.number`, `.output`
- Follow every code block with a `.code-explain` div showing output and/or line-by-line explanation
- Use realistic, contextually relevant examples (not just `foo`/`bar`)
- Show expected output for every runnable example

## Content Guidelines

- Define terms before using them
- Use analogies to connect new concepts to familiar ideas
- Short paragraphs, numbered steps, bullet points
- Multiple learning paths: text + code + tables + analogies
- Progressive complexity within each section
- No dates or semesters in materials (keep them reusable across terms)

## File Structure

```
courseforge/
├── SKILL.md                          # This file
├── assets/
│   ├── theme.json                    # Customizable branding/colors
│   ├── template-tutorial.html        # Tutorial HTML skeleton
│   ├── template-inclass.html         # In-class exercise skeleton
│   ├── template-homework.html        # Homework assignment skeleton
│   └── template-answerkey.html       # Answer key skeleton
└── references/
    └── document-types.md             # Detailed structure for each document type
```

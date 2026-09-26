---
name: "ai-consultant-onboarding"
description: "Generates a complete, professional client onboarding package for AI consultants, auditors, and solopreneurs. Produces four ready‑to‑use documents: intake questionnaire, welcome email, service agreement, and project brief."
---

# AI Consultant Client Onboarding Skill

This skill helps an AI consultant, auditor, or solopreneur onboard a new client efficiently. It gathers required client details, then creates a full onboarding package consisting of four polished documents.

## Step 1 – Gather Client Information
Ask the user for the following items (or extract them if already provided). Use a single friendly message:

```
To create your onboarding package, I need a few quick details:

1. **Client name** (person and/or company)
2. **Your name / business name**
3. **Service type** – choose or describe:
   - AI Readiness Audit
   - AI Strategy & Roadmap
   - AI Tool Implementation
   - AI Workflow Automation
   - AI Team Training / Workshops
   - Ongoing AI Retainer / Advisory
   - Custom (describe briefly)
4. **Project scope** – one sentence describing the goal
5. **Timeline** – start date and rough duration
6. **Budget / investment** (optional)
7. **Primary contact & email** at the client side
8. **Anything special** – industry, pain points, tech stack, etc.
```

Wait for the user's answers before proceeding.

## Step 2 – Generate the Onboarding Package
Using the collected details, produce the following documents in order. Label each with a clear top‑level header.

### Document 1 – Discovery & Intake Questionnaire
*Purpose:* Sent before the first call to gather context.
*Format:* Numbered questions grouped by theme.
*Sections:* About Your Business, AI Awareness & Current State, Goals & Challenges, Practical & Logistical. Add service‑specific questions (e.g., data security for audits, learning styles for training).

### Document 2 – Welcome Email
*Purpose:* Sent immediately after the contract is signed.
*Structure:* Subject line, opening paragraph, 3‑4 bullet points of next steps, brief working‑style overview, practical details (response times, preferred channel), warm closing.
*Tone:* Confident, human, enthusiastic.

### Document 3 – Service Agreement (Plain Language)
*Purpose:* Simple, readable agreement (not a legal document).
*Disclaimer:* Include a top‑level note that the agreement is plain‑language and not a substitute for legal advice.
*Sections:* Parties, Services, Timeline, Investment (omit if budget missing), Client Requirements, Revisions & Scope Changes, Confidentiality, Intellectual Property, Termination, Signatures.

### Document 4 – Project Brief
*Purpose:* Internal reference and/or client‑facing overview.
*Sections:* Project Overview, Objectives, Scope of Work (in‑scope & out‑of‑scope), Timeline & Milestones (simple table or numbered phases), Roles & Responsibilities, Success Metrics, Communication & Tools.

## Step 3 – Deliver & Offer File Export
After generating the four documents, ask the user which export format they prefer:

```
Your onboarding package is ready! Would you like me to:
- [ ] Export everything as a Word document (.docx)
- [ ] Export as a PDF
- [ ] Export as separate Markdown files
- [ ] Keep it here to copy‑paste (no export needed)
```
If an export is chosen, invoke the appropriate export skill (e.g., `docx-export`, `pdf-export`) and provide the downloadable files.

## Quality Standards
- **Specificity:** Use the actual client name, service type, and details; avoid placeholders.
- **AI‑native language:** Mention relevant AI concepts (LLMs, prompts, automation) where appropriate.
- **Tone consistency:** Warm, expert, and human.
- **No filler:** Every sentence must add value.
- **Length guidelines:** Questionnaire ~15 questions, welcome email ~250 words, agreement ~600 words, brief ~500 words (adjust as needed).

## Reference Files (optional)
- `references/service-types.md` – detailed scope notes per service type.
- `references/ai-industry-glossary.md` – common AI terms.
- `assets/email-subject-lines.md` – 20 subject‑line options.

Load these only when additional detail is required for a niche or complex service type.

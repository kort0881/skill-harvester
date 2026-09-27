---
name: "rulcode-development"
description: "Develop and extend the RulCode technical interview preparation platform built with React, Vite, TypeScript, and Supabase."
---

# RulCode Development

This skill guides contributors through adding or modifying features in the RulCode platform, a React/Vite/TypeScript application for technical interview preparation.

## Prerequisites
- Node.js (>=18) and npm installed
- Access to the repository `rkmahale17/rulcode.com`
- Familiarity with React, TypeScript, Tailwind CSS, and Supabase

## Workflow

### 1. Identify the target area
- **Algorithm problems** – files under `src/` (arrays, strings, trees, etc.)
- **Visualizations** – animation components (see `.agents/skills/visualization/SKILL.md`)
- **UI components** – React components using Tailwind and shadcn/ui (`components.json`)
- **Backend / data** – Supabase schema and functions in `supabase/`

### 2. Set up the development environment
```bash
npm install
npm run dev
```
The project uses Vite (`vite.config.ts`), TypeScript (`tsconfig.json`), and Tailwind CSS (`tailwind.config.ts`).

### 3. Implement the change
- Follow existing patterns in `src/` for file structure and naming.
- Respect strict TypeScript settings (`tsconfig.app.json`).
- Run ESLint (`eslint.config.js`) during development.
- Ensure new problems include difficulty metadata and language implementations.

### 4. Verify the change
```bash
npm run build
npm run lint
```
Open the development server and confirm the UI updates at the appropriate route.

### 5. Optional: Add tests
If the repository includes a testing framework, add unit or integration tests for new components or logic.

## References
- Project README
- `.agents/skills/visualization/SKILL.md` for visualization guidelines

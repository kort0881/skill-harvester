---
name: "sveltekit-svelte5-tailwind-skill"
description: "Comprehensive integration skill for building sites with SvelteKit 2, Svelte 5, and Tailwind CSS v4"
---

# SvelteKit 2 + Svelte 5 + Tailwind v4 Integration Skill

This skill provides comprehensive guidance for building modern web applications with the SvelteKit 2 + Svelte 5 + Tailwind CSS v4 stack.

## About This Integration Stack

**SvelteKit 2** is a modern full‑stack framework with:
- File‑based routing with layouts
- Server‑side rendering (SSR) and static site generation (SSG)
- Form actions with progressive enhancement
- Multiple deployment adapters (Vercel, Cloudflare, Node, static)

**Svelte 5** introduces a new reactivity system with:
- Runes: `$state()`, `$derived()`, `$effect()`, `$props()`
- Simplified component authoring
- Better TypeScript support
- Snippets replacing slots

**Tailwind CSS v4** offers:
- CSS‑first configuration
- New Vite plugin architecture
- Improved JIT performance
- Simplified setup

**Integration challenges this skill addresses:**
- Configuring all three tools to work together
- Understanding Svelte 5 runes in SSR context
- Progressive enhancement with form actions
- CSS loading in development and production
- Deployment across different platforms
- Migration from earlier versions

## How to Use This Skill

**CRITICAL: Research‑First Methodology**

When a user asks you to build something with this stack:

1. **Research first** – Search the documentation to understand:
   - How SvelteKit handles this use case
   - What Svelte 5 runes patterns apply
   - How to style with Tailwind v4
   - Common integration pitfalls to avoid
2. **Then execute** – Implement the solution using the knowledge gained from documentation

**Why this matters:**
- This integration has specific constraints (e.g., runes don’t work in SSR)
- The documentation provides authoritative guidance on configuration
- Researching first prevents mistakes that require rework
- You’ll implement solutions that follow best practices

**Workflow:**
1. User requests: "Help me build [feature] with SvelteKit/Svelte 5/Tailwind"
2. You search documentation using the process below
3. You understand the recommended approach
4. You implement the solution correctly the first time

## Documentation Collections

### `references/` (Problem‑Focused Guides)
17 curated guides addressing specific integration challenges:
- **Setup**: `getting-started.md`, `project-setup.md`
- **Core Concepts**: `svelte5-runes.md`, `routing-patterns.md`, `server-rendering.md`, `data-loading.md`
- **Forms & Styling**: `forms-and-actions.md`, `styling-with-tailwind.md`, `styling-patterns.md`
- **Deployment**: `deployment-guide.md`
- **Migration**: `migration-svelte4-to-5.md`, `tailwind-v4-migration.md`
- **Optimization**: `best-practices.md`, `performance-optimization.md`
- **Troubleshooting**: `common-issues.md`, `troubleshooting.md`
- **Search System**: `documentation-search-system.md`

### `docs/` (Comprehensive Reference)
7 adapted documentation guides covering complete APIs:
- `sveltekit-configuration.md` – Complete `svelte.config.js` and Vite config
- `svelte5-api-reference.md` – All Svelte 5 runes and template syntax
- `tailwind-configuration.md` – Tailwind v4 configuration options
- `adapters-reference.md` – Deployment adapter specifications
- `advanced-routing.md` – Advanced SvelteKit routing patterns
- `advanced-ssr.md` – SSR hooks, streaming, and optimization
- `integration-patterns.md` – Complete integration examples

## Searching Documentation

**IMPORTANT: Always search before implementing!**

This skill uses a 5‑stage search process for efficient documentation lookup:

### Stage 0: Discover Available Documentation
```bash
find . -name "index.jsonl" -type f
```
Expected output:
- `./references/index.jsonl` (17 problem‑focused guides)
- `./docs/index.jsonl` (7 comprehensive references)

Sample each collection to understand its scope:
```
Read references/index.jsonl with offset: 1, limit: 5
Read docs/index.jsonl with offset: 1, limit: 5
```
Determine which collection(s) are relevant to your query.

### Stage 1: Load Relevant Indexes
```
Read references/index.jsonl  # For how‑to guides and troubleshooting
Read docs/index.jsonl         # For API reference and configuration
```

### Stage 2: Reason About Candidates
Analyze the summaries to identify 3‑4 most relevant files (examples shown in the original skill).

### Stage 3: Get Section Details
```
Read references/sections.jsonl with offset: {index}, limit: 1
Read docs/sections.jsonl with offset: {index}, limit: 1
```
Analyze section summaries to pinpoint the exact sections that answer the query.

### Stage 4: Read Targeted Sections
```
Read references/getting-started.md with offset: 45, limit: 89
Read docs/svelte5-api-reference.md with offset: 120, limit: 65
```
Use the offset and limit from the `sections.jsonl` data for precise reading.

### Stage 5: Synthesize and Answer
Combine information from multiple sources:
1. Direct answer to the user’s question
2. Complete, runnable code examples
3. Integration‑specific considerations
4. File references for further reading

**Example file references:**
```
See: references/svelte5-runes.md:156-245 (Server‑Side Constraints)
See: docs/advanced-ssr.md:89-134 (SSR Load Functions)
```

For the full search methodology with examples, see `references/documentation-search-system.md`.

## Quick Start (5 Minutes)
For a complete walkthrough, search `references/getting-started.md`.

Basic setup commands:
```bash
# 1. Create SvelteKit project
npm create svelte@latest my-app
cd my-app
npm install

# 2. Add Tailwind v4
npm install -D tailwindcss@next @tailwindcss/vite@next

# 3. Configure Vite (vite.config.js)
import { sveltekit } from '@sveltejs/kit/vite';
import tailwindcss from '@tailwindcss/vite';

export default {
  plugins: [
    tailwindcss(),  // MUST be before sveltekit()
    sveltekit()
  ]
};

# 4. Create app.css
@import "tailwindcss";

# 5. Import in root layout (src/routes/+layout.svelte)
<script>
  import '../app.css';
</script>
<slot />

# 6. Verify
npm run dev
```
**Critical configuration:**
- Tailwind plugin **MUST** come before SvelteKit plugin in `vite.config.js`
- Import CSS in root `+layout.svelte` (not `app.html`)
- Use `@next` tag for Tailwind v4 packages

## Common Use Cases
- **Setup and Configuration** – Search `references/getting-started.md`, `references/project-setup.md`
- **Svelte 5 Runes with SSR** – Search `references/svelte5-runes.md` (see *Server‑Side Constraints*)
- **Forms & Progressive Enhancement** – Search `references/forms-and-actions.md`
- **Styling Components** – Search `references/styling-with-tailwind.md`, `references/styling-patterns.md`
- **Data Loading** – Search `references/data-loading.md`, `docs/advanced-ssr.md`
- **Deployment** – Search `references/deployment-guide.md`, `docs/adapters-reference.md`
- **Troubleshooting Errors** – Start with `references/common-issues.md`, then `references/troubleshooting.md`

## Common Issues and Quick Fixes
- **CSS not loading in production** – Verify Vite plugin order and CSS import location.
- **Runes causing SSR errors** – Do not use `$state()` or `$effect()` in SSR components.
- **Form losing state on submit** – Use manual `enhance()` callback as shown in the form pattern.
- **HMR breaking** – Check Vite plugin order and file‑watch settings.
- **Tailwind classes not working** – Ensure `content` paths in `tailwind.config.js` are correct and use full class names.

## Integration Patterns
```svelte
<!-- +page.svelte (SSR‑safe) -->
<script>
  export let data;
</script>

<ClientCounter initialCount={data.count} />
```
```svelte
<!-- ClientCounter.svelte (client‑only runes) -->
<script>
  let { initialCount } = $props();
  let count = $state(initialCount);
</script>
```
```svelte
<!-- Form with Progressive Enhancement -->
<script>
  import { enhance } from '$app/forms';
  let { form } = $props();
  let submitting = $state(false);
</script>

<form method="POST" use:enhance={() => {
  submitting = true;
  return async ({ result, update }) => {
    submitting = false;
    await update();
  };
}}>
  <!-- form fields -->
</form>
```
```svelte
<!-- Conditional Tailwind Classes -->
<script>
  let active = $state(false);
</script>

<!-- ✅ GOOD: Full class names -->
<div class:bg-blue-500={active} class:bg-gray-200={!active}>
  Button
</div>

<!-- ❌ BAD: Dynamic class parts -->
<div class="bg-{active ? 'blue' : 'gray'}-500">
  Button
</div>
```
For more patterns, search `docs/integration-patterns.md`.

## Best Practices
Search `references/best-practices.md` for guidance on project organization, component design, state management, styling conventions, performance, security, testing, and accessibility.

## Migration Guides
- **Svelte 4 → Svelte 5** – `references/migration-svelte4-to-5.md`
- **Tailwind v3 → v4** – `references/tailwind-v4-migration.md`

## Performance Optimization
Search `references/performance-optimization.md` for bundle size reduction, CSS purging, code‑splitting, image/font optimization, lazy loading, and Core Web Vitals improvements.

## Version Information
- **SvelteKit**: 2.x (latest stable)
- **Svelte**: 5.x (with runes)
- **Tailwind CSS**: 4.x (CSS‑first configuration)

All code examples and patterns are tested with these versions.

## Getting Help
1. **Start with search** – Use the 5‑stage process.
2. **Check common issues** – `references/common-issues.md`.
3. **Systematic debugging** – `references/troubleshooting.md`.
4. **Consult references** – Problem‑focused guides for specific topics.
5. **Check API docs** – Comprehensive references for configuration details.

## Skill Structure
```
sveltekit-svelte5-tailwind-skill/
├── SKILL.md                           # This file
├── references/                        # Problem‑focused guides (17 files)
│   ├── index.jsonl
│   ├── sections.jsonl
│   ├── index.meta.json
│   ├── documentation-search-system.md
│   ├── getting-started.md
│   ├── project-setup.md
│   ├── svelte5-runes.md
│   ├── forms-and-actions.md
│   ├── styling-with-tailwind.md
│   ├── server-rendering.md
│   ├── data-loading.md
│   ├── deployment-guide.md
│   ├── routing-patterns.md
│   ├── styling-patterns.md
│   ├── best-practices.md
│   ├── performance-optimization.md
│   ├── migration-svelte4-to-5.md
│   ├── tailwind-v4-migration.md
│   ├── common-issues.md
│   └── troubleshooting.md
├── docs/                              # Comprehensive references (7 files)
│   ├── index.jsonl
│   ├── sections.jsonl
│   ├── index.meta.json
│   ├── sveltekit-configuration.md
│   ├── svelte5-api-reference.md
│   ├── tailwind-configuration.md
│   ├── adapters-reference.md
│   ├── advanced-routing.md
│   ├── advanced-ssr.md
│   └── integration-patterns.md
├── provenance.jsonl                   # Source attribution
└── skill.manifest.json                # Skill metadata
```

## Distribution Mode
This skill uses **author‑only** distribution: all content is newly authored, no verbatim vendor documentation, and sources are cited in frontmatter (`adapted_from`).

**Remember:** Always search documentation before implementing! The research‑first approach prevents common mistakes and ensures you follow integration best practices.

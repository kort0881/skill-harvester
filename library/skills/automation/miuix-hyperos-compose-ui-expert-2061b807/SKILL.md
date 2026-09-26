---
name: "miuix"
description: "Miuix (HyperOS) Compose expert for UI construction, review, and refactoring."
---

# Miuix Skill

## Overview
Miuix is a Compose Multiplatform UI component library that implements Xiaomi HyperOS design language. It targets Android, iOS, Desktop (JVM), macOS, and Web (Wasm/JS) from a single Kotlin codebase.

### Modules
| Module | Purpose |
|--------|---------|
| `miuix-ui` | Core UI components – Button, Switch, TextField, NavigationBar, Scaffold, dialogs, etc. |
| `miuix-preference` | Settings‑screen components – SwitchPreference, CheckboxPreference, SliderPreference, dropdown selectors |
| `miuix-icons` | 100+ icons in 5 weights |
| `miuix-blur` | Backdrop blur, texture effects, progressive blur |
| `miuix-shader` | RuntimeShader abstraction layer |
| `miuix-squircle` | Squircle shape with API‑33 fallback |
| `miuix-nav` | Compose Multiplatform navigation runtime with serializable back‑stack |

## Key Concepts
- UI must be under an ancestor `MiuixTheme` providing `colorScheme` and `textStyles`.
- Use natural‑language color requests via the **Color semantics and visual lookup** reference; do not invent tokens.
- Overlay components render inside a `Scaffold`’s popup layer; window components render in an independent window layer.
- `PullToRefresh` uses hoisted `isRefreshing` and `rememberPullToRefreshState`.
- `miuix-nav` separates route/back‑stack from navigation chrome; routes must be `@Serializable`.

## Workflow
1. **Determine version** – inspect Gradle files or lock files; fall back to snapshot `0.9.4‑rc01` if unknown.
2. **Resolve code context** – decide if the request targets an existing screen, a standalone app, or an isolated snippet (see the *Resolve Code Context* table).
3. **Load required evidence** – read only the reference files needed for the intent (project setup, component catalog, design language, etc.).
4. **Classify scenario** – UI review, component implementation, migration, accessibility, etc.
5. **Select components** – map user‑spoken component names to the catalog before applying generic Compose advice.
6. **Verify APIs** – cross‑check signatures against the pinned source snapshot (`4a6b750b`).
7. **Implement** – follow the **Code Delivery Contract** (standalone app, page‑level integration, or component snippet).
8. **Validate** – compile, run, and capture visual proof (screenshot, emulator, device).

## Code Delivery Contract
| Scope | Deliverable |
|------|-------------|
| Standalone app | Complete `@Composable App` with `ThemeController`, `MiuixTheme`, required `Scaffold`, imports, and working state |
| Page integration | `@Composable` page function with hoisted state, required imports, and no duplicate root |
| Component snippet | Minimal call, required ancestor note, and necessary state/callbacks |

### Guidelines
- **Never fabricate APIs** – always verify against the source snapshot.
- **Prefer semantic tokens and `*Defaults` objects** over hard‑coded values.
- **Explicitly state required ancestors** (e.g., `MiuixTheme` + `Scaffold`).
- **Report verification facts** – API match, compilation status, visual validation.

## Guardrails
- Use only public Miuix components; do not mix Material‑3 unless explicitly requested.
- For color descriptions, map to existing tokens (`error`, `primary`, etc.) and avoid inventing `warning`/`alert` tokens.
- Verify navigation APIs (`NavKey`, `rememberNavBackStack`, `NavDisplay`) against the source.
- Ensure accessibility, adaptive layout, and platform‑specific behavior are respected.

---

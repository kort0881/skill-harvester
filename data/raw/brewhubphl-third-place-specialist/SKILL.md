---
name: third-place-specialist
description: Ray Oldenburg third-place frameworks, urban planning for community, social capital, age-friendly and child-friendly public space, community gardens, transit placemaking, and Dolley & Bosman edited volume concepts.
version: "1.0.0"
tags:
  - third-places
  - oldenburg
  - urban-planning
  - social-capital
  - community-gardens
  - transit
  - public-space
when_to_use:
  - Auditing whether a space qualifies as a third place (Oldenburg 8-test)
  - Reviewing master plans, MPCs, or "community hub" development claims
  - Age-friendly, child-friendly, or feminist inclusive public realm design
  - Community garden, transit station, or main-street activation briefs
  - CPTED / eyes-on-the-street safety claims tied to third-place clustering
  - Digital layers, AR, or heritage projects extending physical gathering
invocation_examples:
  - "Run the Oldenburg 8-test on this proposed community plaza"
  - "Does this locked community garden build bridging or only bonding capital?"
  - "Audit this New Urbanist town centre for planning-community traps"
  - "Review this transit station redesign for third-place-of-mobility qualities"
  - "Check this main street grant for Zone 1 pavement dining priorities"
disable-model-invocation: true
---

# Third-Place Specialist

Production guidance for agents applying Ray Oldenburg's third-place concept and the Dolley & Bosman edited volume *Rethinking Third Places*. This skill prioritizes **evidence-based audit** over marketing labels — form alone does not make community.

## Overview

Third places are informal public gathering settings—neither home (first) nor work/school (second)—where conversation is primary. The specialist skill teaches agents to:

1. Run the **Oldenburg eight-characteristic audit** before endorsing "community" claims.
2. Load deep patterns **on demand** from `patterns/` and `references/` — never bloat active context.
3. Map **bonding vs bridging** social capital when integration, ageing, or safety are goals.

### Progressive disclosure map

| Need | Load |
|------|------|
| Quick routing / priorities | This file → [AGENTS.md](AGENTS.md) |
| Five core principles | [PRINCIPLES.md](PRINCIPLES.md) |
| Oldenburg 8-test audit | `patterns/oldenburg-eight-test.md` |
| Programming format = who shows up (bridging vs bonding) | `patterns/programming-format-audit.md` |
| Master plan / New Urbanism critique | `patterns/planning-community-traps.md` |
| Feminist inclusion audit | `patterns/feminist-third-place-audit.md` |
| Age-friendly / weak ties | `patterns/ageing-social-health.md` |
| Evidence-based place design | `patterns/evidence-based-design.md` |
| CPTED / eyes on the street | `patterns/eyes-on-street-safety.md` |
| Community gardens | `patterns/community-garden-design.md` |
| Transit as mobility third place | `patterns/transit-third-place.md` |
| Digital / AR layers | `patterns/digital-layers.md` |
| Main street / pavement dining | `patterns/street-life-activation.md` |
| What never to assume | [anti-patterns.md](anti-patterns.md) |
| Abstract planning scenarios | [examples/third-place-planning.md](examples/third-place-planning.md) |
| Quick tables & decision trees | [references/cheatsheet.md](references/cheatsheet.md) |
| Term definitions | [references/glossary.md](references/glossary.md) |
| Book chapter drops | [references/book-summaries/rtp-index.md](references/book-summaries/rtp-index.md) |

---

## Core Principles (summary)

Full text: [PRINCIPLES.md](PRINCIPLES.md).

1. **Conversation is the test** — not the "community hub" label.
2. **Planning enables or destroys** — it rarely installs gemeinschaft.
3. **Weak ties are infrastructure** — bridging beats bonding-only when integrating neighbours.
4. **No place is neutral** — audit emplacement, intersectionality, platform governance.
5. **Layer, don't replace** — digital and transit extensions anchor on physical gathering.

---

## Oldenburg Eight-Characteristic Audit

Use as the **shared diagnostic** across every chapter:

| # | Criterion | Pass if… |
|---|-----------|----------|
| 1 | Neutral ground | Voluntary meeting; neither home nor work |
| 2 | Leveller | Status differences fade |
| 3 | Easy access | Walkable; accommodates linger + activity |
| 4 | Regulars | Known characters anchor social life |
| 5 | Low profile | Informal, unpretentious |
| 6 | Playful | Humour, games, light mood |
| 7 | Home away from home | Emotional comfort, return habit |
| 8 | Conversation primary | Talk is the main activity |

**Rule:** Score ≥6 with **conversation** and **neutral ground** mandatory. See [references/cheatsheet.md](references/cheatsheet.md).

---

## Social Capital Quick Routing

| Goal | Prefer | Pattern / chapter |
|------|--------|-------------------|
| Integrate newcomers | Open garden, café regulars, transit hub | Ch 8, `community-garden-design.md` |
| Bridge across difference (gentrifying area) | Culturally-owned formats (dominoes, spoken-word, gospel) | `programming-format-audit.md` |
| Ageing in place | Walkable club/library within 10 min | Ch 3, `ageing-social-health.md` |
| Child social health | Free playful public realm | Ch 4 |
| Safety perception | Mixed use + active frontages + programming | Ch 6 — not third-place count alone |
| Heritage memory | DIY archive with participant ownership | Ch 7 |

**Bonding** (strong ties, similar people) vs **bridging** (weak ties, diverse neighbours) — Putnam/Granovetter (Chs 3, 8).

---

## Common Pitfalls

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| "Town centre" feels empty | Form without conversation primacy | `planning-community-traps.md` |
| Programming only draws newcomers | Generic hobby format is a demographic filter | `programming-format-audit.md` |
| Garden doesn't integrate neighbours | Locked club model | `community-garden-design.md` |
| Seniors isolated after driving stops | Car-dependent MPC amenity only | `ageing-social-health.md` |
| Retail strip still feels unsafe | CPTED visibility without programming | `eyes-on-street-safety.md` |
| AR app unused socially | Mediated layer replaces F2F | `digital-layers.md` |
| Main street beautification no effect | Hard edges, no Zone 1 dining | `street-life-activation.md` |

Full catalog: [anti-patterns.md](anti-patterns.md).

---

## Chapter Index (book summaries)

Start at [rtp-index.md](references/book-summaries/rtp-index.md). Load **one** chapter file per task.

| # | Title | File |
|---|-------|------|
| 1 | Rethinking third places and community building | `rtp-ch01-rethinking-third-places.md` |
| 2 | Feminist perspectives | `rtp-ch02-feminist-perspectives.md` |
| 3 | Planning for healthy ageing | `rtp-ch03-healthy-ageing.md` |
| 4 | Child-friendly third places | `rtp-ch04-child-friendly.md` |
| 5 | Evidence-based urban development | `rtp-ch05-evidence-based-planning.md` |
| 6 | Eyes on the street | `rtp-ch06-eyes-on-the-street.md` |
| 7 | Music heritage as third place | `rtp-ch07-music-heritage.md` |
| 8 | Community gardens & social capital | `rtp-ch08-community-gardens.md` |
| 9 | Third places in the ether | `rtp-ch09-digital-layers.md` |
| 10 | Third places in transit | `rtp-ch10-transit-third-places.md` |
| 11 | Street life contribution | `rtp-ch11-street-life.md` |

**Book metadata:** Dolley & Bosman (eds.), Edward Elgar, ~240 pp., ISBN 9781786433916. PDF gitignored at repo root.

---

## Topic Index

- **Oldenburg eight characteristics** → Ch 1, 8; `oldenburg-eight-test.md`
- **Programming format / bridging vs bonding filter** → `programming-format-audit.md`
- **Garden City / New Urbanism** → Ch 1; `planning-community-traps.md`
- **Feminist geography / emplacement** → Ch 2; `feminist-third-place-audit.md`
- **Weak ties / ageing** → Ch 3; `ageing-social-health.md`
- **Child-friendly cities** → Ch 4
- **Place-making / Cilliers** → Ch 5; `evidence-based-design.md`
- **CPTED / crime** → Ch 6; `eyes-on-street-safety.md`
- **Music heritage / virtual third place** → Ch 7, 9
- **Community gardens** → Ch 8; `community-garden-design.md`
- **Digital layers / AR** → Ch 9; `digital-layers.md`
- **Public transport** → Ch 10; `transit-third-place.md`
- **Pavement dining / street life** → Ch 11; `street-life-activation.md`

---

## Scope & Limits

This skill covers the Dolley & Bosman edited volume and Oldenburg-derived frameworks. It does not replace local zoning codes, engagement processes, or site-specific ethnography. Combine with project tools and community consultation for implementation.

Ray Oldenburg's *The Great Good Place* (1989) is the foundational source; this volume extends and critiques the concept across disciplines and international sites.

---

## Onboarding for Book-to-Skill Outputs

Use `references/book-summaries/` for modular chapter drops. Workflow:

1. Add `references/book-summaries/<slug>.md` — do **not** paste the full book into `SKILL.md`.
2. Extract durable rules into `patterns/` when they become team standards.
3. Move repeated mistakes into `anti-patterns.md`.
4. Run `node scripts/validate-skill.mjs` before PR.

See [references/book-summaries/README.md](references/book-summaries/README.md) for the template.

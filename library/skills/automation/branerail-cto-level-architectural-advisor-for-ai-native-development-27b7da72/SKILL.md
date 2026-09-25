---
name: "branerail"
description: "CTO‑level architectural advisor for AI‑native development. Use this skill for architecture reviews, resilience analysis, state ownership, scaling decisions, and design‑system definition. Integrates with Claude Code to audit generated code and produce DESIGN.md specifications."
---

# Branerail Skill: CTO‑Level Agent for AI‑Native Development

**Core principle** – AI can generate code at lightspeed, but the architect must conduct the orchestra. This skill provides a repeatable process for turning AI‑generated code into robust, observable, and scalable systems.

## When to Trigger This Skill

Use for:
1. Architecture from scratch
2. Code‑quality audits of AI‑generated code
3. Resilience and failure‑mode analysis
4. State ownership and data‑flow clarification
5. Scaling and bottleneck planning
6. Refactoring or migration projects
7. Observability and monitoring design
8. DESIGN.md creation for UI consistency
9. Dependency mapping and blast‑radius analysis
10. Concurrency and distributed‑system concerns

**Trigger keywords** (use liberally): `architecture`, `design`, `scale`, `failure`, `state`, `blast radius`, `dependency`, `concurrency`, `microservices`, `monolith`, `observability`, `DESIGN.md`, `Claude Code`, etc.

## Part 1 – The Three Pillars of Systems Thinking

### Pillar 1: Where Does State Live?
- **Audit steps**: inventory mutable state, identify authoritative owner, check replicas, trace mutation paths.
- **Pattern table** with trade‑offs (Single Source of Truth, Write‑Through Cache, Event Sourcing, CQRS, etc.).
- **Red‑flags** and a code‑review checklist.

### Pillar 2: Where Does Feedback Live?
- Identify critical operations, define success/failure, instrument logging, metrics, tracing, and alerts.
- Example of good vs. bad structured logs.
- Metrics to track and alerting strategies.
- Checklist for observability.

### Pillar 3: What Breaks If I Delete This?
- Perform a mental deletion test for any component.
- Document blast‑radius, SPOFs, and fallback strategies.
- Dependency‑mapping table and checklist.

## Part 2 – Design Process Before Code

1. **Sketch the Architecture** – boxes, arrows, state owners, external deps, fallbacks.
2. **Write a Design Document** – `DESIGN.md` for UI tokens **or** an architectural spec (`spec.md`). Sample `DESIGN.md` front‑matter and sections are provided.
3. **Run the Deletion Test** – mental checklist for each component.
4. **Manual Re‑implementation** – rewrite AI‑generated code from memory to ensure understanding.

## Part 3 – AI as a Probabilistic Collaborator

Contrast deterministic compilers with LLMs. Highlight typical AI‑generated pitfalls (auth bypasses, off‑by‑one, silent failures, race conditions) and the auditor’s role.

## Part 4 – Code Review Checklist for AI‑Generated Code

- Spec compliance
- State & data ownership
- Error handling
- Observability
- Dependency management
- Concurrency & consistency
- Testing coverage
- Performance & scaling
- Security

## Part 5 – Architectural Anti‑Patterns

Table of common anti‑patterns (no state ownership, silent failures, circular deps, SPOFs, etc.) with fixes.

## Part 6 – Full Development Workflow

1. **Pre‑Code** – problem definition, sketch, three‑pillar answers, spec writing.
2. **Code Generation** – prompt Claude Code with spec and `DESIGN.md`.
3. **Code Review** – run checklist, verify pillars.
4. **Deployment** – deletion test, monitoring verification.
5. **Post‑Deployment** – manual re‑implementation, spec updates, iteration.

## Part 7 – Concurrency & Distributed‑System Patterns

Mutex/Lock, Atomic ops, Immutable data, Channels/Queues, Transactions, Consensus, Eventual consistency, Event sourcing, CQRS, Circuit breaker – description, risks, testing advice.

## Part 8 – Claude Code Integration Workflow

- Initialize project with `DESIGN.md` and spec scaffolding.
- Example prompts that reference specs, enforce observability, and request resilience patterns.

## Part 9 – Advanced Architectural Patterns (SOTA)

Cell‑based architecture, Sidecar/Service Mesh, Strangler Fig, Sagas – when to use and benefits.

## Part 10 – Cloud‑Native Resilience Suite

Brief mention of adaptive throttling and other self‑healing techniques (truncated in original).

---
*End of Branerail skill.*

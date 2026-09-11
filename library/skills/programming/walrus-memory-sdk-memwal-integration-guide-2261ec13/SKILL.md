---
name: "memwal"
description: "Walrus Memory SDK – portable agent memory across apps, sessions, and workflows."
---

# Walrus Memory — Portable Agent Memory

Walrus Memory enables AI agents to operate reliably across apps and sessions without losing context. It stores memories on Walrus (decentralized storage), encrypts them with SEAL, enforces ownership on‑chain via Sui smart contracts, and retrieves them with semantic (vector) search. Memory is portable by design— not tied to a single runtime or provider— and scoped by `owner + namespace` for isolation and coordination.

## When to Use

- **Portable memory** – persists outside prompts and context windows, moves across agents, apps, and workflows
- **Full owner control** – programmable permissions and explicit ownership define how memory is shared and accessed
- **Agent coordination** – shared memory spaces help agents coordinate across long‑running and multi‑step workflows
- **Semantic recall** – retrieve memories by meaning, not just keywords
- **Verifiable integrity** – memory integrity can be independently verified without centralized trust
- **Cross‑app memory** – not tied to a single runtime or provider, share memory between apps via delegate keys

## When NOT to Use

- Temporary conversation context that only matters in the current session
- Large file storage (Walrus Memory is optimized for text memories)
- Use cases that don't need encryption or decentralization

## Installation

```bash
# Install the SDK
pnpm add @mysten-incubation/memwal

# Optional: for Vercel AI SDK integration
pnpm add ai zod

# Optional: for manual client (client‑side SEAL encryption)
pnpm add @mysten/sui @mysten/seal @mysten/walrus
```

## Quick Start

### 1. Get Your Credentials
You need a **delegate key** (Ed25519 private key) and **account ID** (Walrus Memory account object ID on Sui). Generate them at:
- Production: https://memory.walrus.xyz
- Staging: https://staging.memory.walrus.xyz

### 2. Initialize the SDK

```ts
import { MemWal } from "@mysten-incubation/memwal";

const memwal = MemWal.create({
  key: process.env.MEMWAL_PRIVATE_KEY!,
  accountId: process.env.MEMWAL_ACCOUNT_ID!,
  serverUrl: process.env.MEMWAL_SERVER_URL ?? "https://relayer.memory.walrus.xyz",
  namespace: "my-app",
});
```

### 3. Store and Recall Memories

```ts
// Store one already‑distilled fact and wait until it is indexed.
await memwal.rememberAndWait(
  "User prefers dark mode and works in TypeScript.",
  undefined,
  { timeoutMs: 30_000 },
);

// Recall by meaning
const result = await memwal.recall({ query: "What are the user's preferences?" });
console.log(result.results);

// Extract facts from free‑form text and wait until all accepted facts are indexed.
const analyzed = await memwal.analyzeAndWait(
  "I live in Hanoi and prefer dark mode.",
  undefined,
  { timeoutMs: 30_000 },
);
console.log(analyzed.facts.map((f) => f.text));

// Check relayer health
await memwal.health();
```

Use `*AndWait` when a UI saves and then immediately recalls in the same flow. Indexing can lag a few seconds, so `remember()` / `analyze()` may return before recall can find the new memory. Manual polling is still available for advanced async UIs:

```ts
const accepted = await memwal.remember("User likes Sui.");
const stored = await memwal.waitForRememberJob(accepted.job_id, {
  pollIntervalMs: 750,
  timeoutMs: 30_000,
});
```

## SDK Entry Points

| Entry Point | Import | Description |
|---|---|---|
| `MemWal` | `@mysten-incubation/memwal` | Default. Relayer handles embedding, SEAL encryption, Walrus upload, vector search |
| `MemWalManual` | `@mysten-incubation/memwal/manual` | Manual flow – client handles embedding and SEAL encryption |
| `withMemWal` | `@mysten-incubation/memwal/ai` | Vercel AI SDK middleware – auto recall + save around AI conversations |
| Account utils | `@mysten-incubation/memwal/account` | Account creation, delegate key management |

## API Surface

### Walrus Memory Methods

| Method | Description | Returns |
|---|---|---|
| `remember(text, namespace?)` | Accept one memory job immediately | `{ job_id, status }` |
| `rememberAndWait(text, namespace?, opts?)` | Store one memory and wait for completion | `{ id, job_id, blob_id, owner, namespace }` |
| `recall({ query, limit?, topK?, namespace?, maxDistance? })` *(preferred)* | Semantic search for memories | `{ results: [{ blob_id, text, distance }], total }` |
| `analyze(text, namespace?)` | Extract facts and accept one memory job per fact | `{ job_ids, facts, fact_count, status, owner }` |
| `analyzeAndWait(text, namespace?, opts?)` | Extract facts and wait for all fact jobs to complete | `{ results, facts, total, succeeded, failed, owner }` |
| `restore(namespace, limit?)` | Rebuild missing index entries from Walrus | `{ restored, skipped, total, namespace, owner }` |
| `health()` | Check relayer health | `{ status, version }` |
| `getPublicKeyHex()` | Get hex‑encoded public key | `string` |

### Lower‑Level Methods

| Method | Description |
|---|---|
| `rememberManual({ encryptedData, vector, namespace? })` | Send SEAL‑encrypted bytes + pre‑computed vector; relayer uploads |
| `recallManual({ vector, limit?, namespace? })` | Search with pre‑computed vector (returns blob IDs only) |
| `embed(text)` | Generate embedding vector (no storage) |

*(Full TypeScript response interfaces are omitted for brevity.)*

## Namespace Semantics

A namespace is an **opaque, flat string label** scoped to a single owner. It isolates memory: a recall in namespace `A` never returns entries written to namespace `B`, even for the same owner, and never returns entries belonging to other owners.

- Validation: any non‑empty string is accepted; no length cap or character whitelist.
- Flat, not hierarchical: slashes and dots have no special meaning.
- Overwrite behavior: `remember()` always appends; it never upserts.
- Isolation guarantees are enforced at the SQL level, ensuring no cross‑owner or cross‑namespace leakage.

## Restore Semantics

`restore(namespace, limit?)` rebuilds **missing** local index entries for a namespace from Walrus. It is a recovery operation, not a full sync. Defaults to a limit of `10`; larger limits increase latency linearly.

## Recall Distance and Filtering

`recall()` returns the closest K memories by vector distance. Use `maxDistance` or client‑side filtering to discard weak matches:

```ts
const memories = await memwal.recall({
  query: "what did I eat yesterday?",
  limit: 10,
  namespace: "reading-tracker",
  maxDistance: 0.7,
});
```

## Configuration

```ts
MemWal.create({
  key: "<delegate‑private‑key>",
  accountId: "<account‑object‑id>",
  serverUrl: "https://relayer.memory.walrus.xyz", // optional
  namespace: "default", // optional
});
```

## Vercel AI SDK Integration

```ts
import { openai } from "@ai-sdk/openai";
import { streamText } from "ai";
import { withMemWal } from "@mysten-incubation/memwal/ai";

const model = withMemWal(openai("gpt-4o"), {
  key: process.env.MEMWAL_PRIVATE_KEY!,
  accountId: process.env.MEMWAL_ACCOUNT_ID!,
  serverUrl: "https://relayer.memory.walrus.xyz",
  namespace: "chat",
  maxMemories: 5,
  autoSave: true,
  minRelevance: 0.3,
});

const result = streamText({
  model,
  messages: [{ role: "user", content: "What do you remember about me?" }],
});
```

The middleware automatically recalls relevant memories before generation and extracts/saves facts after generation.

## OpenClaw / NemoClaw Plugin

```bash
openclaw plugins install @mysten-incubation/oc-memwal
```

Configure in `~/.openclaw/openclaw.json`:

```json
{
  "plugins": {
    "slots": { "memory": "oc-memwal" },
    "entries": {
      "oc-memwal": {
        "enabled": true,
        "config": {
          "privateKey": "${MEMWAL_PRIVATE_KEY}",
          "accountId": "0x...",
          "serverUrl": "https://relayer.memory.walrus.xyz"
        }
      }
    }
  }
}
```

Lifecycle hooks inject memories before prompts and capture facts after agent responses.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `health()` returns error | Verify relayer URL and network connectivity |
| `recall()` returns empty | Ensure the namespace matches the one used in `remember()` |
| `recall()` returns unrelated filler | Apply `maxDistance` filter or increase relevance threshold |
| `401 Unauthorized` | Check that `MEMWAL_PRIVATE_KEY` and `MEMWAL_ACCOUNT_ID` correspond to the selected relayer (staging vs production) |
| SDK import errors | Ensure Node.js ≥ 18 and the package is installed |
| Manual client errors | Install peer dependencies `@mysten/sui @mysten/seal @mysten/walrus` |
| Forget expectations unclear | `POST /api/forget` removes vector index rows; blobs remain on‑chain until epoch expiry |

## Brand Terminology

| Surface | Canonical term | Notes |
|---|---|---|
| Product / docs / UI | **Walrus Memory** | User‑facing name |
| Package / env vars / internal shorthand | **memwal** | Code and tooling identifier |

## Links

- Docs: https://memory.walrus.xyz
- SDK on npm: https://www.npmjs.com/package/@mysten-incubation/memwal
- GitHub: https://github.com/MystenLabs/MemWal
- Dashboard: https://memory.walrus.xyz

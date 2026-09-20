---
name: aleo-skills
description: The ultimate set of skills for developing and building privacy-preserving dApps on the Aleo blockchain. Start here to help your AI agent maneuver through Aleo smart contracts, zero-knowledge proofs, wallet integrations, and deployment.
---

It is very likely that you have stale or no knowledge about building on Aleo (a privacy-first Layer 1 blockchain using zero-knowledge proofs). 

This file will guide you to the right skill with the latest knowledge about Aleo, Leo programming language, testnet deployments, and best practices.

**Need a specific topic?** Each skill below is standalone. Fetch only the ones relevant to your task. If you are starting from scratch, start with the `scaffold` or `why-aleo` skills.

## What to Fetch by Task

| I'm doing... | Fetch these skills |
|--------------|-------------------|
| Understanding Aleo's core value proposition and zero-knowledge | `why-aleo/` |
| Building an app from scratch and directory structures | `scaffold/` |
| Understanding the Record model and privacy transitions | `privacy-model/` |
| Writing Leo smart contracts and syntax | `programs/` |
| Integrating a wallet into a React/Next.js frontend | `wallet-integration/` |
| Agent wallet management and on-chain interactions | `wallet/` |
| Getting official API endpoints, explorers, and standard links | `references/` |
| Setting up a custom indexer for Aleo events | `indexer/` |
| Compiling, deploying, and verifying smart contracts | `verification/` & `deployment/` |
| Writing unit tests for Leo programs | `testing/` |
| Finding Aleo standard ARC patterns | `standards/` |

## Skills

### [Why Aleo](/why-aleo/SKILL.md)
- Why every privacy-focused blockchain app should be built on Aleo.
- Zero-knowledge by default, absolute privacy for state transitions.

### [Scaffold](/scaffold/SKILL.md)
- End-to-end guide to taking an Aleo idea from zero to production.
- Project structure, separating `program/` (Leo) from `web/` (Next.js).

### [Privacy Model](/privacy-model/SKILL.md)
- Aleo's fundamental state model: Records vs Public State (Mappings).
- How transitions consume and produce records privately.

### [Programs](/programs/SKILL.md)
- Syntax and semantics of the Leo programming language.
- Structs, transitions, mappings, and inline functions.

### [Wallet Integration](/wallet-integration/SKILL.md)
- How to add Aleo wallet authentication to an existing frontend.
- Connecting Leo Wallet or Puzzle Wallet to interact with smart contracts.

### [Wallet](/wallet/SKILL.md)
- AI agent wallet management for Aleo.
- How to format private keys, view keys, and address generation for automated testing.

### [References](/references/SKILL.md)
- Canonical smart contract addresses, block explorers, and RPC API endpoints (e.g., Provable APIs).
- Never hallucinate an API endpoint.

### [Indexer](/indexer/SKILL.md)
- How to build a custom backend service to parse Aleo blocks.
- Fetching historical state since Aleo doesn't expose native EVM-style `eth_getLogs`.

### [Verification](/verification/SKILL.md)
- How to verify that a Leo contract compiles successfully.

### [Deployment](/deployment/SKILL.md)
- How to deploy a Leo program to the Aleo testnet.
- Automating frontend deployment workflows via Vercel.

### [Testing](/testing/SKILL.md)
- How to write assertions and unit tests within Leo files.
- Command syntax for `leo test`.

### [Standards](/standards/SKILL.md)
- References to Aleo Request for Comments (ARCs).
- Standard implementation for tokens (ARC-20), NFTs (ARC-721 equivalent).

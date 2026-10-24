---
name: "credit-optimizer"
description: "Optimize AI agent credit usage by classifying tasks and routing them to the most cost‑efficient model tier, reducing API costs while preserving output quality."
---

# Credit Optimizer v5

**Automatically optimize AI agent credit/token usage by routing tasks to the most cost‑efficient execution path — with zero quality loss.**

## Prerequisites
- Access to at least two model tiers (e.g., a free tier and a paid standard/premium tier) via a programmable API.
- Ability to programmatically select the model for each request.
- Optional: a simple caching layer to store recent task results.

## When to Use This Skill
- Before executing any AI task that consumes credits or tokens.
- When you need to minimize API costs without sacrificing output quality.
- When processing batches of tasks with varying complexity.
- When you must decide between different model tiers (free, standard, premium).

## How It Works
### 1. Task Classification
Classify the incoming task into one of the following categories:

| Category          | Examples                                 | Typical Savings |
|-------------------|------------------------------------------|-----------------|
| Simple Q&A        | Definitions, facts, conversions          | 90‑100% (free)  |
| Code Generation   | Scripts, functions, refactoring          | 40‑60%          |
| Research          | Multi‑source analysis, synthesis         | 20‑40%          |
| Creative Writing  | Articles, stories, marketing copy        | 30‑50%          |
| Data Analysis     | CSV processing, visualization            | 40‑70%          |
| Complex Reasoning | Multi‑step logic, architecture design    | 10‑20%          |

### 2. Prompt Quality Check
1. **Clarity Score (1‑10)** – If < 5, ask the user for clarification before proceeding.
2. **Scope Detection** – Determine whether the request can be split into smaller, cheaper sub‑tasks.
3. **Data Requirement Check** – If real‑time data is needed, fetch it first with a cheap tool, then process.

### 3. Model Routing
```text
IF task is Simple Q&A or formatting:
    → Use FREE tier (no credits)
ELSE IF task is medium complexity (code, writing, basic analysis):
    → Use STANDARD tier
ELSE IF task requires deep reasoning, multi‑step logic, or high‑quality creativity:
    → Use PREMIUM/MAX tier
ELSE IF task is mixed complexity:
    → SPLIT into sub‑tasks and route each independently
```

### 4. Execution Optimizations
- **Context Pruning** – Include only the relevant portion of the conversation.
- **Output Scoping** – Request a specific format to avoid verbose replies.
- **Caching** – Re‑use results of recent, similar tasks.
- **Batch Processing** – Group homogeneous sub‑tasks for a single API call.

## Efficiency Directives
1. Never use premium models for tasks that standard models can handle equally well.
2. Always check the cache or known information before invoking an API.
3. Split compound requests into atomic tasks before routing.
4. Ask for clarification on vague prompts – it is cheaper than re‑doing work.
5. Use structured output formats to reduce token waste.

## Audit Results Summary
| Metric                | Result |
|-----------------------|--------|
| Scenarios tested      | 53     |
| Average savings       | 30‑75% |
| Quality loss          | 0%     |
| Quality improvement   | 2 cases |
| False routing rate    | < 3%   |

## Links
- **Website**: https://creditopt.ai
- **GitHub**: https://github.com/rafsilva85/manus-credit-optimizer
- **MCP Server**: Python MCP server for programmatic integration
- **Full Manus Skill**: https://rafaamaral.gumroad.com/l/credit-optimizer-v5 (one‑time $29)

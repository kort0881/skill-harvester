# Curated Agent Skills Library

Автоматически собранная и проверенная библиотека Agent Skills.

Последнее обновление: `2026-09-11T12:22:20+00:00`

Активных skills: **12**

## Категории

### automation

| Skill | Описание | Теги | Источник |
|---|---|---|---|
| [Chinese Resume JD Optimizer](./skills/automation/chinese-resume-jd-optimizer-cbb3f2a7/SKILL.md) | A comprehensive workflow for optimizing Chinese resumes against specific job descriptions. It guides users through input collection, JD parsing, gap analysis, targeted questioning, resume rewriting, and multi‑layered risk checks, ensuring factual accuracy and ATS/HR friendliness. The skill enforces strict anti‑fabrication rules and adapts to various input scenarios (full JD + resume, resume‑only, JD‑only, or insufficient data). | resume, jd, optimization, chinese, automation, career | coinluu/resume-jd-optimizer-cn |
| [Offline Evidence‑Aware Visual Explainer Generator](./skills/automation/offline-evidence-aware-visual-explainer-generator-bd2264e2/SKILL.md) | A Node.js‑based workflow that turns a technical concept, module, trade‑off, or incident into a self‑contained, evidence‑tagged HTML explainer. It defines a strict spec‑first approach, validation steps, and deterministic rendering without any network access. | automation, visualization, evidence, offline, nodejs | yizhiyanhua-ai/fireworks-open-eli5 |
| [Personal IP Diagram Creator](./skills/automation/personal-ip-diagram-creator-52c958e2/SKILL.md) | A workflow that turns a user‑provided personal photo, profile screenshot, bio or other identity material into a reusable set of minimalist hand‑drawn visual assets. The skill builds a stable “IP character”, extracts core content from long‑form text, selects an appropriate visual mode (hand‑drawn illustration, knowledge‑card or PPT), and generates or outputs prompts for image‑generation tools. It includes safety checks, environment detection, QA, and repair steps. | personal ip, visual generation, automation, content creation | haloshin/ip-diagram-creator |

### content-creation

| Skill | Описание | Теги | Источник |
|---|---|---|---|
| [Markit – Convert Files and URLs to Markdown](./skills/content-creation/markit-convert-files-and-urls-to-markdown-fbf180c9/SKILL.md) | Markit is a Node‑based CLI and SDK that extracts the textual content of many document types (PDF, DOCX, PPTX, HTML, etc.) and returns it as clean Markdown. It can process local files, remote URLs, and GitHub resources, offering raw markdown or JSON output. The skill includes usage examples for both the command line and TypeScript SDK. | content_creation, markdown, cli, sdk, nodejs, file_conversion | shift-labs-ai/markit |

### design

| Skill | Описание | Теги | Источник |
|---|---|---|---|
| [Godot Solana SDK Integration Guide](./skills/design/godot-solana-sdk-integration-guide-f5eb7d66/SKILL.md) | This skill provides a comprehensive, step‑by‑step guide for integrating the Godot Solana SDK into Godot 4 projects. It covers installation, configuration, core nodes, transaction workflow, wallet adapters, and common pitfalls, with concrete GDScript examples. The guide enables developers to build blockchain‑enabled games that can send Solana transactions, manage SPL tokens, mint NFTs, and interact with Anchor programs directly from Godot. | godot, solana, blockchain, gdscript, sdk, gaming | Virus-Axel/godot-solana-sdk |

### devops

| Skill | Описание | Теги | Источник |
|---|---|---|---|
| [Graphsignal Profiler Setup for Inference Workloads](./skills/devops/graphsignal-profiler-setup-for-inference-workloads-f30f3b93/SKILL.md) | This skill explains how to install, configure, and run the Graphsignal Profiler for GPU‑accelerated inference services such as vLLM, SGLang, PyTorch, and dstack. It covers both the CLI sidecar (`graphsignal‑run`) and the in‑process Python entry point (`graphsignal.watch()`), including optional OpenTelemetry tracing and Docker usage. The guide provides concrete commands, environment variables, and engine‑specific notes to get profiling and monitoring up and running quickly. | gpu, profiling, inference, vllm, sglang, pytorch | graphsignal/graphsignal-profiler |
| [Total Recall – Autonomous Agent Memory Skill](./skills/devops/total-recall-autonomous-agent-memory-skill-096b202d/SKILL.md) | Total Recall is an autonomous memory skill for OpenClaw agents that observes conversation logs, compresses them with LLMs, and maintains a prioritized observations file without external databases. It includes a multi‑layer architecture with cron‑based observer, reflector consolidation, session recovery, Linux inotify watcher, and an optional nightly Dream Cycle for deeper archiving. | memory, agent, devops, automation, linux, llm | gavdalf/total-recall |

### ecommerce

| Skill | Описание | Теги | Источник |
|---|---|---|---|
| [Review Analyzer Skill – AI‑driven e‑commerce review and VOC analysis](./skills/ecommerce/review-analyzer-skill-ai-driven-e-commerce-review-and-voc-analysis-d9379fed/SKILL.md) | The skill ingests product reviews (CSV or Sellersprite) and produces a 22‑dimension AI‑tagged dataset, a 15‑chapter insight report, optional visual dashboards and Feishu synchronization. It guides the agent through parameter collection, deterministic Python steps and LLM‑driven tagging/report writing. The workflow is modular, resumable and suitable for both autonomous agents and CLI use. | ecommerce, review‑analysis, voc, report‑generation, visualization, feishu‑sync | buluslan/review-analyzer-skill |

### ml

| Skill | Описание | Теги | Источник |
|---|---|---|---|
| [Agentic Kaggle Competition Workflow](./skills/ml/agentic-kaggle-competition-workflow-cc0cea7c/SKILL.md) | A comprehensive, step‑by‑step workflow for running end‑to‑end Kaggle competitions, covering validation, data handling, model development, multi‑notebook pipelines, off‑loading to Kaggle, and submission tracking. Includes resource references, default procedures, hygiene guidelines, and ready‑to‑run helper scripts. | kaggle, machine‑learning, competition, workflow, automation | FrankS-IntelLab/agentic-kaggle-skill |

### programming

| Skill | Описание | Теги | Источник |
|---|---|---|---|
| [Repo Task Proof Loop](./skills/programming/repo-task-proof-loop-3324eff9/SKILL.md) | A repo‑local workflow that creates a structured task folder, installs project‑scoped Codex and Claude subagents, and manages a repeatable spec‑freeze → build → evidence → verify → fix loop. It updates AGENTS.md and the repository’s Claude guide with managed workflow blocks and provides a set of CLI commands to drive each phase. The skill is designed for large coding tasks that require auditable proof of implementation. | repo, workflow, coding, automation, subagents | DenisSergeevitch/repo-task-proof-loop |
| [Walrus Memory SDK (memwal) Integration Guide](./skills/programming/walrus-memory-sdk-memwal-integration-guide-2261ec13/SKILL.md) | This skill provides a comprehensive guide to integrating the Walrus Memory SDK (memwal) into applications. It covers installation, configuration, API usage, Vercel AI SDK middleware, and troubleshooting, enabling developers to add portable, encrypted, and semantically searchable memory to AI agents. The documentation includes practical code snippets for TypeScript and notes on namespace management and security best practices. | memory, sdk, walrus, sui, typescript, semantic-search | MystenLabs/MemWal |

### writing

| Skill | Описание | Теги | Источник |
|---|---|---|---|
| [Tianming Novel Collaborative Writing System](./skills/writing/tianming-novel-collaborative-writing-system-ef60e762/SKILL.md) | A structured AI‑assisted system for co‑authoring long‑form novels. It defines a set of commands (outline, plan, directory, draft, manuscript, health‑check, archive) that operate on a user‑provided knowledge base to ensure world‑building consistency, narrative pacing, and stylistic coherence. The skill enforces strict safety and quality gates and uses only read‑only tools (Read, Glob, Grep). | novel, collaborative, writing, ai, content-generation | zy-zmc/tianming-skill |

## Примечание

Каждый skill сохраняет метаданные происхождения в `metadata.json`. Проверяйте лицензию и исходный репозиторий перед коммерческим или чувствительным использованием.

# Curated Agent Skills Library

Автоматически собранная и проверенная библиотека Agent Skills.

Последнее обновление: `2026-09-10T12:23:19+00:00`

Активных skills: **6**

## Категории

### automation

| Skill | Описание | Теги | Источник |
|---|---|---|---|
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

### programming

| Skill | Описание | Теги | Источник |
|---|---|---|---|
| [Repo Task Proof Loop](./skills/programming/repo-task-proof-loop-3324eff9/SKILL.md) | A repo‑local workflow that creates a structured task folder, installs project‑scoped Codex and Claude subagents, and manages a repeatable spec‑freeze → build → evidence → verify → fix loop. It updates AGENTS.md and the repository’s Claude guide with managed workflow blocks and provides a set of CLI commands to drive each phase. The skill is designed for large coding tasks that require auditable proof of implementation. | repo, workflow, coding, automation, subagents | DenisSergeevitch/repo-task-proof-loop |

## Примечание

Каждый skill сохраняет метаданные происхождения в `metadata.json`. Проверяйте лицензию и исходный репозиторий перед коммерческим или чувствительным использованием.

# Curated Agent Skills Library

Автоматически собранная и проверенная библиотека Agent Skills.

Последнее обновление: `2026-09-09T12:29:52+00:00`

Активных skills: **3**

## Категории

### content-creation

| Skill | Описание | Теги | Источник |
|---|---|---|---|
| [Markit – Convert Files and URLs to Markdown](./skills/content-creation/markit-convert-files-and-urls-to-markdown-fbf180c9/SKILL.md) | Markit is a Node‑based CLI and SDK that extracts the textual content of many document types (PDF, DOCX, PPTX, HTML, etc.) and returns it as clean Markdown. It can process local files, remote URLs, and GitHub resources, offering raw markdown or JSON output. The skill includes usage examples for both the command line and TypeScript SDK. | content_creation, markdown, cli, sdk, nodejs, file_conversion | shift-labs-ai/markit |

### devops

| Skill | Описание | Теги | Источник |
|---|---|---|---|
| [Total Recall – Autonomous Agent Memory Skill](./skills/devops/total-recall-autonomous-agent-memory-skill-096b202d/SKILL.md) | Total Recall is an autonomous memory skill for OpenClaw agents that observes conversation logs, compresses them with LLMs, and maintains a prioritized observations file without external databases. It includes a multi‑layer architecture with cron‑based observer, reflector consolidation, session recovery, Linux inotify watcher, and an optional nightly Dream Cycle for deeper archiving. | memory, agent, devops, automation, linux, llm | gavdalf/total-recall |

### programming

| Skill | Описание | Теги | Источник |
|---|---|---|---|
| [Repo Task Proof Loop](./skills/programming/repo-task-proof-loop-3324eff9/SKILL.md) | A repo‑local workflow that creates a structured task folder, installs project‑scoped Codex and Claude subagents, and manages a repeatable spec‑freeze → build → evidence → verify → fix loop. It updates AGENTS.md and the repository’s Claude guide with managed workflow blocks and provides a set of CLI commands to drive each phase. The skill is designed for large coding tasks that require auditable proof of implementation. | repo, workflow, coding, automation, subagents | DenisSergeevitch/repo-task-proof-loop |

## Примечание

Каждый skill сохраняет метаданные происхождения в `metadata.json`. Проверяйте лицензию и исходный репозиторий перед коммерческим или чувствительным использованием.

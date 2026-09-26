---
name: "dify-master"
description: "Comprehensive modular skill system for Dify workflow and plugin development"
---

# Dify Master Skill

> A modular, progressive skill system for Dify development.

## Quick Navigation
- [What is Dify](#what-is-dify)
- [Skill Overview](#skill-overview)
- [Getting Started](#getting-started)
- [Sub‑Skill Index](#sub-skill-index)
- [Common References](#common-references)

---

## What is Dify

Dify is an open‑source LLMOps platform that provides visual workflow orchestration and a powerful plugin system, enabling developers to quickly build and deploy AI applications.

### Core Features
- **Visual Workflows** – Drag‑and‑drop orchestration without writing code.
- **Plugin System** – Extend with tools, models, data sources, etc.
- **Production‑Ready** – From local development to large‑scale distributed deployment.
- **Open Ecosystem** – 114K+ GitHub stars, active community, plugin marketplace.

### Architecture Highlights
- **Beehive Architecture** – Modular and extensible.
- **Queue‑Driven Graph Engine** – Event‑driven, parallel execution, high performance.
- **Multiple Runtimes** – Local, Debug, Serverless.
- **MCP Protocol** – Standard integration with assistants like Claude.

---

## Skill Overview

The **dify‑master** skill is organized into six core sub‑skills, covering the full development‑to‑deployment lifecycle.

```
 dify‑master (entry point)
 ├── 01‑workflow      # Workflow design
 ├── 02‑plugin        # Plugin development
 ├── 03‑performance   # Performance tuning
 ├── 04‑security      # Security & deployment
 ├── 05‑integration   # Integration & extensions
 └── 06‑reference     # Reference material
```

### Design Principles
1. **Modular** – Each sub‑skill is self‑contained and can be used independently.
2. **Progressive Disclosure** – Start with an overview, then dive deeper as needed.
3. **Context‑Optimized** – Loads only the necessary content for a given query.
4. **Practical** – Provides ready‑to‑use code snippets and configuration examples.

---

## Getting Started

### Scenario 1: Create a Simple Q&A Workflow
```yaml
workflow:
  graph:
    nodes:
    - data:
        type: start
        variables: []
      id: start
    - data:
        type: llm
        model:
          provider: openai
          name: gpt-4
        prompt_template:
        - role: system
          text: "You are an assistant"
        - role: user
          text: "{{#sys.query#}}"
      id: llm
    - data:
        type: answer
        answer: "{{#llm.text#}}"
      id: answer
    edges:
    - source: start
      target: llm
    - source: llm
      target: answer
```
**Next**: Explore the [01‑workflow sub‑skill](./01-workflow/SKILL.md) for more node types and patterns.

### Scenario 2: Build a Simple Tool Plugin
```python
from typing import Any, Generator
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin import Tool

class MyTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        input_text = tool_parameters.get("text", "")
        result = input_text.upper()
        yield self.create_text_message(result)
```
**Next**: Dive into the [02‑plugin sub‑skill](./02-plugin/SKILL.md) for a full development workflow.

### Scenario 3: Boost Workflow Performance with Parallel Branches
```yaml
- data:
    type: parallel
    branches:
    - nodes: [tool1, process1]
    - nodes: [tool2, process2]
    - nodes: [tool3, process3]
  id: parallel_execution
```
**Next**: Review the [03‑performance sub‑skill](./03-performance/SKILL.md) for additional optimization techniques.

---

## Sub‑Skill Index

### 01. Workflow Design
- **Triggers**: `node`, `LLM`, `Agent`, `workflow`, `variable`, `knowledge retrieval`, `HTTP Request`, `code`, `if‑else`, `iteration`, `template`, `DSL`, `YAML`
- **Content**: 10+ node types, 5 design patterns, templates, variable system, best practices.
- **Link**: [01‑workflow/SKILL.md](./01-workflow/SKILL.md)

### 02. Plugin Development
- **Triggers**: `plugin`, `tool`, `provider`, `manifest`, `OAuth`, `datasource`, `model`, `extension`
- **Content**: 4 plugin types, full dev‑to‑publish pipeline, project scaffolding, testing tips.
- **Link**: [02‑plugin/SKILL.md](./02-plugin/SKILL.md)

### 03. Performance Optimization
- **Triggers**: `performance`, `cache`, `parallel`, `latency`, `throughput`, `monitor`, `benchmark`
- **Content**: Workflow graph tuning, LLM prompt & model selection, async plugin execution, monitoring tools.
- **Link**: [03‑performance/SKILL.md](./03-performance/SKILL.md)

### 04. Security & Deployment
- **Triggers**: `security`, `deploy`, `Docker`, `Kubernetes`, `SSL`, `auth`, `sandbox`, `SSRF`
- **Content**: SSRF protection, sandboxing, encryption, auth, Docker/K8s deployment guides, HA, logging, backup.
- **Link**: [04‑security/SKILL.md](./04-security/SKILL.md)

### 05. Integration & Extensions
- **Triggers**: `integration`, `API`, `Webhook`, `MCP`, `database`, `Redis`, `RabbitMQ`, `Kafka`, `S3`
- **Content**: REST/Webhook/Streaming APIs, MCP client/server, external services, troubleshooting.
- **Link**: [05‑integration/SKILL.md](./05-integration/SKILL.md)

### 06. Reference Material
- **Triggers**: `reference`, `API`, `SDK`, `CLI`, `DSL`, `YAML`, `documentation`
- **Content**: Full DSL spec, REST API docs, Python SDK classes, CLI commands, FAQs, community links.
- **Link**: [06‑reference/SKILL.md](./06-reference/SKILL.md)

---

## Common References

### Variable Syntax
```yaml
{{#sys.query#}}          # User query
{{#sys.files#}}          # Uploaded files
{{#sys.conversation_id#}}# Conversation ID
{{#nodeID.output#}}      # Node output
{{#llm.text#}}           # LLM text output
{{#conversation.var#}}   # Conversation‑level variable
{{#item#}}               # Current iteration item
{{#index#}}              # Current index
```

### Typical Node Configurations
```yaml
# LLM node
- data:
    type: llm
    model:
      provider: openai
      name: gpt-4
      completion_params:
        temperature: 0.7
        max_tokens: 2000
    prompt_template:
    - role: system
      text: "System prompt"
    - role: user
      text: "{{#sys.query#}}"
    context:
      enabled: true
      variable_selector: ["knowledge", "result"]
```

### Plugin Manifest Example
```yaml
version: 0.0.1
type: plugin
author: your-name
name: plugin-name
label:
  en_US: Plugin Name
  zh_Hans: 插件名称
description:
  en_US: Plugin description
  zh_Hans: 插件描述
icon: icon.svg
resource:
  memory: 268435456  # 256MB
plugins:
  tools:
    - provider/provider.yaml
meta:
  version: 0.0.1
  arch: [amd64, arm64]
  runner:
    language: python
    version: "3.12"
    entrypoint: main
tags:
  - utilities
```

### CLI Quick Commands
```bash
# Plugin workflow
dify plugin init          # Scaffold a plugin project
dify plugin run           # Local debugging
dify plugin package       # Package the plugin
dify plugin publish       # Publish to marketplace

# Workflow management
dify workflow export <id>   # Export a workflow
dify workflow import <file> # Import a workflow
dify workflow validate <file> # Validate syntax

# Environment handling
dify env list               # List env vars
dify env set <key> <value>  # Set a variable
```

---

## Learning Paths

### Beginner (0‑1 week)
1. Read this skill to get the big picture.
2. Complete the **01‑workflow** basics.
3. Create your first workflow using the provided template.
4. Test and iterate on the Dify UI.

### Intermediate (1‑4 weeks)
1. Deep‑dive into workflow design patterns.
2. Build a custom tool plugin (02‑plugin).
3. Apply performance tweaks (03‑performance).
4. Deploy a small project.

### Expert (1‑3 months)
1. Master all sub‑skills.
2. Implement production‑grade security & deployment (04‑security).
3. Integrate external services (05‑integration).
4. Contribute back to the community.

---

## Getting Help

- **Official Docs**: https://docs.dify.ai/
- **GitHub**: https://github.com/langgenius/dify
- **Plugin Marketplace**: https://marketplace.dify.ai/
- **Discord**: https://discord.gg/FngNHpbcY7
- **Reddit**: https://reddit.com/r/difyai
- **Chinese Community**: https://github.com/langgenius/dify/discussions

---

## Version Info
- **Current Version**: v1.1.0
- **Last Updated**: 2026-03-05
- **Supported Dify Versions**: 0.15.x – 1.9.x
- **Next Release**: v1.2.0 (more templates & case studies)

---

## License

MIT License – free to use, modify, and distribute.

---

*Start your Dify development journey now – pick a sub‑skill or jump straight into a template!*

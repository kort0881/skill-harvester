---
name: "deepswarm"
description: "Use when running parallel AI workers for any long‑running or multi‑turn batch API task. Auto‑calculates optimal workers and stagger, supports tiered delegation."
---

# DeepSwarm — Task‑Agnostic Parallel Worker Orchestration

Spawn N parallel API workers for **any** long‑running or multi‑turn batch task. Auto‑calculates optimal worker count and stagger delay. Supports tiered model delegation: orchestrator plans with a frontier model (V4 Pro), workers execute with a cheaper model (V4 Flash).

## Overview
DeepSwarm 2.0 generalizes the proven orchestration pattern from the 19,331‑trace generation project to any batch API task. Define a task — translations, reasoning traces, code reviews, summarization — and DeepSwarm parallelizes it across optimal workers with the right stagger for your API.

**Core insight:** API rate limits are a function of simultaneous connections, not total volume. Auto‑calculated stagger + worker count = ≈99.95 % success.

## When to Use
- Any batch API task: generation, translation, summarization, extraction, classification
- Long‑running individual calls (30 s +) that benefit from parallelization
- Multi‑turn tasks where each worker loops through conversation turns
- Cost optimisation via tiered delegation (orchestrator ≠ worker model)
- Crash‑resilient batch processing (checkpointed, idempotent)

**Don’t use for:**
- Quick calls under 10 s (overhead outweighs benefit)
- Tasks requiring inter‑worker coordination (use `delegate_task`)
- Real‑time interactive sessions (use tmux‑agent‑orchestrator)

## Quick Start
```bash
# Install
hermes skills tap add amanning3390/deepswarm

# Define your task (task.yaml)
python3 scripts/seed.py --task task.yaml

# Launch — auto‑optimises workers, stagger, model routing
python3 scripts/swarm.py --task task.yaml --total 1000

# Filter — repair JSON, validate structure, apply length thresholds
python3 scripts/filter.py --input-dir output/ --output clean.jsonl --errors errors.jsonl
```

## Task Definition (task.yaml)
```yaml
task_type: generation              # generation | translation | summarization | custom
prompt_template: |
  You are an AI assistant. {{seed}}

orchestrator_model: deepseek-v4-pro  # Plans, monitors, handles errors
worker_model: deepseek-v4-flash      # Executes batches (cheaper!)
worker_api_base: https://api.deepseek.com/v1/chat/completions
worker_max_tokens: 4096

multi_turn: true                    # Workers loop through conversation turns
max_turns: 20                       # Max turns per worker conversation
seeds_file: seeds.jsonl             # Pre‑generated task seeds

workers: auto                       # auto | N
stagger: auto                       # auto | seconds
batch_size: auto                    # auto | tasks per worker

output_dir: output/
output_format: jsonl               # jsonl | json | parquet
checkpoint_every: 10               # Save progress every N tasks

worker_script: custom_worker.py     # Override default worker behaviour (optional)
```

## Tiered Model Delegation
```
User Task → V4 Pro (plans, monitors)
  ├─ V4 Flash Worker 0 → API → output/
  ├─ V4 Flash Worker 1 → API → output/
  └─ …
```
*Why it matters:* V4 Pro costs ≈3× V4 Flash per token; using the cheap model for the bulk of calls saves 60‑70 % cost.

## Auto‑Optimization
When `workers: auto` and `stagger: auto`:
1. Run a calibration call to measure call duration.
2. Compute optimal workers: `min(8, floor(rate_limit / call_duration))`.
3. Set stagger: `call_duration / workers × 2`.
4. Adjust batch size: `total / workers`.

### Calibration Table
| Call Duration | Workers | Stagger | Success | Throughput |
|---------------|---------|---------|---------|------------|
| <10 s | 16 | 1 s | 99.9 % | ~5,760 /hr |
| 10‑30 s | 12 | 2 s | 99.9 % | ~1,440 /hr |
| 30‑60 s | 8 | 5 s | 99.95 % | ~440 /hr |
| 60‑90 s | 6 | 10 s | 99.9 % | ~240 /hr |
| >90 s | 4 | 15 s | 99.9 % | ~96 /hr |

## Multi‑Turn Task Support
```python
for seed in seeds:
    messages = [system_prompt, user_task]
    for turn in range(config["max_turns"]):
        response = api_call(messages, model=config["worker_model"])
        messages.append({"role": "assistant", "content": response})
        if task_complete(response):
            break
        if needs_tool_call(response):
            messages.append(simulate_tool_response(response))
```

## Worker Design (worker.py)
```python
def run_task(seed, config):
    messages = build_messages(seed, config)
    for turn in range(config["max_turns"]):
        response = call_api(messages, config)
        if is_complete(response, config):
            return finish(response, messages)
        if needs_continuation(response, config):
            messages = append_turn(messages, response, config)
    return messages
```
Supported `task_type`s: `generation`, `translation`, `summarization`, `classification`, `custom`.

## Common Pitfalls
1. `workers: auto` may pick too many; override manually if calibration is unrepresentative.
2. Forgetting to stagger can trigger rate limits.
3. Mixing models without checking format compatibility.
4. Not checkpointing – loss of work on worker crash.
5. Using shell `&` without `wait` – child processes may be killed early.
6. Using V4 Pro for workers when V4 Flash suffices – test quality first.
7. Not cleaning error outputs before restart – they consume disk.

## Verification Checklist
- [ ] Task YAML has valid model names and API base URL
- [ ] API key exported for both orchestrator and worker models
- [ ] `workers: auto` or manual count ≤ 8 per batch
- [ ] `stagger: auto` or manual ≥ `call_duration / workers × 2`
- [ ] Worker model tested on a 5‑sample run before full batch
- [ ] Output directory exists and is writable
- [ ] Seeds file exists with correct format
- [ ] Checkpointing enabled for runs > 100 tasks
- [ ] Orchestrator model is V4 Pro (or equivalent frontier) for planning
- [ ] Worker model is V4 Flash (or cheapest model that handles the task)

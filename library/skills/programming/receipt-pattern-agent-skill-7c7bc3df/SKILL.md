---
name: "receipt-pattern"
description: "Standardized logging of side-effect actions performed by an agent, producing JSON receipts for audit and rollback tracking."
---

# Receipt Pattern — Agent Skill

## Purpose
Create a JSON receipt after every session that performed side‑effect actions (file writes, API mutations, database changes, etc.). The receipt provides an immutable audit trail and helps determine rollback possibilities.

## When to Write a Receipt
Write a receipt when the session includes **any** of the following:
- File writes, deletions, or renames  
- Mutating API calls (`POST`, `PUT`, `DELETE`, `PATCH`)  
- Database writes or schema migrations  
- Sending emails, messages, or notifications  
- Deployments or infrastructure changes  
- Shell commands that have side effects

Do **not** write receipts for read‑only operations such as file reads, `GET` requests, or linting.

## Receipt Location
```
receipts/YYYY-MM-DD-HH-MM-SS-[action-type].json
```
Example: `receipts/2026-03-05-14-35-22-file-write.json`
Create the `receipts/` directory if it does not exist.

## Receipt Schema
```json
{
  "id": "rcpt_<unix_timestamp>_<6_char_hex>",
  "agentId": "<your agent name>",
  "sessionId": "<session identifier>",
  "timestamp": "<ISO 8601>",
  "trigger": "manual | scheduled | webhook",
  "status": "completed | failed | partial | rolled_back",
  "durationMs": 0,
  "actions": [
    {
      "sequence": 1,
      "type": "file:write | file:delete | api:call | db:write | email:send | deploy | shell:exec",
      "target": "<file path, URL, table name, etc.>",
      "summary": "<plain English description>",
      "status": "success | failed | anomaly",
      "isRollbackEligible": true,
      "durationMs": 0,
      "timestamp": "<ISO 8601>"
    }
  ],
  "anomalies": [
    {
      "actionSequence": 1,
      "detail": "<unexpected condition>"
    }
  ],
  "rollbackAvailable": false,
  "sdkVersion": "receipt-pattern/1.0.0"
}
```

## Rules
1. **Sequence matters** – number actions in the order they occurred.
2. **Summaries are plain English** – e.g., “Wrote 142 lines to `src/index.ts`”.
3. **Mark anomalies** – add unexpected events to `anomalies[]`.
4. **Rollback eligibility** – `true` for file operations that can be restored from version control; `false` for sent emails, API calls, deployments.
5. `rollbackAvailable` is `true` only if **all** actions are rollback‑eligible.
6. Write the receipt as the **last** action of the session.

## Session Start Check
```bash
ls receipts/ 2>/dev/null | tail -5
```
Read the most recent receipt to understand the previous session’s state.

## TypeScript Helper
```typescript
import { writeFileSync, mkdirSync, existsSync } from 'fs';

interface ReceiptAction {
  sequence: number;
  type: string;
  target: string;
  summary: string;
  status: 'success' | 'failed' | 'anomaly';
  isRollbackEligible: boolean;
  durationMs: number;
  timestamp: string;
}

interface Receipt {
  id: string;
  agentId: string;
  sessionId: string;
  timestamp: string;
  trigger: string;
  status: 'completed' | 'failed' | 'partial' | 'rolled_back';
  durationMs: number;
  actions: ReceiptAction[];
  anomalies: { actionSequence: number; detail: string }[];
  rollbackAvailable: boolean;
  sdkVersion: string;
}

export function writeReceipt(receipt: Receipt): void {
  if (!existsSync('receipts')) mkdirSync('receipts', { recursive: true });
  const ts = new Date().toISOString().replace(/[T:]/g, '-').replace(/\..+/, '');
  const mainType = receipt.actions[0]?.type.replace(':', '-') ?? 'unknown';
  const path = `receipts/${ts}-${mainType}.json`;
  writeFileSync(path, JSON.stringify(receipt, null, 2));
}
```

## Python Helper
```python
import json, os, time, secrets
from datetime import datetime, timezone

def write_receipt(receipt: dict) -> str:
    os.makedirs("receipts", exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H-%M-%S")
    main_type = receipt["actions"][0]["type"].replace(":", "-") if receipt["actions"] else "unknown"
    path = f"receipts/{ts}-{main_type}.json"
    with open(path, "w") as f:
        json.dump(receipt, f, indent=2)
    return path

def make_receipt_id() -> str:
    return f"rcpt_{int(time.time())}_{secrets.token_hex(3)}"
```

## Completion Signal
Before ending any session that performed significant actions:
1. Assemble all actions into a receipt object.
2. Call the helper (`writeReceipt` or `write_receipt`).
3. Mention the receipt file path in the final message.

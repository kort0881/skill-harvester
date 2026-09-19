---
name: "japan-gyousei-data"
description: "Access Japanese government open data (real‑estate transaction prices, procurement bids, e‑Stat statistics) via the MCP server (mcp.n-3.ai). Provides CLI wrappers for three public data sources."
---

# Japanese Government Open Data Skill

This skill enables retrieval of three Japanese government open‑data sets through the MCP server (`mcp.n-3.ai`). It wraps the underlying tools with a single shell helper.

## Data Sources

| # | Name | Purpose | Tools |
|---|------|---------|-------|
| 1 | Real‑estate transaction price | Ministry of Land, Infrastructure, Transport and Tourism (MLIT) actual transaction data | `reinfolib-real-estate-price`, `reinfolib-city-list` |
| 2 | Procurement (官公需) | Search government and municipal procurement notices | `kkj-search` |
| 3 | e‑Stat | Access the Government Statistics Portal | `e-stat-get-stats-list`, `e-stat-get-meta-info`, `e-stat-get-data-catalog` |

## Invocation

Use the provided `scripts/mcp-call.sh` wrapper. The script expects three arguments:
1. **data_source** – one of `reinfo`, `kkj`, or `estat`.
2. **tool_name** – the specific tool to call (see table above).
3. **arguments_json** – a JSON string with the tool‑specific parameters.

```bash
bash <skill_dir>/scripts/mcp-call.sh <data_source> <tool_name> '<arguments_json>'
```

### Example Commands

```bash
# Real‑estate: Osaka city transaction prices for Q3 2025
bash scripts/mcp-call.sh reinfo reinfolib-real-estate-price '{"year":"2025","quarter":"3","area":"27","city":"27102"}'

# Real‑estate: List municipalities in prefecture 27 (Osaka)
bash scripts/mcp-call.sh reinfo reinfolib-city-list '{"area":"27"}'

# Procurement: Search AI‑related bids (category 3 = services)
bash scripts/mcp-call.sh kkj kkj-search '{"query":"AI 人工知能","category":"3"}'

# e‑Stat: Find statistics containing the word "人口"
bash scripts/mcp-call.sh estat e-stat-get-stats-list '{"searchWord":"人口"}'
```

## Tool Details

For full parameter specifications, refer to `references/tools.md` in the repository.

## Important Notes

- **Procurement regional filter**: `kkj-search` does not accept a prefecture parameter; include location keywords in the query string.
- **Procurement detail data**: MCP returns only the search‑result list. For specifications, amounts, and deadlines, visit the original portal.
- **Real‑estate codes**: Prefecture codes are two‑digit numbers (e.g., Tokyo = 13, Osaka = 27). City codes can be obtained via `reinfolib-city-list`.
- **e‑Stat workflow**: First call `e-stat-get-stats-list` to obtain a statistic ID, then `e-stat-get-meta-info` for metadata, and finally `e-stat-get-data-catalog` to download the data.
- **Rate limits**: These are public APIs; use them at a reasonable frequency to avoid throttling.

---

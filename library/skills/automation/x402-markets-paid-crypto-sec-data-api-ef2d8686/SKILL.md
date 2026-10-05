---
name: "x402-markets"
description: "Paid API service providing live cryptocurrency price data via CoinGecko and recent SEC EDGAR filings, using the x402 payment protocol."
---

# x402-markets — agent skill

Two market‑data lookups, each returning its answer in the paid response.
- `/price/{coinId}` – live CoinGecko snapshot: spot price, 1h/24h/7d change, 24h high‑low range, volume, market cap, circulating and max supply, distance from all‑time high/low.
- `/filings/{ticker}` – resolves a US ticker to its SEC CIK and returns recent EDGAR filings with form type, dates, document link, decoded 8‑K items, and a one‑sentence summary.

**Base URL:** `{BASE_URL}` (default `http://localhost:4023`).
All paid calls return the purchased artifact in the `200` response body.

## Payment

The service uses **x402** (HTTP 402 Payment Required – <https://x402.org>). Pay in USDC on Base (EVM) or Solana; the client chooses the rail.

| Rail | Network | Asset | payTo |
|------|---------|-------|------|
| EVM | `base-sepolia` (`base` on mainnet) | USDC | `0x40252CFDF8B20Ed757D61ff157719F33Ec332402` |
| Solana | `solana` (`solana-devnet` on devnet) | USDC | `WwwuGbqHrwF5RG89KhUbmRWEvjnRH9k5kVM5p7T3WwW` |

Facilitator: `https://x402.org/facilitator` (verifies and settles both rails).

**Flow**
1. Call the endpoint without an `X-PAYMENT` header → receive **402** with an `accepts` array listing both rails.
2. Choose a rail, sign the payment, and place the base64 payload in `X-PAYMENT`.
3. Repeat the request → receive **200** with the artifact and a settlement receipt in `X-PAYMENT-RESPONSE` (base64 JSON `{ success, rail, network, transaction, payer, amount, asset }`).

Example (Node/TS) using the EVM helper library:
```ts
import { wrapFetchWithPayment, createSigner } from "x402-fetch";
const signer = await createSigner("base-sepolia", process.env.PRIVATE_KEY!);
const pay = wrapFetchWithPayment(fetch, signer);
const res = await pay("{BASE_URL}/price/bitcoin");
const artifact = await res.json();
```

## Endpoints

### `GET /price/:coinId` — $0.001
Live crypto spot price and 24h statistics.
| Param | In | Required | Type | Description |
|-------|----|----------|------|-------------|
| `coinId` | path | yes | string | CoinGecko coin id (`bitcoin`, `usd-coin`, …) or ticker shorthand (`btc`, `eth`). |
| `vs` | query | no | string | Quote currency, default `usd`. |

**Response (200 application/json)** – see example in original skill.

---

### `GET /filings/:ticker` — $0.003
Recent SEC EDGAR filings for a US‑listed ticker.
| Param | In | Required | Type | Description |
|-------|----|----------|------|-------------|
| `ticker` | path | yes | string | US ticker symbol (e.g., `AAPL`). |
| `limit` | query | no | integer | Number of filings to return (1‑100), default 20. |
| `forms` | query | no | string | Comma‑separated form types to filter (e.g., `10-K,8-K`). |

**Response (200 application/json)** – see example in original skill.

## Free endpoints
- `GET /` – service metadata, live prices, active payment rails, upstream list
- `GET /health` – liveness probe
- `GET /.well-known/x402` – machine‑readable discovery manifest
- `GET /skill.md` – this skill card
- `GET /openapi.json` – OpenAPI 3.1 spec

## Error codes
| HTTP | `error` | Meaning |
|------|---------|---------|
| 400 | `invalid_coin_id` | `coinId` not plausible for CoinGecko |
| 400 | `invalid_currency` | `vs` not a supported currency |
| 400 | `invalid_limit` | `limit` outside 1‑100 |
| 404 | `not_found` | No such coin or SEC registrant |
| 503 | `upstream_rate_limited` | Upstream rate‑limited; includes `Retry-After` |
| 502 | `upstream_error` | Upstream failed or timed out |
| 402 | — | Payment required or rejected; body contains `accepts` and optional `error` |
| 500 | `no_payment_rail_configured` | Server mis‑configured payment rails |

## Data sources
- **CoinGecko public API** – free, keyless, rate‑limited (~5‑15 calls/min per IP).
- **SEC EDGAR API** – free, keyless; must set a `User-Agent` with contact email (`CONTACT_EMAIL`).

The ticker→CIK map (~1 MB) is cached in memory for 24 h; all other data is fetched live.

## Discovery
- Manifest: `GET /.well-known/x402` (also on GitHub).
- Indexed by x402scan.com, x402 Bazaar, and agentic.market.
- OpenAPI spec: `openapi.json`.

## Contact
nichxbt@gmail.com · <https://github.com/nirholas/x402-markets>

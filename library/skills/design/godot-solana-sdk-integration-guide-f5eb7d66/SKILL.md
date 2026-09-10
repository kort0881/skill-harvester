---
name: "godot-solana-sdk"
description: "Use this skill when building Solana-enabled games or apps in Godot 4 with the Godot Solana SDK."
---

# Godot Solana SDK

A GDExtension (C++) plugin for Godot 4 that brings full Solana blockchain support to game development. Write GDScript to send transactions, manage wallets, mint NFTs, and interact with Anchor programs — on Windows, Linux, macOS, Web, Android, and iOS.

- **Repo:** https://github.com/Virus-Axel/godot-solana-sdk
- **Docs:** https://zenwiki.gitbook.io/solana-godot-sdk-docs
- **Demo:** https://zenrepublic.github.io/GodotSolanaSDKDemos/
- **Asset Library:** https://godotengine.org/asset-library/asset/3232
- **Discord:** https://discord.gg/9aFDCvqPgt

> **Security:** Mainnet use is not yet security‑audited. Crypto can be stolen. Use with care.

## Installation

**Via Godot Asset Library (recommended)**
1. Search for **"Solana"** in the Godot Asset Library and install.
2. Installation must go into the `addons/` folder at the project root.
3. Open **Project → Project Settings → Plugins** and enable **SolanaSDK**.
4. Verify **`SolanaService`** appears under **Project Settings → Autoload**.

**Via GitHub Releases (manual)**
Download binaries from the Releases page, place them under `res://bin/`, and reload the project.

## Configuration

After enabling the plugin, `SolanaService` is automatically added as an autoload singleton.

- **RPC cluster:** Select Mainnet or Devnet in the SolanaService inspector. Provide a custom RPC URL (e.g., from Helius) for better performance. The URL is also read from `Project Settings → solana_sdk/client/default_url`.
- **Wallet:** The `WalletService` child node handles auth.
  - *Use Generated* — deterministic wallet seeded from your machine ID (testing only).
  - *Custom Wallet* — path to a JSON file with the private key as a 64‑byte array.

## Core Nodes

| Node | Inherits | Purpose |
|---|---|---|
| `SolanaClient` | `Node` | Low‑level RPC calls to the Solana network |
| `Transaction` | `SolanaClient` | Build, sign, and send transactions |
| `WalletAdapter` | `Node` | Browser / mobile wallet integration |
| `Account` | `Node` | Mirror of an on‑chain account, auto‑syncs |
| `AccountFetcher` | `SolanaClient` | Bulk‑fetch a list of Account nodes |
| `SystemProgram` | `Node` | SOL transfers and account creation |
| `TokenProgram` | `Node` | SPL Token instructions |
| `AssociatedTokenAccountProgram` | `Node` | Create Associated Token Accounts |
| `ComputeBudget` | `Node` | Set compute unit limits and priority fees |
| `MplCandyMachine` | `Node` | Candy Machine v3 minting |
| `MplCandyGuard` | `Node` | Candy Guard configuration |
| `MplTokenMetadata` | `Node` | Metaplex token metadata |
| `AnchorProgram` | `Node` | Generic interface for any Anchor program |
| `SolanaUtils` | `Node` | Base58/Base64 encoding, hashing utilities |

## Core Resources

| Resource | Purpose |
|---|---|
| `Pubkey` | 32‑byte Solana public key / address |
| `Keypair` | ed25519 keypair for signing |
| `Instruction` | A single transaction instruction |
| `AccountMeta` | Account metadata entry in an instruction |
| `CandyMachineData` | Candy Machine configuration |

## Pubkey
```gdscript
var pk: Pubkey = Pubkey.new_from_string("78GVwUb8ojcJVrEVkwCU5tfUKTfJuiazRrysGwgjqsif")
var pk_bytes: Pubkey = Pubkey.new_from_bytes(some_packed_byte_array)
var program_key := Pubkey.new_from_string("CndyV3LdqHUfDLmE5naZjVN8rBZz4tqhdefbAnjHG3JR")
var pda: Pubkey = Pubkey.new_pda(["Level1"], program_key)
var pda_bytes: Pubkey = Pubkey.new_pda_bytes([some_pubkey.to_bytes()], program_key)
var ata: Pubkey = Pubkey.new_associated_token_address(owner, mint, TokenProgram.get_pid())
var random_pk: Pubkey = Pubkey.new_random()
print(pk.to_string())
print(pk.to_bytes())
```
> `Pubkey.new_pda` searches for a valid bump; `new_program_address` does not.

## Keypair
```gdscript
var kp: Keypair = Keypair.new_random()
var seed = PackedByteArray(); seed.resize(32)
var kp_seed: Keypair = Keypair.new_from_seed(seed)
var kp_phantom: Keypair = Keypair.new_from_bytes("3wUbDHMtMVQ...")
var kp_file: Keypair = Keypair.new_from_file("res://payer.json")
kp.save_to_file("keypair.json")
print(kp.get_public_string())
print(kp.get_private_bytes())
var sig = kp.sign_message("hello".to_ascii_buffer())
var ok = kp.verify_signature(sig, "hello".to_ascii_buffer())
```

## SolanaClient (RPC)
```gdscript
var client: SolanaClient = SolanaClient.new()
add_child(client)
client.set_url_override("https://api.devnet.solana.com")
client.set_commitment("confirmed")
client.get_account_info("4sGjMW1sUnHzSxGspuhpqLDx6wiyjNtZAMdL4VZHirAn")
var response: Dictionary = (await client.http_request_completed)[1]
if response.has("result"):
    print(response["result"])
remove_child(client)
client.queue_free()
```
*All RPC methods emit `http_request_completed`; listen to the signal for results.*

## Transaction
```gdscript
var payer: Keypair = Keypair.new_from_file("res://payer.json")
var receiver: Pubkey = Pubkey.new_from_string("78GVwUb8ojcJVrEVkwCU5tfUKTfJuiazRrysGwgjqsif")
var tx = Transaction.new()
add_child(tx)
tx.set_payer(payer)
tx.add_instruction(SystemProgram.transfer(payer, receiver, 500_000))
tx.update_latest_blockhash()
tx.sign_and_send()
var resp = await tx.transaction_response_received
if resp.has("result"):
    print("Signature:", resp["result"])
await tx.confirmed
await tx.finalized
```

## SystemProgram, TokenProgram, AssociatedTokenAccountProgram, ComputeBudget, WalletAdapter, AnchorProgram, MplCandyMachine, SolanaUtils, SolanaService
*Sections omitted for brevity – the original skill contains full GDScript examples for each.*

## Error Handling
```gdscript
var params = await client.http_request_completed
var error: Error = params[0]
var response: Dictionary = params[1]
if error != OK:
    push_error("Connection error: %d" % error)
    return
if response.is_empty() or response.has("error"):
    push_error("RPC error: " + str(response.get("error", {}).get("message", "unknown")))
    return
var result = response["result"]
```

## Common Pitfalls
- `SolanaClient` must be added to the scene tree before making requests.
- Use `TokenProgram.transfer_checked` instead of `transfer`.
- Derive ATAs with `Pubkey.new_associated_token_address`.
- After `Transaction.new_from_bytes`, re‑assign signers before signing.
- Load Anchor IDL via the inspector, not from code.
- `Pubkey.new_pda` can return `null`; always check.
- `WalletAdapter` is primarily for web exports; use `Keypair` for desktop.

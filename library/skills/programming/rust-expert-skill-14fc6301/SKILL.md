---
name: "rust-skill"
description: "Comprehensive Rust programming expert skill system covering ownership, lifetimes, async/await, FFI, performance, web development, embedded systems, and more, with routing to specialized sub‑skills."
---

# Rust Expert Skill

## Description
You are an expert Rust programmer with deep knowledge of:
- Memory safety, ownership, borrowing, and lifetimes
- Modern Rust patterns (2021‑2024 editions)
- Systems programming, concurrency, and unsafe Rust
- Error handling, testing, and best practices

### When to use this skill
- Rust compilation errors and type‑system issues
- Ownership, borrowing, and lifetime questions
- Async/await and concurrency patterns
- Performance optimization and benchmarking
- FFI and systems programming
- Web development with Rust
- Embedded and `no_std` environments
- Testing, database, observability infrastructure

## Instructions
### Code Analysis
1. Identify ownership and borrowing patterns
2. Check for lifetime issues and potential leaks
3. Evaluate error handling strategy
4. Assess concurrency safety (`Send`/`Sync` bounds)
5. Review API ergonomics and idiomatic usage

### Problem Solving
1. Start with safe, idiomatic solutions
2. Use `unsafe` only when absolutely necessary and justified
3. Prefer the type system over runtime checks
4. Leverage community crates where appropriate
5. Consider performance implications of abstractions

### Best Practices
- Use `Result` and `Option` throughout the codebase
- Implement `std::error::Error` for custom error types
- Write comprehensive tests (unit + integration)
- Document public APIs with `rustdoc`
- Run `cargo clippy` and `cargo fmt` for code quality

#### Error Handling Example
```rust
// Propagate errors with ? operator
fn process_data(input: &str) -> Result<Data, MyError> {
    let parsed = input.parse()?;
    let validated = validate(parsed)?;
    Ok(validated)
}

// Use thiserror for custom error types
#[derive(thiserror::Error, Debug)]
pub enum MyError {
    #[error("validation failed: {0}")]
    Validation(String),
    #[error("io error: {0}")]
    Io(#[from] std::io::Error),
}
```

### Memory Safety Patterns
- Stack‑allocate small, `Copy` types
- Use `Box<T>` for heap allocation and trait objects
- `Rc<T>` / `Arc<T>` for shared ownership
- `Vec<T>` for dynamic collections
- References with explicit lifetimes when needed

### Concurrency Safety
- Use `Send` for data that can cross thread boundaries
- Use `Sync` for data that can be shared safely
- Prefer `Mutex`/`RwLock` for mutable shared state
- Use channels for message passing
- Consider `tokio` or `async‑std` for async I/O

### Cargo Workflow
```bash
# Create new binary/library
cargo new --bin project_name
cargo new --lib library_name

# Add dependencies
cargo add crate_name
cargo add --dev dev_dependency

# Check, test, and build
cargo check          # Fast type checking
cargo build --release  # Optimized build
cargo test --lib     # Library tests
cargo test --doc     # Doc tests
cargo clippy         # Lint warnings
cargo fmt            # Format code
```

## Constraints
### Always Do
- ✅ Run `cargo check` before suggesting fixes
- ✅ Include relevant `Cargo.toml` dependencies
- ✅ Provide complete, compilable code examples
- ✅ Explain the rationale behind each pattern
- ✅ Show how to test the solution
- ✅ Consider backward compatibility and MSRV when specified

### Never Do
- ❌ Suggest `unsafe` without clear justification
- ❌ Use `String` where `&str` suffices
- ❌ Add unnecessary `clone()` calls
- ❌ Ignore `Result` or `Option` values
- ❌ Introduce panics in library code

## Tools (scripts/ directory)
- `scripts/compile.sh` – runs `cargo check --message-format=short`
- `scripts/test.sh` – runs `cargo test --lib --doc --message-format=short`
- `scripts/clippy.sh` – runs `cargo clippy -- -D warnings`
- `scripts/fmt.sh` – runs `cargo fmt --check`

## References (references/ directory)
- Core concepts: ownership, lifetimes, concurrency
- Best practices: API design, error handling, unsafe rules
- Ecosystem: recommended crates, modern crates (2024‑2025), testing strategies
- Versions: Rust 2021/2024 edition features
- Commands: code review, unsafe check, skill index

## Sub‑Skills (35 total)
### Core Skills
| Skill | Description | Triggers |
|-------|-------------|----------|
| **rust-skill** | Main Rust expert entry point | rust, cargo, compile error |
| **rust-ownership** | Ownership & lifetime | ownership, borrow, lifetime |
| **rust-mutability** | Interior mutability | mut, Cell, RefCell, borrow |
| **rust-concurrency** | Concurrency & async | thread, async, tokio |
| **rust-error** | Error handling | Result, Error, panic |
| **rust-error-advanced** | Advanced error handling | thiserror, anyhow, context |
| **rust-coding** | Coding standards | style, naming, clippy |

### Advanced Skills
| Skill | Description | Triggers |
|-------|-------------|----------|
| **rust-unsafe** | Unsafe code & FFI | unsafe, FFI, raw pointer |
| **rust-anti-pattern** | Anti‑patterns | anti-pattern, clone, unwrap |
| **rust-performance** | Performance optimization | performance, benchmark, false sharing |
| **rust-web** | Web development | web, axum, HTTP, API |
| **rust-learner** | Learning & ecosystem | version, new feature |
| **rust-ecosystem** | Crate selection | crate, library, framework |
| **rust-cache** | Redis caching | cache, redis, TTL |
| **rust-auth** | JWT & API Key auth | auth, jwt, token, api-key |
| **rust-middleware** | Middleware patterns | middleware, cors, rate-limit |
| **rust-xacml** | Policy engine | xacml, policy, rbac, permission |

### Expert Skills
| Skill | Description | Triggers |
|-------|-------------|----------|
| **rust-ffi** | Cross‑language interop | FFI, C, C++, bindgen, C++ exception |
| **rust-pin** | Pin & self‑referential | Pin, Unpin, self-referential |
| **rust-macro** | Macros & proc‑macro | macro, derive, proc-macro |
| **rust-async** | Async patterns | Stream, backpressure, select |
| **rust-async-pattern** | Advanced async | tokio::spawn, plugin |
| **rust-const** | Const generics | const, generics, compile-time |
| **rust-embedded** | Embedded & no_std | no_std, embedded, ISR, WASM, RISC‑V |
| **rust-lifetime-complex** | Complex lifetimes | HRTB, GAT, 'static, dyn trait |
| **rust-skill-index** | Skill index | skill, index, 技能列表 |
| **rust-linear-type** | Linear types & resource mgmt | Destructible, RAII, linear semantics |
| **rust-coroutine** | Coroutines & green threads | generator, suspend/resume, coroutine |
| **rust-ebpf** | eBPF & kernel programming | eBPF, kernel module, map, tail call |
| **rust-gpu** | GPU memory & computing | CUDA, GPU memory, compute shader |

## Problem‑Based Lookup
| Problem Type | Skills to Use |
|--------------|---------------|
| Compile errors (ownership/lifetime) | rust-ownership, rust-lifetime-complex |
| Borrow checker conflicts | rust-mutability |
| Send/Sync issues | rust-concurrency |
| Performance bottlenecks | rust-performance |
| Async code issues | rust-concurrency, rust-async, rust-async-pattern |
| Unsafe code review | rust-unsafe |
| FFI & C++ interop | rust-ffi |
| Embedded/no_std | rust-embedded |
| eBPF kernel programming | rust-ebpf |
| GPU computing | rust-gpu |
| Advanced type system | rust-lifetime-complex, rust-macro, rust-const |
| Coding standards | rust-coding |
| Caching strategies | rust-cache |
| Authentication/Authorization | rust-auth, rust-xacml |
| Web middleware | rust-middleware, rust-web |

## Skill Collaboration Diagram
```
rust-skill (main entry)
    │
    ├─► rust-ownership ──► rust-mutability ──► rust-concurrency ──► rust-async
    │         │                     │                     │
    │         └─► rust-unsafe ──────┘                     │
    │                   │                              │
    │                   └─► rust-ffi ─────────────────────► rust-ebpf
    │                             │                         │
    │                             └────────────────────────► rust-gpu
    │
    ├─► rust-error ──► rust-error-advanced ──► rust-anti-pattern
    │
    ├─► rust-coding ──► rust-performance
    │
    ├─► rust-web ──► rust-middleware ──► rust-auth ──► rust-xacml
    │                              │
    │                              └─► rust-cache
    │
    └─► rust-learner ──► rust-ecosystem / rust-embedded
              │
              └─► rust-pin / rust-macro / rust-const
                        │
                        └─► rust-lifetime-complex / rust-async-pattern
                                  │
                                  └─► rust-coroutine
```

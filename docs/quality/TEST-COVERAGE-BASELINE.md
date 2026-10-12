# Test and coverage baseline — 2026-10-12

## Immutable reference

- Fork: `Rwanbt/lightcraft`, base branch: `main`.
- Initial base commit: `0ba118de92a81f7463ca0e6d79e1323137b1adae`.
- QA working branch: `test/quality-baseline-20261012`.
- Internal draft PR: https://github.com/Rwanbt/lightcraft/pull/1
- Source of initial inventory: recursive GitHub tree of the initial base commit; **not** `cargo test -- --list`.

## Discovered inventory (not runtime validation)

- 27 application/crate `Cargo.toml` files in `apps/*` and `crates/*`, plus `xtask` — 28 workspace member locations defined by the globs in the root manifest.
- 107 Rust files whose names/paths contain test conventions in the initial GitHub tree. **This is a file count, not a test count**, and excludes many in-module tests.
- Three applications: desktop `apps/lightcraft`, CLI `apps/lightcraft-cli`, WebAssembly `apps/lightcraft-web`.
- Initially four GitHub workflows: FreeBSD, Packaging lint, Release, Windows ARM64.
- At discovery time this fork reported **zero Actions runs**; workflows elsewhere and README claims are not evidence of a green fork.
- Product's own `docs/gaps.md` ranks missing native-platform automated tests as a beta blocker (#9).
- Desktop, CLI, MCP and native rendering surfaces are present; existence is not proof of passing E2E scenarios.

## Instrumented coverage baseline

| Measurement | Verified baseline |
|---|---|
| Workspace lines | NOT MEASURED |
| Workspace branches/functions | NOT MEASURED |
| Color crate lines | NOT MEASURED |
| Functional E2E coverage | NOT MEASURED |
| Actual test cases discovered | NOT COLLECTED |
| Excluded code | NONE AUTHORIZED |

Do not infer percentage coverage from source file counts. No minimum coverage threshold has been installed until a reliable baseline is available. Keep all production code under observation; explain any future exclusions before applying them.

## Reproducible checks

The draft PR adds `.github/workflows/quality.yml`. It performs:
- Linux: `cargo xtask ci` (format, Clippy, HEIF, workspace tests, parity, architecture, attribution, WASM).
- Windows and macOS: `cargo test --workspace --locked`.
- On each PR: `cargo llvm-cov -p lightcraft-color --lib --locked --lcov --output-path coverage/color.lcov`.
- Manual or weekly: `cargo llvm-cov --workspace --locked --lcov --output-path coverage/workspace.lcov`.
- LCOV is uploaded as a downloadable artifact when produced.

The exact workflow run SHA and results must be read from GitHub Actions. A pending, failed, skipped or missing job is **not passed**. Comparing successive coverage reports requires matching toolchain, feature set and platform.

## Environment limitations

The initiating container had no `rustc` and could not resolve `github.com`; direct local cargo execution was unavailable. GitHub Actions is the test runner. No real test count or coverage percentage is asserted here before successful collection.

## Exit gate

Keep the PR in draft until the exact HEAD SHA is checked, all applicable required jobs pass, coverage artifacts are inspected, and remaining native UI and external-corpus requirements are either verified or explicitly blocked. This is a **first baseline tranche**, not a production-ready declaration.

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

## First measured color result (historical SHA)

GitHub Actions run [38267686177](https://github.com/Rwanbt/lightcraft/actions/runs/38267686177), head `ddb45eb391adb667c5e0ca09ce2a89bbb60eaaa4`; job *Linux / instrumented color contracts* **succeeded**. This is a **historical run**, not the eventual latest PR HEAD.

- Rust toolchain in runner: `rustc 1.99.0`.
- Test runner: `22 passed, 0 failed` for `lightcraft-color --lib`.
- Color lines: **520 / 558 = 93.19%**.
- Color functions: **97 / 107 = 90.65%**.
- Branch coverage: **not collected** (LCOV has no branch totals).
- Download: [color.lcov](https://github.com/Rwanbt/lightcraft/actions/runs/38267686177/artifacts/11756095348).
- Missing lines on that commit: `lib.rs` 16; `perceptual.rs` 8; `spline.rs` 7; `transfer.rs` 6; `cct.rs` 0. Subsequent PR commits add contract tests for these gaps; their effect is **not measured yet**.
- The Linux, Windows and macOS full-suite job conclusions on this historical run were not completed and the run was later cancelled when new commits arrived. They must **not** be marked passed.

## Cross-platform test baseline and CI defects (historical SHA)

The completed [run 38268740650](https://github.com/Rwanbt/lightcraft/actions/runs/38268740650)
was executed on `39ec7d1326283411ad985d8ff26c32b53cc87ea7`.

- Linux `cargo xtask ci`: **success**; its `cargo test --workspace` stage reported
  **2,574 passed, 0 failed, 26 ignored** across **83 test-binary reports**
  (log-parsed values, not a source file count).
- macOS full workspace tests: **success**.
- Windows workspace tests: **seven failures** in `tests_sync`; all seven compare
  mixed `/\` fixture paths against native Windows scanner paths. The scratch
  path builder now joins components using the host separator, with a regression test.
- Full workspace LLVM instrumentation: failed after **653 engine tests passed**
  because the former full-size preview cancellation test timed out while
  processing the first rendering job. The test now verifies command-to-flag wiring
  deterministically, with separate worker cancellation tests. The production worker
  also checks cancellation between the thumbnail and view renders. **Coverage
  from this run was not collected** because the test runner exited unsuccessfully.

A later [color job on run 38273549385](https://github.com/Rwanbt/lightcraft/actions/runs/38273549385)
executed **30 tests, 0 failures**, with **649/649 instrumented lines and
116/116 instrumented functions (100% each)** for `lightcraft-color`.
It is a historical measurement; it does not validate subsequent HEAD commits
or imply branch coverage. All changes after that measurement require a fresh CI run.

## Reproducible checks

The draft PR adds `.github/workflows/quality.yml`. It performs:
- Linux: `cargo xtask ci` (format, Clippy, HEIF, workspace tests, parity, architecture, attribution, WASM).
- Windows and macOS: `cargo test --workspace --locked`.
- On each PR: `cargo llvm-cov -p lightcraft-color --lib --locked --lcov --output-path coverage/color.lcov`.
- Dedicated `test/quality-baseline-*` PR branches, manual runs, or weekly: `cargo llvm-cov --workspace --locked --lcov --output-path coverage/workspace.lcov`.
- LCOV is uploaded as a downloadable artifact when produced.

The exact workflow run SHA and results must be read from GitHub Actions. A pending, failed, skipped or missing job is **not passed**. Comparing successive coverage reports requires matching toolchain, feature set and platform.

## Environment limitations

The initiating container had no `rustc` and could not resolve `github.com`; direct local cargo execution was unavailable. GitHub Actions is the test runner. No real test count or coverage percentage is asserted here before successful collection.

## Exit gate

Keep the PR in draft until the exact HEAD SHA is checked, all applicable required jobs pass, coverage artifacts are inspected, and remaining native UI and external-corpus requirements are either verified or explicitly blocked. This is a **first baseline tranche**, not a production-ready declaration.

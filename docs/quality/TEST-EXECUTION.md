# Reproducing ArtCraft fork-quality checks

All work is done on `Rwanbt/lightcraft`, not `storytold/lightcraft`. The PR is draft and must not be merged automatically.

## Local native Linux prerequisites

Use a Rust toolchain supporting edition 2024 and the root manifest's MSRV (1.90); install `rustfmt`, `clippy`, and `wasm32-unknown-unknown`. The Linux apt dependencies are described in `.github/workflows/quality.yml`.

From the root directory:

```sh
git rev-parse HEAD
cargo fmt --all -- --check
cargo xtask ci
cargo test --workspace --locked
cargo test -p lightcraft-color --lib --locked non_finite_curve_inputs_do_not_panic_or_propagate_nan
```

The project's full quality gate is `cargo xtask ci`. Avoid substituting a lone `cargo check` for functional tests.

## Instrumented measurement

```sh
rustup component add llvm-tools-preview
cargo install cargo-llvm-cov --locked
mkdir -p coverage
cargo llvm-cov -p lightcraft-color --lib --locked --lcov --output-path coverage/color.lcov
cargo llvm-cov --workspace --locked --lcov --output-path coverage/workspace.lcov
```

Use separate reports for platforms and mutually exclusive features. CI uploads reports for inspection. Do not set a 100% threshold before reviewing reachable code, uncovered branches, and any documented justified exclusions.

## Native and UI E2E

The project's own `AGENTS.md` directs agents to use **its control channel**, not generic desktop keystroke/click automation. Headless UI screenshots can be made with `lightcraft-cli snapshot --demo --script tour.jsonl -o out.png --size 1600x1000`. UI E2E must exercise a real application/binary, import a procedural asset, edit, undo/redo, save, reopen and verify the final exported file. Record test data, expected outputs and SHA before marking a scenario VERIFIED.

## CI acceptance

1. Open the Actions run for the precise branch commit (not a previous commit).
2. Read all job conclusions. A skipped weekly/full workspace coverage job is not a success.
3. Collect `color.lcov` and `workspace.lcov` from the appropriate job artifacts.
4. Report actual test totals from the runner, failures, flaky reruns and relevant skipped scenarios.
5. Leave the fork's PR in **draft** unless every applicable test is green and residual risk is documented.

There is no demonstrated local cargo execution in the initiating environment; results must come from GitHub Actions.

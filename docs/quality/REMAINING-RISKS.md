# Residual risk register — initial audit 2026-10-12

Baseline: `main` `0ba118de92a81f7463ca0e6d79e1323137b1adae`. PR: https://github.com/Rwanbt/lightcraft/pull/1 (draft).

| Priority | Risk | Evidence / condition | Next evidence |
|---|---|---|---|
| P0 | Regression of user's photo library or non-destructive edits | Catalog/import/export handle original photographs and persistent metadata | Actual interrupted-write, corrupted-input and restart E2E |
| P0 | Native-platform test gates missing on initial fork | `docs/gaps.md` #9; before this PR only FreeBSD ran normal workspace tests | Execute and inspect Linux, Windows, macOS jobs on PR SHA |
| P0 | Runtime crash from malformed/invalid inputs | `MonotoneCurve::eval(NaN)` could index beyond the last point, `-Inf` returned NaN; corrected in this PR pending CI proof | Verify newly added regression and fuzz other media/command boundaries |
| P1 | Camera formats and visual fidelity not verified against independent oracles | `docs/gaps.md` #1–#3, #6, #10; insufficient sampled camera variants | Pinned corpus, chart/camera validation and render golden comparisons |
| P1 | Native/wasm full end-to-end user journeys unproven | Unit test existence does not prove startup, dialogs, save/reopen or export | Run controlled real-app E2E and collect screenshots/files |
| P1 | Whole-workspace measured coverage unavailable | No instrumented baseline existed at initial discovery | Run manual/weekly workspace LLVM coverage, inspect missing files and branches |
| P1 | Heavy GPU/AI models and optional features | Tests may skip unavailable accelerators/weights | Tagged environment-aware deterministic GPU/CPU and disabled-feature checks |
| P1 | Cross-platform builds and installers | Build/packaging and runtime smoke differ from comprehensive E2E | Check native builds, package install/uninstall and logs |

**Status:** PARTIALLY VERIFIED (structural inspection only). No claim of production readiness or 100% coverage is valid until run-based proof is collected. Do not remove failing tests or reduce coverage thresholds to obtain green checks.

## Discovered during first CI execution

- **Windows test-fixture path bug:** seven `tests_sync` test failures resulted from
  mixed separators in expected strings. Fixed in the shared `Scratch::path`
  helper with a platform-native path assertion, awaiting full Windows CI rerun.
- **Preview cancellation latency:** full-resolution rendering could take longer
  than the old cancellation test's one-minute deadline. The worker now checks
  cancellation between the thumbnail and view render jobs. A single running
  decode/render is **not instantly interruptible**; deeper cancellation support
  through the pipeline remains a documented residual limitation.
- **Coverage overhead and test non-determinism:** the first instrumented workspace
  run failed on preview timing and yielded no LCOV artifact; new deterministic
  tests avoid using wall-clock time as proof of cancellation. Rerun required.
- **Untested/sometimes ignored behaviors:** 26 ignored cases appeared in the
  historical Linux workspace run. Identify and justify these before claiming
  full functional verification; counts may change between commits.

Current PR remains **DRAFT**. Historical successes are not proof of current HEAD.

# Initial feature-to-test traceability

Initial code-level map for `Rwanbt/lightcraft` at base `0ba118de92a81f7463ca0e6d79e1323137b1adae` (2026-10-12).

**Status semantics:** VERIFIED means an applicable test was executed for the exact commit and its assertions verify the contract. PARTIAL means a necessary class of checks is missing. UNVERIFIED means no qualifying run has been evaluated. BLOCKED means essential dependencies are unavailable. The table must be updated from artifacts, not from test filenames alone.

| ID | Area / implementation | Expected contract and critical risks | Evidence in source | Required validation | State |
|---|---|---|---|---|---|
| LC-QA-001 | Photo catalog: `crates/catalog`, `crates/engine/src/library.rs` | Atomic edits, locking, restart/recovery, prevent data loss | `crates/catalog/src/tests_journal.rs`, `tests_torn_append.rs`, `tests_lock.rs` | Repeatable crash/reopen tests and native E2E | UNVERIFIED |
| LC-QA-002 | RAW/TIFF: `crates/raw`, `crates/tiff` | Reject truncated/malformed media without panic; exact decode bounds | `crates/raw/tests/robust.rs`, `vendor_robust.rs`; TIFF roundtrip | Corpus + fuzz replay + optional formats | UNVERIFIED |
| LC-QA-003 | Standard codecs: `crates/codecs` | Header detection, decode/encode, no corruption | `crates/codecs/tests/header.rs`, `roundtrip.rs`, `fuzz.rs` | Instrumented format and malformed input checks | UNVERIFIED |
| LC-QA-004 | Color science: `crates/color` | Accurate matrices/transfer, monotone curve, no crash on invalid float | Inline tests `transfer.rs`, `spline.rs` | Oracle roundtrips, NaN/Inf regression, instrumented coverage | UNVERIFIED |
| LC-QA-005 | Non-destructive development: `crates/develop`, `crates/pipeline` | Deterministic rendering, stable settings and undo/redo | `tests_process.rs`, `crates/pipeline/src/tests.rs` | Numerical oracles, cross-resolution equivalence | UNVERIFIED |
| LC-QA-006 | Import and filesystem: `crates/engine/src/import.rs`, `files.rs` | Never overwrite originals, protect file integrity | `tests_import.rs`, `tests_import_move.rs` | Import + cancellation + disk failure + restart E2E | UNVERIFIED |
| LC-QA-007 | Export/media: `crates/engine/src/export.rs` | Valid dimensions, metadata, file roundtrip | `tests_export.rs` | CLI output checksum, format oracles, E2E | UNVERIFIED |
| LC-QA-008 | Masking/AI/denoise: `crates/segment`, `crates/denoise` | Deterministic fallback, no unapproved remote costs | `crates/segment/tests/reference.rs`, `crates/denoise/tests/real_model.rs` | Model fixtures, GPU/CPU, controlled remote tests | UNVERIFIED |
| LC-QA-009 | Desktop UI: `crates/ui-egui`, `apps/lightcraft` | Menu, selection, save, compare, undo/redo | `crates/ui-egui/src/tests_*.rs` | Native headless control-channel UI scripts and screenshots | UNVERIFIED |
| LC-QA-010 | CLI: `apps/lightcraft-cli` | Real process and exit status, import/render/export | `apps/lightcraft-cli/tests/cli.rs` | Run binary with procedural data, assert outputs | UNVERIFIED |
| LC-QA-011 | MCP/control: `crates/mcp`, desktop control server | Structured commands, bad input errors, isolation | `crates/mcp/tests/e2e.rs` | Live protocol E2E and malformed request suite | UNVERIFIED |
| LC-QA-012 | Browser/WebAssembly: `apps/lightcraft-web` | Web startup, worker messages, backup/recovery | `apps/lightcraft-web/src`, `worker.js` | Compile WASM, real browser E2E and responsive tests | UNVERIFIED |

Tests are **present in files**, but their harness-reported counts and per-feature adequacy are not yet known. This matrix is an inventory awaiting proof, not a sign-off.

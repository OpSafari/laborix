# laborix

`laborix` is a **fully offline** orchestrator for autonomous experiment
pipelines, in the spirit of Agent-Laboratory-style research automation. It
implements and verifies the **mechanics** of automated research programs —
versioned plan schemas, dependency-safe deterministic execution, tamper-evident
provenance ledgers, budget-respecting scheduling under uncertainty, ablation
bookkeeping, and report synthesis — rather than the creativity of any
particular language model.

At runtime the package depends only on NumPy. PyTorch (CPU-only) is an optional
extra powering the trainable surrogate-scheduling demos. Every default test and
example runs without network access; "experiment steps" in the demos execute
real NumPy computations on synthetic data.

## Installation

```bash
python -m venv .venv
.venv/bin/pip install -e ".[dev]"          # development env (hatchling, pytest, ruff, mypy)
.venv/bin/pip install -e ".[dev,torch]" \
    --extra-index-url https://download.pytorch.org/whl/cpu   # for surrogate-scheduling demos
```

## Quick start

```bash
.venv/bin/laborix demo demo-output
```

The demo executes a complete synthetic research program offline — plan →
schedule → run → ablate → report — and prints measured regret against the
oracle, ablation coverage, and the artifact ledger summary (for example
`{"coverage": {"method": true, "seed": true}, "regret": 4.5, "runs": 24,
"synthetic": true}`). Everything it produces is reproducible from the printed
seeds and config hashes.

## CLI

The `laborix` command-line tool provides one subcommand per lifecycle stage:

| Subcommand | Purpose |
| --- | --- |
| `validate` | Statically validate a research plan: schema version, dependency DAG (cycle detection, dangling refs), typed step inputs/outputs, resource annotations — with precise error messages |
| `plan` | Emit example/templated research plans in the versioned JSON schema |
| `run` | Execute a plan deterministically: topological step order, bounded parallelism with ordering guarantees, retries with jitter and attempt ceilings, timeouts, cancellation with clean partial-state semantics |
| `resume` | Resume a crashed or cancelled run from the ledger — completed steps replay from recorded artifacts instead of recomputing; final artifacts are byte-identical to a straight run |
| `schedule` | Run the bandit-based experiment scheduler (UCB1 / Thompson sampling) over candidate configurations under budget constraints, reporting cumulative regret vs. the oracle |
| `ablate` | Generate and execute an ablation matrix from a factor grid with coverage checks (every factor varied while others are fixed at least once) and missing-cell detection |
| `ledger` | Inspect and verify the append-only provenance ledger, including the chained-hash tamper-evidence check |
| `verify` | Re-verify recorded artifact hashes and ledger integrity for a run directory |
| `report` | Synthesize a Markdown/self-contained-HTML research report from ledger + result tables, with paired comparisons, deterministic bootstrap CIs, embedded reproducibility metadata, and a limitations section generated from actual coverage/budget facts |
| `demo` | The full offline end-to-end demonstration described above |

Exit codes are documented in [docs/exit-codes.md](docs/exit-codes.md).

## Common commands

| Command | Purpose |
| --- | --- |
| `make build` | Build a wheel with the local venv (`--no-isolation`) |
| `make test` | Fast test suite (excludes the `slow` mark) |
| `make test-all` | Full suite including slow integration tests |
| `make format` / `make format-check` | ruff formatting and its check mode |
| `make lint` | ruff check + format --check |
| `make typecheck` | mypy static analysis |

## What is guaranteed (and tested)

The test suite (837 fast tests plus 4 slow integration tests) pins the
properties that make an automated pipeline trustworthy:

- **Executor determinism** — the same plan and seeds produce byte-identical
  artifacts across runs and across run directories.
- **Crash recovery** — a real subprocess is killed mid-run; resuming from the
  ledger completes to artifacts byte-identical to an uninterrupted run.
- **Tamper-evident ledger** — every step attempt records input hash, code
  version, config hash, seed, output hash, wall time, and status; the chained
  hash verification detects any edited or reordered entry.
- **Budget safety** — the scheduler never exceeds run/wall-clock budgets, and
  cumulative regret is sublinear on stationary synthetic surfaces.
- **Schema discipline** — plan/artifact schemas round-trip exactly, reject
  unknown keys and wrong versions, and golden files make any drift deliberate.
- **Ablation completeness** — generated grids carry a witness for every factor
  variation; incomplete coverage is reported honestly instead of silently
  dropped.

## Package layout

`ablation` · `adapters` · `artifacts` · `cli` · `clock` · `demo` · `errors` ·
`executor` · `http_adapter` · `ledger` · `mappings` · `metrics` · `plan` ·
`plan_queries` · `records` · `report` · `scheduler` · `schema` · `sequences` ·
`surrogate` (torch extra) · `svg` · `transforms` — with `py.typed` and full
type hints throughout.

## Examples and documentation

`examples/` contains three fully offline, runnable examples, each with its own
README and captured output:

- `checkpoint_resume` — plan validation, deterministic execution, and a
  simulated crash followed by resume-to-identical-artifacts.
- `bandit_regret` — UCB1/Thompson scheduling against a synthetic oracle with a
  regret curve emitted as dependency-free SVG.
- `mini_program` — a complete miniature research program producing an HTML
  report from real executed computations.

Documentation lives under `docs/`: [architecture](docs/architecture.md),
[artifacts](docs/artifacts.md) and [artifact layout](docs/artifact-layout.md),
[canonical JSON](docs/canonical-json.md), [configuration](docs/configuration.md),
[adapters](docs/adapters.md), [ablation](docs/ablation.md), the
[API reference](docs/api.md), a [glossary](docs/glossary.md), and per-command
references (`demo-command.md`, `ablate-command.md`, `exit-codes.md`, …).

## License

MIT — see [LICENSE](LICENSE). Release history is in [CHANGELOG.md](CHANGELOG.md).

# CLAUDE.md

Independent replication and extension of **ConstraintBench** (Tso et al., Haladir Research, [arXiv:2602.22465](https://arxiv.org/abs/2602.22465)). The paper asks whether LLMs can solve constrained optimization problems *directly*, answering in JSON without writing solver code, and finds that feasibility, not optimality, is the bottleneck. We rebuild the benchmark, check whether its findings hold, improve the method, then extend it. Roadmap, status and decision log: `PLAN.md`.

## How to work in this repo

- **Plan before building.** For anything beyond a small fix, propose the approach and agree on it with the user before writing code. The user is learning research methodology, so briefly explain the *why* behind design choices.
- **Ask before spending money.** Any command that calls a paid LLM API beyond a single smoke-test call needs the user's OK first, with an estimated cost (calls × model × expected tokens).
- **Reuse, don't reinvent.** Prefer established tools (Gurobi, Pydantic, provider SDKs) over custom code. What we must write ourselves: the problem generators and the checkers.
- Keep `PLAN.md` current: tick milestones as they finish and add decisions to its log when they're made.

## Research rules

These keep results reproducible. Don't break them without the user's agreement.

1. **Prompts are versioned and frozen once used.** Every prompt sent to a model lives in `prompts/<id>/<version>.md` (see `prompts/README.md`). Never edit a prompt with `status: frozen`; copy it to a new version instead.
2. **Log every model call**: prompt id, version and sha256, model, all settings, raw response, token usage, cost, timestamp. Never overwrite or delete results; new runs go in new files.
3. **Checkers are independent of the Gurobi models.** A checker validates an answer constraint by constraint and recomputes the objective from the raw decision values. Never trust an LLM's self-reported objective, and never reuse Gurobi model code inside a checker.
4. **Every difference from the paper goes in `docs/deviations.md`**, with the reason.
5. **Fixed seeds** for everything random (problem generation, sampling).
6. **Use the paper's metrics.** Feasible = zero violations. Optimal = feasible and within 0.1% of the Gurobi objective. Joint "% optimal" divides by all tasks, and errors and parse failures count as infeasible.

## Commands

```bash
uv sync                               # install dependencies
uv run pytest                         # run tests
uv run python scripts/check_env.py    # check Python, packages, Gurobi, API keys
uv add <package>                      # add a dependency (never pip install)
```

## Layout

- `src/cbench/`: Python package. `prompts.py` loads and renders versioned prompts.
- `prompts/`: versioned prompt templates.
- `tests/`: pytest tests.
- `scripts/`: runnable entry points.
- `docs/`: notes and `deviations.md`.
- `papers/`: local PDFs of the papers we read. Gitignored; fetch with `scripts/download_papers.sh`.

Create these only when a milestone needs them:
- `src/cbench/domains/<domain>/`: generator, Gurobi model, Pydantic answer schema and checker for each domain.
- `data/`: generated problems.
- `results/`: run logs.

## Conventions

- Python 3.12, managed with `uv`. Use type hints, and a Pydantic model for every answer schema.
- Keep code simple and readable. This is research code that others should be able to audit.
- Secrets live in `.env` (gitignored). Never commit API keys or print them.
- The PyPI `gurobipy` comes with a size-limited license (about 2,000 variables and 2,000 constraints). Keep problems within it, or flag when a larger license is needed.

# Reproducibility evidence

These files support the measurements and planner results reported in the PDF. They are not additional PDDL problem submissions: the submission still contains exactly the five required `.pddl` files under `PDDL/`.

## Sudoku

The `sudoku/benchmarks/` directory contains the 13 fixed inputs and `manifest.csv`. The recorded experiment used Python 3.11.9 on macOS 15.7.7 ARM64, one excluded warm-up and five measured runs per puzzle/strategy, with a one-second limit per run.

- `raw_runs.csv`: all 234 warm-up and measured records.
- `summary_by_puzzle.csv`: medians and deterministic search counts used in the report.
- `environment.json`: runtime, platform, timeout, selection rule, and metric definitions.
- `benchmark_console.log`: complete console output from the verified run.
- `h4_extended.json` and `h4_extended_console.log`: one 30-second-cap follow-up per strategy. All three solved H4 and produced the same solution hash.
- `failure_cases.json`: invalid-input and no-solution checks.

`forward_checks` counts calls to the forward-checking function. `peer_checks` counts unassigned peer domains actually evaluated inside those calls.

## PDDL

Pyperplan 2.1 was run with A* and the additive heuristic:

```bash
pyperplan -H hadd -s astar 'PDDL/PartA&B/domain.pddl' 'PDDL/PartA&B/mission1.pddl'
pyperplan -H hadd -s astar 'PDDL/PartA&B/domain.pddl' 'PDDL/PartA&B/mission2.pddl'
pyperplan -H hadd -s astar PDDL/PartC/domain-ext.pddl PDDL/PartC/mission3.pddl
```

The saved runs produced plans of 10, 21 and 26 actions and expanded 11, 85 and 178 nodes. The logs note that the external VAL executable was unavailable. `plan_replay.log` records a separate replay through Pyperplan's grounded operators: every action precondition held and all 3/3, 6/6 and 6/6 goals were reached.

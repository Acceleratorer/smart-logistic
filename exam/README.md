# Exam protocol

Use this protocol for each AGV simulation run.

- Record notebook version, source commit, robot count, grid size, safety parameters, seed or dispatch order, and dataset identifier.
- Run TN01–TN07 with the same input order when comparing controller variants.
- Store pass/fail per scenario. A pass requires task completion, no static-obstacle route, valid state transitions, and no rejected step that corrupts state.
- Repeat each comparison at least 10 times before reporting a mean or percentage improvement.

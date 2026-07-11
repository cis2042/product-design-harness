# Implementation Agent Adapter

Use this adapter before any implementation session.

An implementation agent receives product judgment only after the review returns
continue.

## Input Order

1. Canonical review result
2. Context pack
3. Execution task
4. Verification requirements

## Required Handoff

| Field | Required content |
|---|---|
| Goal | Product outcome, not only artifact change. |
| Scope | What execution may change. |
| Non-goals | What execution must not change. |
| User rule | What the actor must understand or achieve. |
| Evidence rule | What behavior or outcome must become measurable. |
| Business rule | What value, cost, retention, or distribution rule matters. |
| Acceptance criteria | Observable completion state. |
| Stop conditions | When execution returns to product judgment. |
| Human approval gates | Decisions that must not be delegated. |

## Guardrails

| Risk | Guardrail |
|---|---|
| Overbuilding | Narrow scope and explicit non-goals. |
| Hidden assumptions | Include the riskiest claim and weakest flow. |
| Surface polish before proof | Require an evidence rule before refinement. |
| Scope drift | Stop when new product decisions appear. |
| False completion | Verify against acceptance criteria and stop conditions. |

If the verdict is verify, execute only the proof step.

If the verdict is stop_reframe, do not create implementation work.

# Council Facilitator

## Role

Turn verified disagreement into one product decision. Do not vote and do not
average.

## Preflight

Reject synthesis unless the council input contains:

- claim analysis with dependency edges
- three independent lane reviews
- three challenge-round reviews
- uncertainty review
- evidence provenance and freshness
- an accountable owner for any human-owned decision

## Decision Rule

| Lane state | Combined verdict |
|---|---|
| Any lane `stop_reframe`, for any reason | `stop_reframe` |
| One or more `verify` and no stop | `verify` |
| All three `continue` | `continue` |

Select the weakest flow deterministically: the lane with the most severe
verdict (`stop_reframe` > `verify` > `continue`); ties break to the lowest
lane `evidence_tier`, then to the fixed priority evidence, user, business.
The weakest flow defines the next action. Human judgment may raise the proof
bar, but it may not erase missing actor clarity, provenance, or safety.

## Contract

Input: `schemas/council-input.schema.json`

Output: `schemas/review-result.schema.json`

Only `continue` creates a context pack. `verify` creates one proof step.
`stop_reframe` creates one better product question.

# OpenCrawl Evidence Adapter

Use this adapter when product judgment depends on discovering, comparing, or
tracing evidence across sources.

This adapter keeps retrieval, interpretation, and verdict separate.

## Contract

Input: `schemas/evidence-request.schema.json`

Output: `schemas/evidence-response.schema.json`

Every receipt uses `schemas/evidence.schema.json` and includes:

- source identifier and raw artifact location
- signal type
- signal and interpretation
- decision impact
- evidence tier
- counter-signal
- collection and source-verification time
- maximum staleness

## Guardrails

| Risk | Guardrail |
|---|---|
| Search rank treated as truth | Return traceable receipts, not conclusions. |
| External evidence overrules user reality | User Flow remains an independent review. |
| Competitor copying | Business Flow checks value and differentiation. |
| Evidence overload | Retrieve only evidence tied to named claims. |
| Stale sources | Re-verify or downgrade expired receipts. |
| Crawl-to-build jump | Retrieval cannot return a product verdict. |

## Review Flow

1. Create a product brief and claim graph.
2. Request evidence for missing claims.
3. Validate evidence response and freshness.
4. Run Evidence Flow Reviewer.
5. Join User, Evidence, and Business reviews.
6. Create a context pack only after `continue`.

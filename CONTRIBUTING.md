# Contributing

UX3 is a community-built system for strategic product judgment. Most design
repositories improve a prototype, visual, or animation. This repository asks a
different question: what should be built, for whom, based on what evidence,
under which business conditions, and with which human accountable for the
trade-off?

Every contribution must improve decision quality. The repository is not a
link collection, trend archive, or showcase gallery.

## Ways To Contribute

| Track | Contribution | Required proof |
|---|---|---|
| Field evidence | A real decision, intervention, and observed outcome. | Context, all three flows, counter-signal, human judgment, limitations, consent. |
| Decision rule | A reusable constraint for product judgment. | Repeated failure, trigger, evidence requirement, counter-signal, stop condition. |
| Pressure case | A scenario that exposes a weak rule or agent behavior. | Baseline failure and the expected bounded response. |
| Contract | Schema, validator, prompt, or template change. | Which invalid output it rejects or which handoff it makes checkable. |
| Integration | A new way to invoke UX3 in a product workflow. | Execution boundary, failure mode, and verified example. |
| Documentation | A clearer explanation or translation. | Canonical English source and no change to machine identifiers. |

## Field Evidence Contract

Field evidence is the preferred contribution. It must include:

1. Product stage and decision context.
2. The decision before UX3 or before the proposed rule was applied.
3. User Flow observation, including affected people and excluded groups.
4. Evidence Flow observation, including source, signal, interpretation,
   freshness, and at least one counter-signal.
5. Business Flow observation, including value exchange, cost, owner, and risk.
6. Designer-in-the-Loop judgment: owner, trade-off, rationale, and reversal
   condition.
7. The bounded action taken and the observed outcome.
8. Measurement window, limitations, consent, and redaction status.

Do not submit customer secrets, personal data, private interview recordings,
or claims that cannot be published. An anonymized case is welcome when its
decision logic remains inspectable.

An accepted evidence report is not automatically a canonical UX3 rule. It
first enters review, then may become a pressure case, example, rule change, or
documented counterexample.

## Contribution Workflow

1. Choose the Field Evidence, Decision Rule, or Bug issue form.
2. Fork or branch from the latest `main`.
3. Keep one strategic change per branch.
4. Open a Pull Request and complete the evidence, boundary, and validation
   sections.
5. Address review findings without deleting material counter-evidence.

No direct commits to main. Contributors use a Fork or branch and a Pull
Request. Sustained contributors may be invited into an Evidence Steward or
Maintainer role under `GOVERNANCE.md`.

## Required Mapping

Every contribution maps to at least one of:

- User Flow
- Evidence Flow
- Business Flow
- Human Judgment Gate
- UX3 Decision Kernel

Changes to a canonical flow, verdict, schema, evidence tier, weakest-flow rule,
or Human Judgment Gate require maintainer review and explicit migration notes.

## Avoid

- tool-specific promotion or vendor lock-in;
- generic trend summaries;
- surface critique without product judgment;
- prototype, visual, or animation work without decision impact;
- examples without observed outcome or stated limitation;
- prompts that produce plans without gates or stop conditions;
- synthetic evidence presented as field evidence;
- averaging away the weakest flow.

## Validate

Install `requirements-dev.txt`, then run:

- `python -m unittest discover -s tests -v`
- `python scripts/validate.py`
- `python scripts/check_review.py examples/quick-gate-review.json`

Use a short imperative commit subject. The Pull Request, not the commit count,
is the unit of community review.

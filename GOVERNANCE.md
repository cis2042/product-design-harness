# Governance

## Purpose

UX3 is open for community development while keeping one coherent strategic
judgment system. Participation is open; changes to Canonical UX3 remain
reviewed because a permissive collection of contradictory rules would make the
harness less useful to both people and agents.

## Roles

### Contributor

Anyone who submits field evidence, an issue, a review, documentation, a test,
or a Pull Request. Contributors do not need prior permission.

### Evidence Steward

A sustained contributor trusted to review evidence completeness, consent,
redaction, provenance, counter-signals, and overclaiming. An Evidence Steward
does not turn a case into a canonical rule alone.

### Maintainer

A person accountable for repository health, releases, security response, and
Canonical UX3 decisions. Maintainers merge Pull Requests, resolve governance
questions, and protect the contract shared by human and agent surfaces.

## Decision Rights

| Change | Decision path |
|---|---|
| Typo, broken link, or non-semantic cleanup | Maintainer review after tests. |
| Field evidence or case report | Evidence Steward review, then maintainer approval. |
| New prompt, template, adapter, or pressure case | Maintainer approval with an observed failure or explicit test contract. |
| Canonical UX3 flow, verdict, evidence tier, schema, weakest-flow rule, or Human Judgment Gate | Maintainer approval plus migration notes, contract tests, and evidence review. |
| License, governance, or security policy | Explicit repository-owner decision. |

The combined product judgment follows UX3: the weakest flow cannot be averaged
away. Popularity, vote count, polish, or contributor status cannot substitute
for missing evidence.

## Review Principles

- Separate source, signal, interpretation, counter-signal, and decision impact.
- Record uncertainty and limitations instead of upgrading confidence by prose.
- Preserve human accountability for taste, strategy, ethics, and risk.
- Prefer reversible trials before changing a canonical rule.
- Treat a rejected proposal as reusable evidence when its reasoning is sound.

## Conflict Of Interest

Contributors and reviewers disclose any conflict of interest, including vendor
affiliation, paid implementation, customer relationship, or ownership in a
product used as evidence. A conflicted reviewer may provide context but should
not be the sole approver.

## Access And Commits

No direct commits to `main`. Write access is earned through sustained,
constructive contributions and does not remove Pull Request review. Emergency
security fixes may use an expedited maintainer path and must be documented
after disclosure risk is contained.

## Disagreement

State the disputed claim, evidence, counter-signal, and reversible test in the
Issue or Pull Request. Maintainers publish the decision and rationale. A closed
proposal may be reopened when materially new evidence appears.

## License

Code and documentation remain available under the repository MIT License.
Contributors affirm that they have the right to submit their work under those
terms.

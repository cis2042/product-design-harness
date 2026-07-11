#!/usr/bin/env python3
"""Validate a review-result file against the canonical contract AND the
semantic rules that JSON Schema alone cannot fully express.

Usage: python scripts/check_review.py path/to/review.json
Exit 0 = valid; exit 1 = violations printed to stderr.
"""
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parent.parent
SEVERITY = {"stop_reframe": 2, "verify": 1, "continue": 0}
PRIORITY = {"evidence": 0, "user": 1, "business": 2}
VERDICTS = ["continue", "verify", "stop_reframe"]


def expected_weakest_flow(reviews):
    def sort_key(lane):
        review = reviews[lane]
        return (
            -SEVERITY[review["verdict"]],
            review["evidence_tier"],
            PRIORITY[lane],
        )

    return sorted(reviews, key=sort_key)[0]


def check(document):
    problems = []
    schema = json.loads(
        (ROOT / "schemas" / "review-result.schema.json").read_text()
    )
    resources = []
    for schema_name in ["session-config.schema.json", "actor-boundary.schema.json"]:
        external_schema = json.loads((ROOT / "schemas" / schema_name).read_text())
        resource = Resource.from_contents(external_schema)
        resources.extend(
            [
                (external_schema["$id"], resource),
                (schema_name, resource),
                (
                    f"https://productdesignharness.org/schemas/{schema_name}",
                    resource,
                ),
            ]
        )
    registry = Registry().with_resources(resources)
    for error in Draft202012Validator(schema, registry=registry).iter_errors(document):
        problems.append(f"schema: {error.json_path}: {error.message}")
    if problems:
        return problems

    reviews = document["reviews"]
    severities = [SEVERITY[lane["verdict"]] for lane in reviews.values()]
    expected_combined = VERDICTS[max(severities)]
    if document["combined_verdict"] != expected_combined:
        problems.append(
            "combined_verdict must equal the worst lane verdict: "
            f"expected {expected_combined}, got {document['combined_verdict']}"
        )

    expected_weakest = expected_weakest_flow(reviews)
    if document["weakest_flow"] != expected_weakest:
        problems.append(
            "weakest_flow must follow the deterministic selection: "
            f"expected {expected_weakest}, got {document['weakest_flow']}"
        )

    min_lane_tier = min(lane["evidence_tier"] for lane in reviews.values())
    if document["evidence_tier"] != min_lane_tier:
        problems.append(
            "headline evidence_tier must equal the lowest lane tier: "
            f"expected {min_lane_tier}, got {document['evidence_tier']}"
        )

    tier = document["evidence_tier"]
    verdict = document["combined_verdict"]
    if tier == "t0" and verdict != "stop_reframe":
        problems.append(
            "evidence tier t0 forces stop_reframe: internal belief with no "
            f"traceable source cannot authorize {verdict}"
        )
    if tier == "t1" and verdict == "continue":
        problems.append(
            "evidence tier t1 can never return continue: stated opinion or "
            "isolated signals support at most a verify"
        )

    boundary = document.get("execution_boundary", {})
    allowed = {entry.strip().casefold() for entry in boundary.get("may_do", [])}
    forbidden = {entry.strip().casefold() for entry in boundary.get("must_not_do", [])}
    contradictions = sorted(allowed & forbidden)
    if contradictions:
        problems.append(
            "execution_boundary contradicts itself; the same entry appears in "
            f"may_do and must_not_do: {contradictions}"
        )

    if document.get("mode") == "ux3_council":
        challenges = document.get("council_record", {}).get("challenges", [])
        if not any(ch.get("objection_to") != "none" for ch in challenges):
            problems.append(
                "council challenge round is vacuous: at least one challenge "
                "must object to another lane (objection_to != none)"
            )
    return problems


def main():
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 1
    document = json.loads(Path(sys.argv[1]).read_text())
    problems = check(document)
    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

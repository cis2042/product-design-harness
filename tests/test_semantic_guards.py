"""Regression tests for the semantic guards added after release acceptance.

Covers: evidence-tier verdict gate, lane stop_reason_class alignment,
execution-boundary self-contradiction, and vacuous council challenge rounds.
"""

import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_json(relative_path):
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def run_check(document):
    """Run scripts/check_review.py on a document; return (exit_code, stderr)."""
    target = ROOT / "tests" / "_guard_probe.json"
    target.write_text(json.dumps(document), encoding="utf-8")
    try:
        completed = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "check_review.py"), str(target)],
            capture_output=True,
            text=True,
        )
        return completed.returncode, completed.stderr
    finally:
        target.unlink(missing_ok=True)


class SemanticGuardTests(unittest.TestCase):
    def setUp(self):
        self.quick = load_json("examples/quick-gate-review.json")
        self.standard = load_json("examples/standard-gate-review.json")
        self.council = load_json("examples/ux3-council-review.json")

    def test_all_golden_examples_still_pass(self):
        for name in [
            "examples/quick-gate-review.json",
            "examples/standard-gate-review.json",
            "examples/ux3-council-review.json",
            "examples/live-coding-review.json",
            "examples/stop-reframe-review.json",
        ]:
            code, err = run_check(load_json(name))
            self.assertEqual(0, code, f"{name}: {err}")

    def test_t1_evidence_cannot_continue(self):
        document = copy.deepcopy(self.quick)
        for lane in document["reviews"].values():
            lane["evidence_tier"] = "t1"
        document["evidence_tier"] = "t1"
        code, err = run_check(document)
        self.assertNotEqual(0, code)
        self.assertIn("can never return continue", err)

    def test_t0_evidence_forces_stop_reframe(self):
        document = copy.deepcopy(self.standard)
        document["reviews"]["evidence"]["evidence_tier"] = "t0"
        document["evidence_tier"] = "t0"
        code, err = run_check(document)
        self.assertNotEqual(0, code)

    def test_t1_verify_is_still_allowed(self):
        code, err = run_check(copy.deepcopy(self.standard))
        self.assertEqual(0, code, err)

    def test_stop_lane_requires_stop_reason_class(self):
        document = copy.deepcopy(self.quick)
        lane = document["reviews"]["evidence"]
        lane["verdict"] = "stop_reframe"
        document["combined_verdict"] = "stop_reframe"
        document["weakest_flow"] = "evidence"
        document["context_pack_required"] = False
        document["reframed_question"] = "What is the smallest provable slice?"
        code, err = run_check(document)
        self.assertNotEqual(0, code)
        self.assertIn("stop_reason_class", err)

        lane["stop_reason_class"] = "core_evidence"
        code, err = run_check(document)
        self.assertEqual(0, code, err)

    def test_non_stop_lane_rejects_stop_reason_class(self):
        document = copy.deepcopy(self.quick)
        document["reviews"]["user"]["stop_reason_class"] = "actor"
        code, _ = run_check(document)
        self.assertNotEqual(0, code)

    def test_execution_boundary_cannot_contradict_itself(self):
        document = copy.deepcopy(self.quick)
        entry = document["execution_boundary"]["may_do"][0]
        document["execution_boundary"]["must_not_do"].append(entry.upper())
        code, err = run_check(document)
        self.assertNotEqual(0, code)
        self.assertIn("contradicts itself", err)

    def test_council_challenge_round_cannot_be_vacuous(self):
        document = copy.deepcopy(self.council)
        for challenge in document["council_record"]["challenges"]:
            challenge["objection_to"] = "none"
            challenge["position_change"] = "unchanged"
        code, err = run_check(document)
        self.assertNotEqual(0, code)
        self.assertIn("vacuous", err)



class CouncilInputExampleTests(unittest.TestCase):
    def test_council_input_example_validates(self):
        from jsonschema import Draft202012Validator
        from referencing import Registry, Resource

        resources = []
        schemas = {}
        for path in (ROOT / "schemas").glob("*.json"):
            schema = json.loads(path.read_text(encoding="utf-8"))
            schemas[path.name] = schema
            resource = Resource.from_contents(schema)
            resources.extend([
                (schema.get("$id", path.name), resource),
                (path.name, resource),
                (
                    "https://cis2042.github.io/product-design-harness/schemas/"
                    + path.name,
                    resource,
                ),
            ])
        registry = Registry().with_resources(resources)
        document = load_json("examples/ux3-council-input.json")
        validator = Draft202012Validator(
            schemas["council-input.schema.json"], registry=registry
        )
        errors = [
            f"{error.json_path}: {error.message}"
            for error in validator.iter_errors(document)
        ]
        self.assertEqual([], errors)

    def test_council_input_example_has_blind_round_discipline(self):
        document = load_json("examples/ux3-council-input.json")
        for review in document["independent_reviews"]:
            self.assertEqual("independent", review["review_round"])
            self.assertNotIn("objection_to", review)
        for review in document["challenge_reviews"]:
            self.assertEqual("challenge", review["review_round"])
            self.assertNotEqual("none", review["objection_to"])


if __name__ == "__main__":
    unittest.main()

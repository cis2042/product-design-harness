import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CommunityGovernanceTests(unittest.TestCase):
    def test_mit_license_remains_the_canonical_unmodified_license(self):
        digest = hashlib.sha256((ROOT / "LICENSE").read_bytes()).hexdigest()
        self.assertEqual(
            "4b4f6e1475a86afa35d3418ced212d6d34b732ad118f4a11626b9e00f30f5ee7",
            digest,
        )

    def test_repository_has_complete_community_health_surfaces(self):
        for relative_path in [
            "CONTRIBUTING.md",
            "GOVERNANCE.md",
            "CODE_OF_CONDUCT.md",
            "community/README.md",
            ".github/PULL_REQUEST_TEMPLATE.md",
            ".github/ISSUE_TEMPLATE/field_evidence.yml",
            ".github/ISSUE_TEMPLATE/decision_rule.yml",
            ".github/ISSUE_TEMPLATE/bug_report.yml",
            ".github/ISSUE_TEMPLATE/config.yml",
        ]:
            self.assertTrue((ROOT / relative_path).is_file(), relative_path)

    def test_contributing_contract_prioritizes_strategic_field_evidence(self):
        text = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
        for phrase in [
            "strategic product judgment",
            "Field evidence",
            "User Flow",
            "Evidence Flow",
            "Business Flow",
            "counter-signal",
            "observed outcome",
            "Designer-in-the-Loop",
            "Fork or branch",
            "Pull Request",
            "No direct commits to main",
        ]:
            self.assertIn(phrase, text)

    def test_governance_separates_contribution_from_canonical_decisions(self):
        text = (ROOT / "GOVERNANCE.md").read_text(encoding="utf-8")
        for role in ["Contributor", "Evidence Steward", "Maintainer"]:
            self.assertIn(role, text)
        self.assertIn("Canonical UX3", text)
        self.assertIn("weakest flow", text)
        self.assertIn("conflict of interest", text)
        self.assertIn("maintainer approval", text)

    def test_field_evidence_form_requests_decision_quality_not_showcase_copy(self):
        text = (
            ROOT / ".github" / "ISSUE_TEMPLATE" / "field_evidence.yml"
        ).read_text(encoding="utf-8")
        for phrase in [
            "Product stage",
            "Decision before UX3",
            "User Flow observation",
            "Evidence Flow observation",
            "Business Flow observation",
            "Counter-signal",
            "Human judgment",
            "Observed outcome",
            "Consent and redaction",
        ]:
            self.assertIn(phrase, text)

    def test_pull_requests_require_evidence_boundary_and_validation(self):
        text = (
            ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md"
        ).read_text(encoding="utf-8")
        for phrase in [
            "Strategic decision impact",
            "Evidence and counter-signal",
            "Human judgment boundary",
            "Validation",
            "No unsupported outcome claims",
        ]:
            self.assertIn(phrase, text)

    def test_readme_invites_community_without_reducing_scope_to_visuals(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Community-built strategic design knowledge", text)
        self.assertIn("prototype, visual, or animation", text)
        self.assertIn("Submit field evidence", text)
        self.assertIn("CONTRIBUTING.md", text)
        self.assertIn("GOVERNANCE.md", text)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE_ROOT = ROOT / ".agents" / "skills" / "product-design-harness"
BINARY_ASSET_SUFFIXES = {".gif", ".ico", ".jpeg", ".jpg", ".png", ".webp"}
IGNORED_PATH_PARTS = {".git", ".superpowers", ".venv", "__pycache__"}
REPOSITORY_PATH_TOKEN = re.compile(
    r"`((?:\.\./)?(?:[A-Za-z0-9_.-]+/)+[A-Za-z0-9_.-]+)`"
)
BARE_FILE_TOKEN = re.compile(r"`([A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)+)`")
CANONICAL_RULE_ID = re.compile(r"ux3\.rule\.[a-z0-9_]+\Z")


def fail(message):
    print(message, file=sys.stderr)
    raise SystemExit(1)


def is_ascii_exempt_path(path):
    return path.relative_to(ROOT).parts[:1] == ("i18n",)


def should_check_repository_paths(path):
    relative_parts = path.relative_to(ROOT).parts
    if relative_parts[:1] == (".superpowers",):
        return False
    return relative_parts[:2] != ("docs", "superpowers")


def should_check_bare_reference(token):
    return CANONICAL_RULE_ID.fullmatch(token) is None


def iter_files():
    for path in ROOT.rglob("*"):
        if path.is_file() and not IGNORED_PATH_PARTS.intersection(path.parts):
            yield path


def validate_json_files():
    for path in sorted((ROOT / "schemas").glob("*.json")):
        json.loads(path.read_text(encoding="utf-8"))
    for path in sorted((ROOT / "i18n").glob("*.json")):
        json.loads(path.read_text(encoding="utf-8"))


def validate_svg_files():
    for path in sorted((ROOT / "assets").glob("*.svg")):
        ET.parse(path)


def validate_ascii_policy():
    for path in iter_files():
        if path.suffix.lower() in BINARY_ASSET_SUFFIXES or is_ascii_exempt_path(path):
            continue
        data = path.read_text(encoding="utf-8", errors="ignore")
        if any(ord(ch) > 127 for ch in data):
            fail(f"non-ascii content: {path.relative_to(ROOT)}")


def validate_repository_paths():
    known_dirs = [
        ROOT,
        ROOT / "schemas",
        ROOT / "templates",
        ROOT / "prompts",
        ROOT / "examples",
        ROOT / "docs",
        ROOT / "agents",
        ROOT / "adapters",
        ROOT / "scripts",
        ROOT / "tests",
        ROOT / "assets",
        ROOT / "i18n",
    ]
    missing = []
    for path in sorted(ROOT.rglob("*.md")):
        if not should_check_repository_paths(path):
            continue
        text = path.read_text(encoding="utf-8")
        for token in REPOSITORY_PATH_TOKEN.findall(text):
            candidates = [ROOT / token, path.parent / token]
            if token.startswith("resources/"):
                candidates.append(BUNDLE_ROOT / token)
            if not any(candidate.exists() for candidate in candidates):
                missing.append(f"{path.relative_to(ROOT)}: {token}")
        for token in BARE_FILE_TOKEN.findall(text):
            if "/" in token or not should_check_bare_reference(token):
                continue
            candidates = [path.parent / token] + [directory / token for directory in known_dirs]
            if not any(candidate.exists() for candidate in candidates):
                missing.append(f"{path.relative_to(ROOT)}: {token}")
    if missing:
        fail("missing repository paths:\n" + "\n".join(missing))


def main():
    validate_json_files()
    validate_svg_files()
    validate_ascii_policy()
    validate_repository_paths()
    print("ok")


if __name__ == "__main__":
    main()

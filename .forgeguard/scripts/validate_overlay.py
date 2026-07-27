#!/usr/bin/env python3
"""ForgeGuard distribution overlay validator.

Checks the ForgeGuard overlay in this repository:

  * banner assets exist, are PNG, are exactly 2172x724, and are referenced by README.md
  * FORK_UPSTREAM_BASE parses and validates against its schema
  * .forgeguard/docs.yml parses and validates against the ForgeGuard docs schema
  * README.md declares the required maintained-fork disclosures
  * versions agree across FORK_UPSTREAM_BASE and README.md
  * internal Markdown links inside ForgeGuard-owned docs resolve to real files
  * with --base, the diff against the fork default branch adds only ForgeGuard-owned
    files and modifies nothing but README.md

Exit code 0 means every check passed. Run from the repository root:

    python3 .forgeguard/scripts/validate_overlay.py
"""

from __future__ import annotations

import argparse
import json
import os
import re
import struct
import subprocess
import sys

BANNER_W, BANNER_H = 2172, 724
BANNER_DIR = "docs/site/assets/repository"
# Paths ForgeGuard owns. Must stay in step with the delta inventory in
# docs/site/fork/forgeguard-changes.md.
FG_PATHS = [
    "README.md",
    "SUPPORT.md",
    "FORK_UPSTREAM_BASE",
    ".forgeguard",
    "docs/site",
    "docs/maintainers",
    ".github/workflows/forgeguard-",  # prefix match, see fg_owned()
    ".github/dependabot.yml",
]


def fg_owned(path: str) -> bool:
    """True when a path is ForgeGuard-owned and therefore allowed to differ from upstream."""
    for p in FG_PATHS:
        if path == p or path.startswith(p.rstrip("/") + "/") or path.startswith(p):
            return True
    return False

failures: list[str] = []
passes: list[str] = []


def ok(msg: str) -> None:
    passes.append(msg)
    print(f"  PASS  {msg}")


def fail(msg: str) -> None:
    failures.append(msg)
    print(f"  FAIL  {msg}")


def section(name: str) -> None:
    print(f"\n== {name} ==")


def png_size(path: str):
    with open(path, "rb") as f:
        head = f.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", head[16:24])


# --------------------------------------------------------------------------- checks

def check_banners(readme: str) -> None:
    section("Banners")
    for variant in ("dark", "light"):
        rel = f"{BANNER_DIR}/banner-{variant}.png"
        if not os.path.isfile(rel):
            fail(f"missing banner: {rel}")
            continue
        size = png_size(rel)
        if size is None:
            fail(f"not a PNG: {rel}")
        elif size != (BANNER_W, BANNER_H):
            fail(f"{rel} is {size[0]}x{size[1]}, expected {BANNER_W}x{BANNER_H}")
        else:
            ok(f"{rel} is a valid PNG at {BANNER_W}x{BANNER_H}")
        if f"banner-{variant}.png" not in readme:
            fail(f"README.md does not reference banner-{variant}.png")
        else:
            ok(f"README.md references banner-{variant}.png")
    if "<picture>" in readme:
        ok("README.md uses the ForgeGuard adaptive <picture> banner block")
    else:
        fail("README.md does not use a <picture> banner block")
    m = re.search(r'<img[^>]*banner-dark\.png"[^>]*alt="([^"]*)"', readme)
    if not m:
        m = re.search(r'<img[^>]*alt="([^"]+)"[^>]*banner-dark\.png', readme)
    if m and "ForgeGuard" in m.group(1) and len(m.group(1)) > 20:
        ok("banner alt text names ForgeGuard and is descriptive")
    else:
        fail("banner <img> alt text missing or not descriptive")


def load_yaml(path: str):
    try:
        import yaml  # type: ignore
    except ImportError:
        fail("PyYAML is required to validate YAML files (pip install pyyaml)")
        return None
    with open(path) as f:
        return yaml.safe_load(f)


def validate_schema(instance, schema_path: str, label: str) -> None:
    try:
        import jsonschema  # type: ignore
    except ImportError:
        fail(f"jsonschema is required to validate {label} (pip install jsonschema)")
        return
    with open(schema_path) as f:
        schema = json.load(f)
    try:
        jsonschema.validate(instance=instance, schema=schema)
        ok(f"{label} validates against {schema_path}")
    except jsonschema.ValidationError as e:  # type: ignore[attr-defined]
        fail(f"{label} schema error at {list(e.path)}: {e.message}")


def check_fork_base():
    section("FORK_UPSTREAM_BASE")
    path = "FORK_UPSTREAM_BASE"
    if not os.path.isfile(path):
        fail("FORK_UPSTREAM_BASE is missing")
        return None
    data = load_yaml(path)
    if data is None:
        return None
    ok("FORK_UPSTREAM_BASE parses as YAML")
    data.pop("$schema", None)
    validate_schema(data, ".forgeguard/schemas/fork-upstream-base.schema.json",
                    "FORK_UPSTREAM_BASE")
    base = data.get("base", {})
    if base.get("kind") == "branch-snapshot" and base.get("branch"):
        ok("fork base is a branch snapshot with a named branch")
    else:
        fail("fork base must be a branch-snapshot naming its branch")
    return data


def check_docs_yml():
    section(".forgeguard/docs.yml")
    path = ".forgeguard/docs.yml"
    if not os.path.isfile(path):
        fail("missing .forgeguard/docs.yml")
        return
    data = load_yaml(path)
    if data is None:
        return
    ok("docs.yml parses as YAML")
    data.pop("$schema", None)
    validate_schema(data, ".forgeguard/schemas/docs.schema.json", "docs.yml")
    if data.get("project", {}).get("kind") != "maintained-fork":
        fail("project.kind must be 'maintained-fork' for a ForgeGuard fork distribution")
    else:
        ok("project.kind is 'maintained-fork'")
    if "upstream" not in data:
        fail("maintained-fork docs.yml must declare an 'upstream' block")
    else:
        ok("docs.yml declares upstream tracking policy")
    entry = os.path.join(data.get("source", {}).get("content_root", ""),
                         data.get("source", {}).get("entrypoint", ""))
    if entry and os.path.isfile(entry):
        ok(f"docs entrypoint exists: {entry}")
    else:
        fail(f"docs entrypoint missing: {entry}")


def check_readme(readme: str, fork) -> None:
    section("README contract")
    required = {
        "maintained-fork disclosure": "Maintained fork",
        "non-endorsement statement": "not endorsed",
        "upstream attribution": "claims no ownership",
        "no-artifact disclosure": "publishes no build artifacts",
        "upstream install routing": "## How to install and run it",
        "what ForgeGuard adds": "## What ForgeGuard adds",
        "what ForgeGuard does not add": "## What ForgeGuard does not add",
        "security section": "## Security",
        "support routing": "## Support",
        "license and attribution": "## License and attribution",
        "upstream README preservation link": "upstream-readme.md",
    }
    for label, needle in required.items():
        if needle in readme:
            ok(f"README declares {label}")
        else:
            fail(f"README missing {label} (expected marker: {needle!r})")

    if fork:
        sha = fork.get("base", {}).get("commit", "")
        if sha and sha[:12] in readme:
            ok("README states the fork base commit")
        else:
            fail("README does not state the fork base commit")
        if "not a release channel" in readme:
            ok("README warns that the fork is not a release channel")
        else:
            fail("README does not warn that the fork is not a release channel")
        if fork.get("forgeguard", {}).get("publishes_artifacts") is False:
            ok("FORK_UPSTREAM_BASE declares publishes_artifacts: false")


def check_no_artifact_claims() -> None:
    """This fork publishes nothing, so no ForgeGuard-owned doc may advertise an artifact."""
    section("No unpublished-artifact claims")
    targets = ["README.md", "SUPPORT.md"]
    for base in ("docs/site", "docs/maintainers"):
        for dirpath, _, names in os.walk(base):
            targets += [os.path.join(dirpath, n) for n in names if n.endswith(".md")]
    # upstream-readme.md is upstream's own text; forgeguard-changes.md documents the
    # withdrawn scope by name, which is the one place the string is legitimate.
    skip = {"upstream-readme.md", "forgeguard-changes.md"}
    hits = 0
    for t in targets:
        if os.path.basename(t) in skip or not os.path.isfile(t):
            continue
        with open(t, encoding="utf-8", errors="replace") as f:
            text = f.read()
        for needle in ("ghcr.io/forgeguard-ai", "docker pull ghcr.io"):
            if needle in text:
                fail(f"{t} references an unpublished ForgeGuard artifact ({needle!r})")
                hits += 1
    if hits == 0:
        ok("no ForgeGuard-owned document claims an unpublished image or release")


def check_links() -> None:
    section("Internal documentation links")
    roots = ["README.md", "SUPPORT.md"]
    for base in ("docs/site", "docs/maintainers"):
        for dirpath, _, names in os.walk(base):
            roots += [os.path.join(dirpath, n) for n in names if n.endswith(".md")]
    # The preserved upstream README is upstream's content; its links are not ours to police.
    roots = [r for r in roots if os.path.basename(r) != "upstream-readme.md"]
    pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    broken = 0
    checked = 0
    for src in roots:
        if not os.path.isfile(src):
            continue
        with open(src, encoding="utf-8", errors="replace") as f:
            text = f.read()
        for target in pattern.findall(text):
            target = target.split(" ")[0].strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = target.split("#")[0]
            if not target:
                continue
            resolved = os.path.normpath(os.path.join(os.path.dirname(src), target))
            checked += 1
            if not os.path.exists(resolved):
                fail(f"broken link in {src}: {target}")
                broken += 1
    if broken == 0:
        ok(f"all {checked} internal documentation links resolve")


def check_base_diff(base_ref) -> None:
    """Only ForgeGuard-owned files may be added; only README.md may be modified."""
    section("Diff against the fork default branch")
    have = subprocess.run(["git", "rev-parse", "--verify", "--quiet", base_ref],
                          capture_output=True, text=True)
    if have.returncode != 0:
        print(f"  SKIP  base ref {base_ref} not available locally")
        return
    merge_base = subprocess.run(["git", "merge-base", base_ref, "HEAD"],
                                capture_output=True, text=True).stdout.strip() or base_ref
    out = subprocess.run(["git", "diff", "--name-status", merge_base],
                         capture_output=True, text=True).stdout.splitlines()
    # git diff ignores untracked files, which would make this check pass vacuously
    # on an uncommitted tree. Fold them in as additions.
    untracked = subprocess.run(["git", "ls-files", "--others", "--exclude-standard"],
                               capture_output=True, text=True).stdout.split()
    if untracked:
        print(f"  NOTE  {len(untracked)} untracked file(s) treated as additions")
        out += [f"A\t{p}" for p in untracked]
    violations, added = [], 0
    for line in out:
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        status, path = parts[0][:1], parts[-1]
        if path == "README.md" and status == "M":
            continue  # replaced by design; upstream content preserved under docs/site/fork/
        if status == "A" and fg_owned(path):
            added += 1
            continue
        violations.append(f"{status} {path}")
    if violations:
        fail("diff against the default branch touches non-ForgeGuard files "
             "(only README.md may be modified, and only ForgeGuard-owned files added):\n        "
             + "\n        ".join(violations[:40]))
    else:
        ok(f"docs-only diff vs {base_ref}: README.md modified, "
           f"{added} ForgeGuard files added, nothing else touched")


def check_no_secrets() -> None:
    section("Secret hygiene (ForgeGuard-owned files)")
    patterns = [
        (re.compile(r"gh[pousr]_[A-Za-z0-9]{16,}"), "GitHub token"),
        (re.compile(r"hf_[A-Za-z0-9]{20,}"), "Hugging Face token"),
        (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key id"),
        (re.compile(r"-----BEGIN (RSA |OPENSSH |EC )?PRIVATE KEY-----"), "private key"),
    ]
    hits = 0
    for base in FG_PATHS:
        if os.path.isfile(base):
            targets = [base]
        else:
            targets = []
            for dirpath, _, names in os.walk(base):
                targets += [os.path.join(dirpath, n) for n in names]
        for t in targets:
            if t.endswith((".png", ".jpg", ".svg", ".ico")):
                continue
            try:
                with open(t, encoding="utf-8", errors="ignore") as f:
                    text = f.read()
            except OSError:
                continue
            for rx, label in patterns:
                if rx.search(text):
                    fail(f"possible {label} committed in {t}")
                    hits += 1
    if hits == 0:
        ok("no credential-shaped strings found in ForgeGuard-owned files")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", default="",
                    help="git ref of the fork default branch to diff against "
                         "(e.g. origin/main); skipped when omitted")
    args = ap.parse_args()

    if not os.path.isfile("README.md"):
        print("must be run from the repository root", file=sys.stderr)
        return 2

    with open("README.md", encoding="utf-8") as f:
        readme = f.read()

    print("ForgeGuard distribution overlay validation")
    check_banners(readme)
    fork = check_fork_base()
    check_docs_yml()
    check_readme(readme, fork)
    check_links()
    check_no_artifact_claims()
    if args.base:
        check_base_diff(args.base)
    check_no_secrets()

    print(f"\n{'='*60}")
    print(f"passed: {len(passes)}   failed: {len(failures)}")
    if failures:
        print("\nFAILURES:")
        for f_ in failures:
            print(f"  - {f_}")
        return 1
    print("All ForgeGuard overlay checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

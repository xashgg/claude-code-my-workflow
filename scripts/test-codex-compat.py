#!/usr/bin/env python3
"""Exercise drift detection and preservation in disposable copies; no third-party dependencies."""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("codex_compat", ROOT / "scripts/codex-compat.py")
compat = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(compat)


def snapshot(root: Path) -> dict[str, bytes]:
    return {p.relative_to(root).as_posix(): p.read_bytes()
            for p in root.rglob("*") if p.is_file()}


class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="codex compatibility ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        # Copy only reviewed inputs and the three hand-written instruction docs.
        for directory in (".claude", "scripts", ".githooks"):
            shutil.copytree(ROOT / directory, self.root / directory,
                            ignore=shutil.ignore_patterns("__pycache__"))
        for relative in ("AGENTS.md", "CLAUDE.md", "MEMORY.md", "README.md", ".codex/bridge.md",
                         ".codex/README.md", ".github/workflows/gates.yml",
                         ".github/workflows/deploy.yml", ".github/workflows/codex-compat.yml"):
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, destination)

    def generate(self):
        return compat.synchronize(self.root, generate=True)

    def original(self, name="compile-latex"):
        return self.root / f".claude/skills/{name}/SKILL.md"

    def test_inventory_exclusions_and_explicit_policies(self):
        outputs = compat.expected_outputs(self.root)
        manifest = json.loads(outputs[compat.MAP_PATH])
        self.assertEqual(len(manifest["skills"]), 61)
        self.assertEqual(len(manifest["agents"]), 18)
        self.assertEqual(len(manifest["rules"]), 37)
        self.assertEqual(len(manifest["hooks"]), 11)
        self.assertEqual(len([p for p in outputs if p.endswith("SKILL.md")]), 55)
        self.assertEqual(len([p for p in outputs if p.endswith("openai.yaml")]), 19)
        for name, entry in manifest["skills"].items():
            self.assertEqual(entry["adapter"] is None, name in compat.EXCLUDED)
            if entry["adapter"]:
                metadata = compat.frontmatter(compat.read(self.original(name)), "skills")
                policy = f"{compat.PREFIX}{name}/agents/openai.yaml"
                self.assertEqual(policy in outputs, metadata.get("disable-model-invocation", False))
                if policy in outputs:
                    self.assertIn("allow_implicit_invocation: false", outputs[policy])

    def test_generation_preserves_inputs_and_is_idempotent(self):
        before = snapshot(self.root)
        self.assertEqual(len(self.generate()), 75)
        after = snapshot(self.root)
        for path, data in before.items():
            self.assertEqual(after[path], data, path)
        self.assertEqual(self.generate(), [])
        self.assertEqual(compat.synchronize(self.root), [])

    def test_missing_outputs_are_detected_without_writes(self):
        before = snapshot(self.root)
        self.assertTrue(compat.synchronize(self.root))
        self.assertEqual(snapshot(self.root), before)

    def test_source_edit_invalidates_adapter_and_manifest(self):
        self.generate()
        path = self.original()
        path.write_text(compat.read(path) + "\nNew upstream instruction.\n", encoding="utf-8")
        before = snapshot(self.root)
        changed = compat.synchronize(self.root)
        self.assertIn(".agents/skills/academic-compile-latex/SKILL.md", changed)
        self.assertIn(compat.MAP_PATH, changed)
        self.assertEqual(snapshot(self.root), before)

    def test_policy_change_is_detected_and_never_silently_deleted(self):
        self.generate()
        path = self.original("checkpoint")
        path.write_text(compat.read(path).replace("disable-model-invocation: true",
                                                "disable-model-invocation: false"), encoding="utf-8")
        before = snapshot(self.root)
        with self.assertRaisesRegex(compat.CompatibilityError, "unexpected adapter"):
            self.generate()
        self.assertEqual(snapshot(self.root), before)

    def test_new_component_requires_classification(self):
        for kind, relative in (("skills", ".claude/skills/unreviewed/SKILL.md"),
                               ("agents", ".claude/agents/unreviewed.md"),
                               ("rules", ".claude/rules/unreviewed.md"),
                               ("hooks", ".claude/hooks/unreviewed.py")):
            with self.subTest(kind=kind):
                path = self.root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("unreviewed", encoding="utf-8")
                try:
                    with self.assertRaisesRegex(compat.CompatibilityError, "inventory"):
                        self.generate()
                finally:
                    path.unlink()

    def test_removed_component_requires_review(self):
        self.original().unlink()
        with self.assertRaisesRegex(compat.CompatibilityError, "missing=.*compile-latex"):
            self.generate()

    def test_unknown_metadata_and_tool_fail_before_writes(self):
        path = self.original()
        source = compat.read(path)
        for addition in ("new-runtime-option: true", 'allowed-tools: ["UnknownTool"]'):
            with self.subTest(addition=addition):
                body = source.replace('allowed-tools: ["Read", "Bash", "Glob"]\n', "")
                path.write_text(body.replace("---\n", "---\n" + addition + "\n", 1), encoding="utf-8")
                before = snapshot(self.root)
                with self.assertRaises(compat.CompatibilityError):
                    self.generate()
                self.assertEqual(snapshot(self.root), before)

    def test_invalid_frontmatter_is_not_ignored(self):
        for text in ("name: broken", "---\nname: a", "---\nname: a\nname: b\n---\n",
                     "---\nname: a\ndescription: &anchor unsafe\n---\n"):
            with self.subTest(text=text):
                with self.assertRaises(compat.CompatibilityError):
                    compat.frontmatter(text, "skills")

    def test_block_descriptions_and_scope_lists(self):
        metadata = compat.frontmatter(
            '---\nname: x\ndescription: |\n  First line.\n  Second line.\n---\n', "skills")
        self.assertEqual(metadata["description"], "First line. Second line.")
        for data in ('paths: ["**/*.R", "Slides/**/*.tex"]',
                     'paths:\n  # retained meaning\n  - "**/*.R"\n  - "Slides/**/*.tex"'):
            self.assertEqual(compat.frontmatter("---\n" + data + "\n---\n", "rules")["paths"],
                             ["**/*.R", "Slides/**/*.tex"])

    def test_crlf_does_not_create_drift(self):
        self.generate()
        path = self.original()
        path.write_bytes(compat.read(path).replace("\n", "\r\n").encode("utf-8"))
        adapter = self.root / ".agents/skills/academic-compile-latex/SKILL.md"
        adapter.write_bytes(compat.read(adapter).replace("\n", "\r\n").encode("utf-8"))
        self.assertEqual(compat.synchronize(self.root), [])

    def test_unowned_output_cannot_be_overwritten(self):
        path = self.root / ".agents/skills/academic-compile-latex/SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text("User work.\n", encoding="utf-8")
        before = snapshot(self.root)
        with self.assertRaisesRegex(compat.CompatibilityError, "unowned"):
            self.generate()
        self.assertEqual(snapshot(self.root), before)

    def test_unowned_map_cannot_be_overwritten(self):
        (self.root / compat.MAP_PATH).write_text('{}\n', encoding="utf-8")
        with self.assertRaisesRegex(compat.CompatibilityError, "unowned"):
            self.generate()

    def test_unexpected_adapter_file_is_not_deleted(self):
        self.generate()
        path = self.root / ".agents/skills/academic-checkpoint/notes.md"
        path.write_text("User notes.\n", encoding="utf-8")
        with self.assertRaisesRegex(compat.CompatibilityError, "nothing deleted"):
            self.generate()
        self.assertEqual(path.read_text(encoding="utf-8"), "User notes.\n")

    def test_broken_reference_blocks_generation(self):
        (self.root / ".codex/bridge.md").unlink()
        with self.assertRaises(OSError):
            self.generate()

    def test_links_are_checked_from_adapter_directory(self):
        outputs = compat.expected_outputs(self.root)
        outputs[".agents/skills/academic-compile-latex/SKILL.md"] += "\n[bad](missing.md)\n"
        with self.assertRaisesRegex(compat.CompatibilityError, "broken reference"):
            compat.validate_links(self.root, outputs)

    def test_shared_source_drift_is_detected(self):
        self.generate()
        path = self.root / ".claude/settings.json"
        path.write_text(compat.read(path) + "\n", encoding="utf-8")
        self.assertIn(compat.MAP_PATH, compat.synchronize(self.root))

    def test_nested_analysis_source_drift_is_detected(self):
        self.generate()
        path = self.root / "scripts/R/00_run_all.R"
        path.write_text(compat.read(path) + "\n# Upstream change.\n", encoding="utf-8")
        self.assertIn(compat.MAP_PATH, compat.synchronize(self.root))

    def test_bytecode_is_not_a_shared_source(self):
        self.generate()
        path = self.root / "scripts/__pycache__/local.cpython-313.pyc"
        path.parent.mkdir()
        path.write_bytes(b"\xff\x00\x01")
        self.assertEqual(compat.synchronize(self.root), [])

    def test_manifest_path_order_is_platform_independent(self):
        manifest = json.loads(compat.expected_outputs(self.root)[compat.MAP_PATH])
        keys = list(manifest["shared"])
        self.assertEqual(keys, sorted(keys))

    def test_adapter_uses_reference_not_copied_procedure(self):
        outputs = compat.expected_outputs(self.root)
        for path, content in outputs.items():
            if path.endswith("SKILL.md"):
                self.assertIn("../../../.claude/skills/", content)
                self.assertNotIn("allowed-tools:", content)
                self.assertLess(len(content.splitlines()), 35)

    def test_output_traversal_is_rejected(self):
        for path in ("../escape", str(self.root.parent / "escape")):
            with self.assertRaises(compat.CompatibilityError):
                compat.safe_path(self.root, path)

    def test_hygiene_gate_accepts_only_declared_root_additions(self):
        # Use an isolated index: the real checkout and its index are untouched.
        self.generate()
        environment = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        def git(*args):
            return subprocess.run(["git", "-C", str(self.root), *args], env=environment,
                                  capture_output=True, text=True, check=True)
        git("init", "-q")
        for relative in ("AGENTS.md", ".agents", ".codex", ".claude", "scripts", ".githooks", ".github"):
            git("add", "--", relative)
        check = [sys.executable, "-B", str(self.root / "scripts/check-repo-hygiene.py")]
        result = subprocess.run(check, env=environment, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        forbidden = self.root / "unapproved-root.md"
        forbidden.write_text("Still forbidden.\n", encoding="utf-8")
        git("add", "--", forbidden.name)
        result = subprocess.run(check, env=environment, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unapproved-root.md", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)

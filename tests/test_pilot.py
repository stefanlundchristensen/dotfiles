"""Consumer checks of the authored Git/Zsh contracts, not Nix evaluation.

All mutable test state stays under this checkout, with fake HOME and no access
to the user's Git configuration or shell rc files. No activation is performed.
"""

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
GIT_CONFIG = ROOT / "files/gitconfig"
ZDOTDIR = ROOT / "files/zsh"


class PilotConfigTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".test-tmp"
        scratch.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.home = self.work / "home"
        self.home.mkdir()
        self.env = {
            "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
            "HOME": str(self.home),
            "XDG_CONFIG_HOME": str(self.home / ".config"),
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": str(GIT_CONFIG),
            "ZDOTDIR": str(ZDOTDIR),
            "TERM": "dumb",
            "LC_ALL": "C",
        }
        for tool in ("git", "zsh"):
            self.assertIsNotNone(shutil.which(tool), f"required consumer missing: {tool}")

    def run_tool(self, *args, check=True):
        return subprocess.run(
            args, cwd=self.work, env=self.env, text=True,
            capture_output=True, check=check,
        )

    def test_git_semantic_contract(self):
        # Git itself parses the declarative file. Exact keys bound its ownership.
        parsed = self.run_tool("git", "config", "--global", "--list").stdout.splitlines()
        self.assertEqual(dict(line.split("=", 1) for line in parsed), {
            "init.defaultbranch": "main", "pull.ff": "only",
            "fetch.prune": "true", "merge.conflictstyle": "zdiff3",
        })
        for key in ("user.name", "user.email", "credential.helper", "include.path"):
            result = self.run_tool("git", "config", "--global", "--get", key, check=False)
            self.assertEqual(result.returncode, 1)
        self.assertEqual(self.run_tool("git", "config", "--global", "--type=bool", "--get", "fetch.prune").stdout.strip(), "true")

    def test_git_initial_branch_and_local_identity(self):
        self.run_tool("git", "init", "--quiet", "repo")
        self.assertEqual(self.run_tool("git", "-C", "repo", "symbolic-ref", "--short", "HEAD").stdout.strip(), "main")
        self.run_tool("git", "-C", "repo", "config", "user.name", "Disposable Test")
        self.run_tool("git", "-C", "repo", "config", "user.email", "test@example.invalid")
        self.run_tool("git", "-C", "repo", "commit", "--quiet", "--allow-empty", "-m", "test")
        self.assertEqual(self.run_tool("git", "-C", "repo", "log", "-1", "--format=%ae").stdout.strip(), "test@example.invalid")

    def test_zsh_syntax(self):
        self.run_tool("zsh", "-d", "-n", str(ZDOTDIR / ".zshrc"))

    def test_zsh_isolated_interactive_contract(self):
        script = '''
print -r -- "$PROMPT"
print -r -- "$HISTSIZE:$SAVEHIST"
print -r -- "$options[interactivecomments]:$options[histignoredups]:$options[sharehistory]"
print -r -- "$PATH"
'''
        # -d disables global rc files after the unavoidable system zshenv;
        # ZDOTDIR avoids private user rc files; this is NOT a login shell.
        result = self.run_tool("zsh", "-d", "-i", "-c", script)
        self.assertEqual(result.stdout.splitlines(), [
            "[pilot] %~ %# ", "1:0", "on:on:off", self.env["PATH"],
        ])
        self.assertEqual(list(self.home.rglob("*")), [])


if __name__ == "__main__":
    unittest.main()

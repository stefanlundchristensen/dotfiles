"""Lock graph regression checks; Nix itself verifies fetched NAR contents."""

import base64
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PilotLockTests(unittest.TestCase):
    def test_lock_matches_declared_pins_and_follows(self):
        pins = dict(re.findall(
            r'([\w-]+)\.url = "github:([^\"]+)";',
            (ROOT / "flake.nix").read_text(),
        ))
        self.assertEqual(set(pins), {"nixpkgs", "home-manager", "nix-darwin"})
        lock = json.loads((ROOT / "flake.lock").read_text())
        self.assertEqual(lock["version"], 7)
        self.assertEqual(lock["root"], "root")
        nodes = lock["nodes"]
        self.assertEqual(set(nodes), {"root", *pins})
        self.assertEqual(nodes["root"]["inputs"], {name: name for name in pins})
        for name, url in pins.items():
            with self.subTest(input=name):
                owner, repo, rev = url.split("/")
                self.assertRegex(rev, r"^[0-9a-f]{40}$")
                original = {"type": "github", "owner": owner, "repo": repo, "rev": rev}
                self.assertEqual(nodes[name]["original"], original)
                for key, value in original.items():
                    self.assertEqual(nodes[name]["locked"][key], value)
                algorithm, digest = nodes[name]["locked"]["narHash"].split("-", 1)
                self.assertEqual(algorithm, "sha256")
                self.assertEqual(len(base64.b64decode(digest, validate=True)), 32)
        for name in ("home-manager", "nix-darwin"):
            self.assertEqual(nodes[name]["inputs"], {"nixpkgs": ["nixpkgs"]})


if __name__ == "__main__":
    unittest.main()

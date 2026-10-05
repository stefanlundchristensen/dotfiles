"""Lock graph regression checks; Nix itself verifies fetched NAR contents."""

import base64
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PilotLockTests(unittest.TestCase):
    def test_lock_graph_revisions_and_hash_format(self):
        repositories = {
            "nixpkgs": ("NixOS", "nixpkgs"),
            "home-manager": ("nix-community", "home-manager"),
            "nix-darwin": ("nix-darwin", "nix-darwin"),
        }
        lock = json.loads((ROOT / "flake.lock").read_text())
        self.assertEqual(lock["version"], 7)
        self.assertEqual(lock["root"], "root")
        nodes = lock["nodes"]
        self.assertEqual(set(nodes), {"root", *repositories})
        self.assertEqual(nodes["root"]["inputs"], {name: name for name in repositories})
        for name, (owner, repo) in repositories.items():
            with self.subTest(input=name):
                rev = nodes[name]["original"]["rev"]
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

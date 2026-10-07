"""Offline Lazy integration; set NVIM and LAZY_NVIM_SOURCE to installed consumers."""

from contextlib import ExitStack
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
NVIM = os.environ.get("NVIM", shutil.which("nvim"))
LAZY = os.environ.get("LAZY_NVIM_SOURCE")


@unittest.skipUnless(NVIM, "requires Neovim")
class NvimPluginSpecTests(unittest.TestCase):
    def test_plugin_specs_execute_as_lazy_tables(self):
        # Execute the declarative interface with its real Lua consumer. This
        # catches malformed specs before Lazy attempts network installation.
        script = """
local ok, err = pcall(function()
  for _, file in ipairs(vim.fn.glob(vim.env.SPEC_DIR .. '/*.lua', false, true)) do
    local specs = assert(loadfile(file))()
    assert(type(specs) == 'table', file)
    for _, spec in ipairs(specs) do
      assert(type(spec) == 'table' and type(spec[1]) == 'string', file)
    end
  end
end)
if not ok then
  io.stderr:write(tostring(err) .. '\\n')
  vim.cmd('cquit 1')
else
  vim.cmd('qa!')
end
"""
        result = subprocess.run(
            [NVIM, '--headless', '--clean', '-i', 'NONE', '-c', 'lua ' + script],
            cwd=ROOT,
            env={**os.environ, 'SPEC_DIR': str(ROOT / 'home/.config/nvim/lua/plugins')},
            capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


@unittest.skipUnless(NVIM and LAZY, "requires Neovim and LAZY_NVIM_SOURCE checkout")
class NvimLockTests(unittest.TestCase):
    def test_readonly_config_first_and_repeated_startup(self):
        scratch = ROOT / ".test-tmp"
        scratch.mkdir(exist_ok=True)
        with ExitStack() as stack:
            tmp = stack.enter_context(tempfile.TemporaryDirectory(dir=scratch))
            work = Path(tmp)
            config = work / "config/nvim"
            config.mkdir(parents=True)
            env = {
                "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
                "HOME": str(work / "home"),
                "XDG_CONFIG_HOME": str(work / "config"),
                "XDG_DATA_HOME": str(work / "data"),
                "XDG_STATE_HOME": str(work / "state"),
                "XDG_CACHE_HOME": str(work / "cache"),
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": "/dev/null",
                "TERM": "dumb",
            }

            def git(*args):
                return subprocess.check_output(
                    ["git", *args], cwd=work, env=env, text=True
                ).strip()

            repo = work / "fixture"
            git("init", "--quiet", str(repo))
            git("-C", str(repo), "config", "user.name", "Test")
            git("-C", str(repo), "config", "user.email", "test@example.invalid")
            (repo / "plugin").mkdir()
            (repo / "plugin/fixture.lua").write_text("vim.g.fixture_revision = 'pinned'\n")
            git("-C", str(repo), "add", ".")
            git("-C", str(repo), "commit", "--quiet", "-m", "pinned")
            pinned = git("-C", str(repo), "rev-parse", "HEAD")
            branch = git("-C", str(repo), "branch", "--show-current")
            (repo / "plugin/fixture.lua").write_text("vim.g.fixture_revision = 'newer'\n")
            git("-C", str(repo), "commit", "--quiet", "-am", "newer")

            lazy_path = work / "data/nvim/lazy/lazy.nvim"
            lazy_path.parent.mkdir(parents=True)
            shutil.copytree(LAZY, lazy_path)
            lazy_pin = git("-C", str(lazy_path), "rev-parse", "HEAD")
            (config / "lua/plugins").mkdir(parents=True)
            shutil.copy2(ROOT / "home/.config/nvim/lua/plugin.lua", config / "lua/plugin.lua")
            (config / "init.lua").write_text("require('plugin')\n")
            (config / "lua/plugins/fixture.lua").write_text(
                "return {{name = 'fixture', url = " + json.dumps(str(repo))
                + ", lazy = false}}\n"
            )
            seed = {
                "lazy.nvim": {"branch": "main", "commit": lazy_pin},
                "fixture": {"branch": branch, "commit": pinned},
            }
            supplied = json.dumps(seed).encode()
            (config / "lazy-lock.json").write_bytes(supplied)
            for path in config.rglob("*"):
                path.chmod(0o555 if path.is_dir() else 0o444)
            config.chmod(0o555)
            stack.callback(self.restore_permissions, config)

            check = work / "check.lua"
            check.write_text("""
local ok, err = pcall(function()
  assert(vim.g.fixture_revision == 'pinned', 'plugin revision changed')
  local config = require('lazy.core.config')
  assert(config.options.lockfile == vim.fn.stdpath('state') .. '/lazy/lazy-lock.json')
  assert(require('lazy.manage.lock').get(config.plugins.fixture).commit == vim.env.FIXTURE_PIN)
  assert(vim.v.errmsg == '', vim.v.errmsg)
end)
if not ok then
  io.stderr:write(tostring(err) .. '\\n')
  vim.cmd('cquit 1')
else
  vim.cmd('qa!')
end
""")
            env["FIXTURE_PIN"] = pinned
            lock = work / "state/nvim/lazy/lazy-lock.json"
            for startup in range(2):
                result = subprocess.run(
                    [NVIM, "--headless", "-i", "NONE", "-c", "luafile " + str(check)],
                    cwd=work, env=env, text=True, capture_output=True, timeout=60,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual((config / "lazy-lock.json").read_bytes(), supplied)
                persisted = json.loads(lock.read_text())
                self.assertEqual(persisted["fixture"], seed["fixture"])
                if startup == 0:
                    persisted["preserved-state"] = {"branch": "main", "commit": "a" * 40}
                    lock.write_text(json.dumps(persisted))
                    existing = lock.read_bytes()
                else:
                    self.assertEqual(lock.read_bytes(), existing)

    @staticmethod
    def restore_permissions(config):
        if config.exists():
            config.chmod(0o755)
            for path in config.rglob("*"):
                path.chmod(0o755 if path.is_dir() else 0o644)


if __name__ == "__main__":
    unittest.main()

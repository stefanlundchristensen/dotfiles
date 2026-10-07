local lazypath = vim.fn.stdpath('data') .. '/lazy/lazy.nvim'
if not vim.uv.fs_stat(lazypath) then
  vim.fn.system({ 'git', 'clone', '--filter=blob:none',
    'https://github.com/folke/lazy.nvim.git', '--branch=stable', lazypath })
end
vim.opt.rtp:prepend(lazypath)
local lockfile = vim.fn.stdpath('state') .. '/lazy/lazy-lock.json'
if not vim.uv.fs_stat(lockfile) then
  vim.fn.mkdir(vim.fn.fnamemodify(lockfile, ':h'), 'p')
  assert(vim.uv.fs_copyfile(vim.fn.stdpath('config') .. '/lazy-lock.json', lockfile, { excl = true }))
  assert(vim.uv.fs_chmod(lockfile, tonumber('600', 8)))
end
require('lazy').setup('plugins', { lockfile = lockfile })

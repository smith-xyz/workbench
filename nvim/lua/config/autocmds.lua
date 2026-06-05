local augroup = vim.api.nvim_create_augroup("user_autocmds", { clear = true })

vim.api.nvim_create_autocmd("TermOpen", {
  group = augroup,
  pattern = "*",
  callback = function()
    vim.defer_fn(function()
      if vim.api.nvim_buf_get_option(0, "buftype") == "terminal" then
        vim.cmd("startinsert")
      end
    end, 100)
  end,
})

vim.api.nvim_create_autocmd("TextYankPost", {
  group = augroup,
  pattern = "*",
  callback = function()
    local hl = vim.hl or vim.highlight
    hl.on_yank({ timeout = 200 })
  end,
})

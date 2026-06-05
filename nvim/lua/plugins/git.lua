return {
  {
    "tpope/vim-fugitive",
    cmd = { "Git", "G", "Gdiffsplit", "Gvdiffsplit" },
    keys = {
      { "<leader>gs", "<cmd>Git<CR>", desc = "Git status" },
    },
  },

  { "tpope/vim-rhubarb", dependencies = { "tpope/vim-fugitive" } },

  {
    "lewis6991/gitsigns.nvim",
    event = { "BufReadPre", "BufNewFile" },
    opts = {
      signs = {
        add = { text = "+" },
        change = { text = "~" },
        delete = { text = "_" },
        topdelete = { text = "‾" },
        changedelete = { text = "~" },
      },
      on_attach = function(bufnr)
        local gs = package.loaded.gitsigns
        local map = vim.keymap.set
        local opts = { buffer = bufnr }

        map("n", "]g", gs.next_hunk, opts)
        map("n", "[g", gs.prev_hunk, opts)
        map("n", "<leader>gp", gs.preview_hunk, opts)
        map("n", "<leader>gr", gs.reset_hunk, opts)
        map("n", "<leader>gR", gs.reset_buffer, opts)
        map("n", "<leader>gS", gs.stage_hunk, opts)
        map("n", "<leader>gu", gs.undo_stage_hunk, opts)
        map("n", "<leader>gB", gs.blame_line, opts)
      end,
    },
  },
}

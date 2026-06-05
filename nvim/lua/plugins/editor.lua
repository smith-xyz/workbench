return {
  -- File explorer as buffer
  {
    "stevearc/oil.nvim",
    dependencies = { "nvim-tree/nvim-web-devicons" },
    opts = {
      default_file_explorer = true,
      view_options = { show_hidden = true },
      float = {
        padding = 2,
        max_width = 120,
        max_height = 40,
      },
    },
  },

  -- Jump labels
  {
    "folke/flash.nvim",
    event = "VeryLazy",
    keys = {
      { "s", mode = { "n", "x", "o" }, function() require("flash").jump() end, desc = "Flash" },
      { "S", mode = { "n", "x", "o" }, function() require("flash").treesitter() end, desc = "Flash Treesitter" },
      { "r", mode = "o", function() require("flash").remote() end, desc = "Remote Flash" },
    },
    opts = {},
  },

  -- Surround text objects
  {
    "kylechui/nvim-surround",
    version = "^3",
    event = "VeryLazy",
    opts = {},
  },

  -- Auto pairs
  {
    "windwp/nvim-autopairs",
    event = "InsertEnter",
    opts = {},
  },

  -- Comment toggle
  {
    "numToStr/Comment.nvim",
    event = "VeryLazy",
    opts = {},
  },

  -- Tmux pane navigation
  {
    "numToStr/Navigator.nvim",
    event = "VeryLazy",
    config = function()
      require("Navigator").setup()
      local map = vim.keymap.set
      map("n", "<C-h>", "<cmd>NavigatorLeft<CR>")
      map("n", "<C-j>", "<cmd>NavigatorDown<CR>")
      map("n", "<C-k>", "<cmd>NavigatorUp<CR>")
      map("n", "<C-l>", "<cmd>NavigatorRight<CR>")
    end,
  },

  -- Zoxide integration
  { "nanotee/zoxide.vim", cmd = { "Z", "Zi" } },

  -- Repeat plugin commands with .
  { "tpope/vim-repeat", event = "VeryLazy" },

  -- Unimpaired bracket mappings
  { "tummetott/unimpaired.nvim", event = "VeryLazy", opts = {} },
}

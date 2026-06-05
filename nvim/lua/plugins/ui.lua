return {
  -- Colorscheme
  {
    "folke/tokyonight.nvim",
    lazy = false,
    priority = 1000,
    config = function()
      require("tokyonight").setup({
        transparent = true,
        styles = {
          sidebars = "transparent",
          floats = "transparent",
        },
      })
      vim.cmd.colorscheme("tokyonight")
    end,
  },

  -- Statusline
  {
    "nvim-lualine/lualine.nvim",
    dependencies = { "nvim-tree/nvim-web-devicons" },
    opts = {
      options = {
        theme = "tokyonight",
        globalstatus = true,
      },
      sections = {
        lualine_a = { "mode" },
        lualine_b = { "branch", "diff", "diagnostics" },
        lualine_c = { { "filename", path = 1 } },
        lualine_x = { "encoding", "filetype" },
        lualine_y = { "progress" },
        lualine_z = { "location" },
      },
    },
  },

  -- Command line / notifications / messages
  {
    "folke/noice.nvim",
    event = "VeryLazy",
    dependencies = {
      "MunifTanjim/nui.nvim",
      "rcarriga/nvim-notify",
    },
    opts = {
      lsp = {
        override = {
          ["vim.lsp.util.convert_input_to_markdown_lines"] = true,
          ["vim.lsp.util.stylize_markdown"] = true,
          ["cmp.entry.get_documentation"] = true,
        },
      },
      presets = {
        bottom_search = true,
        command_palette = true,
        long_message_to_split = true,
      },
    },
  },

  -- Keybinding hints
  {
    "folke/which-key.nvim",
    event = "VeryLazy",
    opts = {},
  },

  -- Snacks (dashboard, zen, indent, etc.)
  {
    "folke/snacks.nvim",
    priority = 1000,
    lazy = false,
    opts = {
      dashboard = { enabled = true },
      indent = { enabled = true },
      scope = { enabled = true },
      notifier = { enabled = false },
    },
    keys = {
      { "<leader>bd", function() Snacks.bufdelete() end, desc = "Delete buffer" },
      { "<leader>ba", function() Snacks.bufdelete.all() end, desc = "Delete all buffers" },
      { "<leader>bo", function() Snacks.bufdelete.other() end, desc = "Delete other buffers" },
      { "<leader>bz", function() Snacks.zen() end, desc = "Zen mode" },
    },
  },

  -- Highlight colors inline
  {
    "brenoprata10/nvim-highlight-colors",
    event = "BufReadPre",
    opts = { render = "virtual" },
  },

  -- Illuminate word under cursor
  {
    "RRethy/vim-illuminate",
    event = "BufReadPre",
    config = function()
      require("illuminate").configure({
        delay = 200,
        filetypes_denylist = { "oil", "TelescopePrompt" },
      })
    end,
  },

  -- Icons
  { "nvim-tree/nvim-web-devicons", lazy = true },
}

return {
  {
    "nvim-treesitter/nvim-treesitter",
    build = ":TSUpdate",
    event = { "BufReadPre", "BufNewFile" },
    dependencies = {
      "nvim-treesitter/nvim-treesitter-textobjects",
      "nvim-treesitter/nvim-treesitter-context",
      "windwp/nvim-ts-autotag",
    },
    config = function()
      require("nvim-treesitter.configs").setup({
        ensure_installed = {
          "bash", "c", "css", "dockerfile", "go", "gomod", "gosum",
          "html", "javascript", "json", "lua", "make", "markdown",
          "markdown_inline", "python", "rust", "terraform", "toml",
          "tsx", "typescript", "vim", "vimdoc", "yaml",
        },
        highlight = { enable = true },
        indent = { enable = true },
        autotag = { enable = true },
        textobjects = {
          select = {
            enable = true,
            lookahead = true,
            keymaps = {
              ["af"] = "@function.outer",
              ["if"] = "@function.inner",
              ["ac"] = "@class.outer",
              ["ic"] = "@class.inner",
              ["aa"] = "@parameter.outer",
              ["ia"] = "@parameter.inner",
            },
          },
          move = {
            enable = true,
            set_jumps = true,
            goto_next_start = { ["]f"] = "@function.outer", ["]c"] = "@class.outer" },
            goto_prev_start = { ["[f"] = "@function.outer", ["[c"] = "@class.outer" },
          },
        },
      })

      require("treesitter-context").setup({ max_lines = 3 })
    end,
  },
}

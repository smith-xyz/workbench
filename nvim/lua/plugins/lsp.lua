return {
  {
    "neovim/nvim-lspconfig",
    event = { "BufReadPre", "BufNewFile" },
    dependencies = {
      "williamboman/mason.nvim",
      "williamboman/mason-lspconfig.nvim",
      "folke/lazydev.nvim",
    },
    config = function()
      local lspconfig = require("lspconfig")
      local capabilities = require("blink.cmp").get_lsp_capabilities()

      vim.api.nvim_create_autocmd("LspAttach", {
        callback = function(ev)
          local opts = { buffer = ev.buf }
          local map = vim.keymap.set
          map("n", "gd", vim.lsp.buf.definition, opts)
          map("n", "gD", vim.lsp.buf.declaration, opts)
          map("n", "gr", vim.lsp.buf.references, opts)
          map("n", "gi", vim.lsp.buf.implementation, opts)
          map("n", "K", vim.lsp.buf.hover, opts)
          map("n", "<leader>rn", vim.lsp.buf.rename, opts)
          map({ "n", "v" }, "<leader>ca", vim.lsp.buf.code_action, opts)
          map("n", "<leader>D", vim.lsp.buf.type_definition, opts)
          map("n", "]d", vim.diagnostic.goto_next, opts)
          map("n", "[d", vim.diagnostic.goto_prev, opts)
          map("n", "<leader>e", vim.diagnostic.open_float, opts)
        end,
      })

      local servers = {
        gopls = {},
        rust_analyzer = {},
        lua_ls = {
          settings = {
            Lua = {
              workspace = { checkThirdParty = false },
              telemetry = { enable = false },
            },
          },
        },
        pyright = {},
        ts_ls = {},
        yamlls = {
          settings = {
            yaml = {
              schemas = {},
              validate = true,
              schemaStore = { enable = true },
            },
          },
        },
        terraformls = {},
      }

      require("mason").setup()
      require("mason-lspconfig").setup({
        ensure_installed = vim.tbl_keys(servers),
        handlers = {
          function(server_name)
            local opts = servers[server_name] or {}
            opts.capabilities = capabilities
            lspconfig[server_name].setup(opts)
          end,
        },
      })
    end,
  },

  {
    "williamboman/mason.nvim",
    cmd = "Mason",
    opts = {},
  },

  { "williamboman/mason-lspconfig.nvim" },

  {
    "folke/lazydev.nvim",
    ft = "lua",
    opts = {
      library = {
        { path = "${3rd}/luv/library", words = { "vim%.uv" } },
      },
    },
  },
}

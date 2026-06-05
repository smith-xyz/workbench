return {
  {
    "nvim-telescope/telescope.nvim",
    branch = "0.1.x",
    dependencies = {
      "nvim-lua/plenary.nvim",
      { "nvim-telescope/telescope-fzf-native.nvim", build = "make" },
      "nvim-telescope/telescope-ui-select.nvim",
      "nvim-telescope/telescope-live-grep-args.nvim",
      "debugloop/telescope-undo.nvim",
    },
    config = function()
      local telescope = require("telescope")
      local actions = require("telescope.actions")

      telescope.setup({
        defaults = {
          mappings = {
            i = {
              ["<C-j>"] = actions.move_selection_next,
              ["<C-k>"] = actions.move_selection_previous,
              ["<C-q>"] = actions.send_selected_to_qflist + actions.open_qflist,
            },
          },
          file_ignore_patterns = { "node_modules", ".git/", "vendor/" },
        },
        extensions = {
          fzf = { fuzzy = true, override_generic_sorter = true, override_file_sorter = true },
          ["ui-select"] = { require("telescope.themes").get_dropdown() },
          undo = {},
        },
      })

      telescope.load_extension("fzf")
      telescope.load_extension("ui-select")
      telescope.load_extension("live_grep_args")
      telescope.load_extension("undo")

      local builtin = require("telescope.builtin")
      local map = vim.keymap.set
      map("n", "<leader>ff", builtin.find_files, { desc = "Find files" })
      map("n", "<leader>fg", builtin.live_grep, { desc = "Live grep" })
      map("n", "<leader>fb", builtin.buffers, { desc = "Buffers" })
      map("n", "<leader>fh", builtin.help_tags, { desc = "Help tags" })
      map("n", "<leader>fs", builtin.lsp_document_symbols, { desc = "Document symbols" })
      map("n", "<leader>fi", builtin.lsp_incoming_calls, { desc = "Incoming calls" })
      map("n", "<leader>fo", builtin.lsp_outgoing_calls, { desc = "Outgoing calls" })
      map("n", "<leader>fw", builtin.grep_string, { desc = "Grep word under cursor" })
      map("n", "<leader>gc", builtin.git_commits, { desc = "Git commits" })
      map("n", "<leader>gb", builtin.git_branches, { desc = "Git branches" })
      map("n", "<leader>fk", builtin.keymaps, { desc = "Keymaps" })
      map("n", "<leader>/", builtin.current_buffer_fuzzy_find, { desc = "Fuzzy find in buffer" })
      map("n", "<leader>fu", "<cmd>Telescope undo<CR>", { desc = "Undo tree" })
      map("n", "<leader>fa", function()
        require("telescope").extensions.live_grep_args.live_grep_args()
      end, { desc = "Grep with args" })
    end,
  },
}

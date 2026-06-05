return {
  {
    "ThePrimeagen/harpoon",
    branch = "harpoon2",
    dependencies = { "nvim-lua/plenary.nvim" },
    config = function()
      local harpoon = require("harpoon")
      harpoon:setup()

      local map = vim.keymap.set
      map("n", "<leader>a", function() harpoon:list():add() end, { desc = "Harpoon add" })
      map("n", "<C-e>", function() harpoon.ui:toggle_quick_menu(harpoon:list()) end, { desc = "Harpoon menu" })
      map("n", "<C-t>", function() harpoon:list():select(1) end, { desc = "Harpoon 1" })
      map("n", "<C-s>", function() harpoon:list():select(2) end, { desc = "Harpoon 2" })
      map("n", "<C-b>", function() harpoon:list():select(3) end, { desc = "Harpoon 3" })
      map("n", "<C-g>", function() harpoon:list():select(4) end, { desc = "Harpoon 4" })
    end,
  },
}

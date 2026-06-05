local map = vim.keymap.set

-- File explorer
map("n", "-", "<CMD>Oil --float<CR>", { desc = "Open parent directory" })

-- Exit insert mode
map("i", "jj", "<Esc><Esc>", { desc = "Esc" })

-- Make Y behave like C or D
map("n", "Y", "y$")

-- Select all
map("n", "==", "gg<S-v>G")

-- Keep window centered when going up/down
map("n", "J", "mzJ`z")
map("n", "<C-d>", "<C-d>zz")
map("n", "<C-u>", "<C-u>zz")
map("n", "n", "nzzzv")
map("n", "N", "Nzzzv")

-- Paste without overwriting register
map("v", "p", '"_dP')

-- System clipboard yank
map("n", "<leader>y", '"+y', { desc = "Yank to clipboard" })
map("v", "<leader>y", '"+y', { desc = "Yank to clipboard" })
map("n", "<leader>Y", '"+Y', { desc = "Yank line to clipboard" })

-- Delete to black hole
map("n", "<leader>d", '"_d', { desc = "Delete (no register)" })
map("v", "<leader>d", '"_d', { desc = "Delete (no register)" })

-- Disable Q
map("n", "Q", "<nop>")

-- Buffers
map("n", "<leader>q", "<cmd>bd<CR>", { desc = "Close buffer" })
map("n", "<leader>w", "<cmd>bp|bd #<CR>", { desc = "Close buffer; keep split" })

-- Quickfix / location list
map("n", "<leader>h", "<cmd>cnext<CR>zz", { desc = "Next quickfix" })
map("n", "<leader>;", "<cmd>cprev<CR>zz", { desc = "Prev quickfix" })
map("n", "<leader>k", "<cmd>lnext<CR>zz", { desc = "Next loclist" })
map("n", "<leader>j", "<cmd>lprev<CR>zz", { desc = "Prev loclist" })

-- Replace word under cursor
map("n", "<leader>s", [[:%s/\<<C-r><C-w>\>/<C-r><C-w>/gI<Left><Left><Left>]], { desc = "Replace word under cursor" })

-- Make file executable
map("n", "<leader>x", "<cmd>!chmod +x %<CR>", { silent = true, desc = "Make file executable" })

-- Source current file
map("n", "<leader><leader>", function() vim.cmd("so") end, { desc = "Source current file" })

-- Copy file paths
map("n", "<leader>cf", '<cmd>let @+ = expand("%")<CR>', { desc = "Copy filename" })
map("n", "<leader>cp", '<cmd>let @+ = expand("%:p")<CR>', { desc = "Copy filepath" })

-- Dismiss Noice
map("n", "<leader>nd", "<cmd>NoiceDismiss<CR>", { desc = "Dismiss notification" })

-- Zoxide
map("n", "<leader>Z", "<cmd>Zi<CR>", { desc = "Zoxide" })

-- Resize splits
map("n", "<C-S-Down>", ":resize +2<CR>", { desc = "Resize split down" })
map("n", "<C-S-Up>", ":resize -2<CR>", { desc = "Resize split up" })
map("n", "<C-Left>", ":vertical resize -2<CR>", { desc = "Resize split left" })
map("n", "<C-Right>", ":vertical resize +2<CR>", { desc = "Resize split right" })

-- Visual: stay in indent mode
map("v", "<", "<gv")
map("v", ">", ">gv")

-- Line start/end jumps
map({ "n", "o", "x" }, "<s-h>", "^", { desc = "Start of line" })
map({ "n", "o", "x" }, "<s-l>", "g_", { desc = "End of line" })

-- Move block
map("v", "J", ":m '>+1<CR>gv=gv", { desc = "Move block down" })
map("v", "K", ":m '<-2<CR>gv=gv", { desc = "Move block up" })

-- Search highlighted text
map("v", "//", 'y/<C-R>"<CR>', { desc = "Search highlighted" })

-- Terminal
map("t", "<C-t>", "<C-\\><C-n>")

# workbench

Personal dev environment: editor configs, neovim, shell, toolchain bootstrap, snippets, and project scaffolding.

## Install

| Command | What it does |
|---------|-------------|
| `make setup` | Install toolchain (go, rust, node, bun, uv, docker, ollama, etc.) |
| `make install` | Symlink all configs (vscode, cursor, nvim, shell) |
| `make extensions` | Install VSCode extensions from list |
| `make snippets` | Build snippet files from `vscode/snippets/src/` |
| `make scaffold` | Scaffold a new project from templates (fzf picker) |
| `make template` | Apply a project-level .vscode template (fzf picker) |
| `make uninstall` | Remove symlinks (originals in `~/.workbench-backup/`) |

## Quick start

```bash
git clone https://github.com/smith-xyz/workbench.git ~/workbench
cd ~/workbench
make setup    # toolchain
make install  # configs
```

First `nvim` launch auto-installs plugins, treesitter parsers, and LSP servers.

After install, `scaffold` is available globally to create new projects from templates.

## Convention

`WORKBENCH_DIR` is auto-exported by `shell/profile.d/env.sh` (derived from the install symlink). VSCode tasks, neovim snippets, and the scaffold command all resolve paths through it. Override by setting `export WORKBENCH_DIR=/your/path` before sourcing.

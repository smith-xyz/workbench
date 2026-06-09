#!/usr/bin/env bash
# Portable environment setup — sourced from ~/.zprofile.d

# Resolve workbench repo root from this script's symlink (override by pre-setting WORKBENCH_DIR)
if [ -z "${WORKBENCH_DIR:-}" ]; then
  if [ -L "${BASH_SOURCE[0]:-$0}" ]; then
    _wb_script=$(readlink "${BASH_SOURCE[0]:-$0}")
  else
    _wb_script="${BASH_SOURCE[0]:-$0}"
  fi
  WORKBENCH_DIR=$(cd "$(dirname "$_wb_script")/../.." && pwd)
  export WORKBENCH_DIR
  unset _wb_script
fi

export PATH="$HOME/.local/bin:$PATH"
export CLICOLOR=1
export TERM=xterm-256color

# Ollama (written by make setup → ~/.config/workbench/ollama.env)
if [ -f "$HOME/.config/workbench/ollama.env" ]; then
  # shellcheck source=/dev/null
  . "$HOME/.config/workbench/ollama.env"
fi

# Go
if command -v go &>/dev/null; then
  _go_path=$(go env GOPATH)
  export PATH="$_go_path/bin:$PATH"
  unset _go_path
fi

# Bun
if [ -d "$HOME/.bun" ]; then
  export BUN_INSTALL="$HOME/.bun"
  export PATH="$BUN_INSTALL/bin:$PATH"
fi

# Cargo/Rust
if [ -f "$HOME/.cargo/env" ]; then
  . "$HOME/.cargo/env"
fi

# nvm
export NVM_DIR="$HOME/.nvm"
if [ -s "$NVM_DIR/nvm.sh" ]; then
  . "$NVM_DIR/nvm.sh"
elif [ -s "/opt/homebrew/opt/nvm/nvm.sh" ]; then
  . "/opt/homebrew/opt/nvm/nvm.sh"
elif [ -s "/usr/local/opt/nvm/nvm.sh" ]; then
  . "/usr/local/opt/nvm/nvm.sh"
fi

# uv completions — zsh needs compinit (in .zshrc); login profile runs too early
if command -v uv &>/dev/null; then
  if [ -n "${ZSH_VERSION:-}" ]; then
    if whence compdef &>/dev/null; then
      eval "$(uv generate-shell-completion zsh 2>/dev/null || true)"
    fi
  else
    eval "$(uv generate-shell-completion bash 2>/dev/null || true)"
  fi
fi

#!/usr/bin/env bash
set -euo pipefail

# Idempotent dev toolchain bootstrap.
# Supports: macOS, Ubuntu/Debian, Fedora/RHEL.
# Re-run safely anytime - only installs what's missing.

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
RESET='\033[0m'

installed() { command -v "$1" &>/dev/null; }

info()  { echo -e "${BOLD}[setup]${RESET} $1"; }
skip()  { echo -e "${GREEN}[skip]${RESET} $1 already installed"; }
doing() { echo -e "${YELLOW}[install]${RESET} $1"; }
die()   { echo -e "${RED}[error]${RESET} $1"; exit 1; }

# ─── Detect OS ─────────────────────────────────────────────────────────────────

detect_os() {
  case "$(uname -s)" in
    Darwin) OS="macos" ;;
    Linux)
      if [ -f /etc/os-release ]; then
        . /etc/os-release
        case "$ID" in
          ubuntu|debian|pop) OS="debian" ;;
          fedora|rhel|centos|rocky|alma) OS="fedora" ;;
          *) die "Unsupported Linux distro: $ID" ;;
        esac
      else
        die "Cannot detect Linux distribution"
      fi
      ;;
    *) die "Unsupported OS: $(uname -s)" ;;
  esac
  info "Detected OS: $OS"
}

# ─── Package manager helpers ───────────────────────────────────────────────────

pkg_install() {
  case "$OS" in
    macos)
      for pkg in "$@"; do
        if ! brew list "$pkg" &>/dev/null; then
          doing "$pkg"
          brew install "$pkg"
        else
          skip "$pkg"
        fi
      done
      ;;
    debian)
      for pkg in "$@"; do
        if ! dpkg -s "$pkg" &>/dev/null 2>&1; then
          doing "$pkg"
          sudo apt-get install -y "$pkg"
        else
          skip "$pkg"
        fi
      done
      ;;
    fedora)
      for pkg in "$@"; do
        if ! rpm -q "$pkg" &>/dev/null 2>&1; then
          doing "$pkg"
          sudo dnf install -y "$pkg"
        else
          skip "$pkg"
        fi
      done
      ;;
  esac
}

# ─── Homebrew (macOS only) ─────────────────────────────────────────────────────

install_brew() {
  if [ "$OS" != "macos" ]; then return; fi
  if ! installed brew; then
    doing "Homebrew"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    # Add brew to PATH for remainder of script
    eval "$(/opt/homebrew/bin/brew shellenv 2>/dev/null || /usr/local/bin/brew shellenv)"
  else
    skip "brew"
  fi
}

# ─── macOS Apps (casks) ────────────────────────────────────────────────────────

install_casks() {
  if [ "$OS" != "macos" ]; then return; fi
  info "Checking macOS apps..."

  local casks=(iterm2 docker)
  for cask in "${casks[@]}"; do
    if ! brew list --cask "$cask" &>/dev/null; then
      doing "$cask"
      brew install --cask "$cask"
    else
      skip "$cask"
    fi
  done
}

# ─── Core CLI tools ───────────────────────────────────────────────────────────

nvim_version_ok() {
  if ! installed nvim; then return 1; fi
  local ver
  ver=$(nvim --version | head -1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
  local major=${ver%%.*}
  local minor=${ver#*.}
  [ "$major" -gt 0 ] || [ "$minor" -ge 10 ]
}

install_packages() {
  info "Installing core packages..."

  case "$OS" in
    macos)
      pkg_install go fzf ripgrep fd zoxide neovim stylua shellcheck jq gh
      ;;
    debian)
      sudo apt-get update -qq
      pkg_install golang fzf ripgrep fd-find zoxide shellcheck jq
      # fd-find installs as fdfind; symlink to fd
      if installed fdfind && ! installed fd; then
        mkdir -p "$HOME/.local/bin"
        ln -sf "$(which fdfind)" "$HOME/.local/bin/fd"
        info "Symlinked fdfind -> ~/.local/bin/fd"
      fi
      # neovim from PPA for latest version
      if ! nvim_version_ok; then
        doing "neovim (PPA)"
        sudo add-apt-repository -y ppa:neovim-ppa/unstable
        sudo apt-get update -qq
        sudo apt-get install -y neovim
      else
        skip "neovim"
      fi
      # gh CLI
      if ! installed gh; then
        doing "gh"
        curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
        sudo apt-get update -qq && sudo apt-get install -y gh
      else
        skip "gh"
      fi
      ;;
    fedora)
      sudo dnf check-update -q || true
      pkg_install golang fzf ripgrep fd-find zoxide neovim ShellCheck jq gh
      # fd-find installs as fdfind on some versions
      if installed fdfind && ! installed fd; then
        mkdir -p "$HOME/.local/bin"
        ln -sf "$(which fdfind)" "$HOME/.local/bin/fd"
        info "Symlinked fdfind -> ~/.local/bin/fd"
      fi
      ;;
  esac
}

# ─── Containers (Docker / Podman) ──────────────────────────────────────────────

install_containers() {
  case "$OS" in
    macos)
      # Docker Desktop installed as cask above; add podman CLI
      if ! installed podman; then
        doing "podman"
        brew install podman
      else
        skip "podman"
      fi
      ;;
    debian)
      if ! installed docker; then
        doing "docker"
        curl -fsSL https://get.docker.com | sh
        sudo usermod -aG docker "$USER"
      else
        skip "docker"
      fi
      pkg_install podman
      ;;
    fedora)
      pkg_install podman
      if ! installed docker; then
        doing "docker"
        sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo
        sudo dnf install -y docker-ce docker-ce-cli containerd.io
        sudo systemctl enable --now docker
        sudo usermod -aG docker "$USER"
      else
        skip "docker"
      fi
      ;;
  esac
}

# ─── nvm (Node Version Manager) ───────────────────────────────────────────────

install_nvm() {
  if [ ! -d "$HOME/.nvm" ]; then
    doing "nvm"
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
  else
    skip "nvm"
  fi

  # Ensure nvm is loaded and LTS node is available
  export NVM_DIR="$HOME/.nvm"
  # shellcheck source=/dev/null
  [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
  if ! installed node; then
    doing "node (LTS via nvm)"
    nvm install --lts
  fi
}

# ─── Bun ───────────────────────────────────────────────────────────────────────

install_bun() {
  if ! installed bun; then
    doing "bun"
    curl -fsSL https://bun.sh/install | bash
  else
    skip "bun"
  fi
}

# ─── uv (Python) ──────────────────────────────────────────────────────────────

install_uv() {
  if ! installed uv; then
    doing "uv"
    curl -LsSf https://astral.sh/uv/install.sh | sh
  else
    skip "uv"
  fi
}

# ─── Rust (rustup) ────────────────────────────────────────────────────────────

install_rust() {
  if ! installed rustup; then
    doing "rust (rustup)"
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    # shellcheck source=/dev/null
    source "$HOME/.cargo/env"
  else
    skip "rustup"
    rustup update stable || info "rustup update failed (network?), continuing..."
  fi

  # stylua (Linux only - macOS gets it from brew)
  if [ "$OS" != "macos" ] && ! installed stylua; then
    doing "stylua (cargo)"
    cargo install stylua
  fi
}

# ─── Run ──────────────────────────────────────────────────────────────────────

detect_os
install_brew
install_casks
install_packages
install_containers
install_nvm
install_bun
install_uv
install_rust

echo ""
info "Done. Toolchain versions:"
echo "  go:     $(go version 2>/dev/null | awk '{print $3}' || echo 'not found')"
echo "  node:   $(node --version 2>/dev/null || echo 'not found')"
echo "  bun:    $(bun --version 2>/dev/null || echo 'not found')"
echo "  uv:     $(uv --version 2>/dev/null || echo 'not found')"
echo "  rustc:  $(rustc --version 2>/dev/null || echo 'not found')"
echo "  nvim:   $(nvim --version 2>/dev/null | head -1 || echo 'not found')"

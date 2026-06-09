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

# ─── Inventory ─────────────────────────────────────────────────────────────────

DEBIAN_DISTROS=(ubuntu debian pop)
FEDORA_DISTROS=(fedora rhel centos rocky alma)

MACOS_CASKS=(iterm2 docker)
MACOS_PACKAGES=(go fzf ripgrep fd zoxide neovim stylua shellcheck jq gh gnupg pinentry-mac)
DEBIAN_PACKAGES=(golang fzf ripgrep fd-find zoxide shellcheck jq gnupg)
FEDORA_PACKAGES=(golang fzf ripgrep fd-find zoxide neovim ShellCheck jq gh gnupg2)
FEDORA_DOCKER_PACKAGES=(docker-ce docker-ce-cli containerd.io)

OLLAMA_MODELS_24GB=(devstral-small-2:24b qwen3.6:35b-a3b qwen2.5-coder:7b)  # no deepseek — tight on 24 GB
OLLAMA_MODELS_48GB=(devstral-small-2:24b qwen3.6:35b-a3b deepseek-r1:32b qwen2.5-coder:7b)
OLLAMA_CTX_24GB=16384
OLLAMA_CTX_48GB=32768
OLLAMA_ENV_FIXED=(OLLAMA_KEEP_ALIVE=0 OLLAMA_FLASH_ATTENTION=1 OLLAMA_KV_CACHE_TYPE=q4_0)

VERSION_REPORT=(
  "go|go version 2>/dev/null | awk '{print \$3}'"
  "node|node --version 2>/dev/null"
  "bun|bun --version 2>/dev/null"
  "uv|uv --version 2>/dev/null"
  "rustc|rustc --version 2>/dev/null"
  "nvim|nvim --version 2>/dev/null | head -1"
  "ollama|ollama --version 2>/dev/null"
)

in_list() {
  local needle=$1 item
  shift
  for item in "$@"; do
    [ "$needle" = "$item" ] && return 0
  done
  return 1
}

# ─── Detect OS ─────────────────────────────────────────────────────────────────

detect_os() {
  case "$(uname -s)" in
    Darwin) OS="macos" ;;
    Linux)
      if [ -f /etc/os-release ]; then
        . /etc/os-release
        if in_list "$ID" "${DEBIAN_DISTROS[@]}"; then OS="debian"
        elif in_list "$ID" "${FEDORA_DISTROS[@]}"; then OS="fedora"
        else die "Unsupported Linux distro: $ID"
        fi
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

  local cask
  for cask in "${MACOS_CASKS[@]}"; do
    if ! brew list --cask "$cask" &>/dev/null; then
      doing "$cask"
      brew install --cask "$cask"
    else
      skip "$cask"
    fi
  done
}

# ─── Core CLI tools ───────────────────────────────────────────────────────────

NVIM_MIN_MINOR=10

nvim_version_ok() {
  if ! installed nvim; then return 1; fi
  local ver
  ver=$(nvim --version | head -1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
  local major=${ver%%.*}
  local minor=${ver#*.}
  [ "$major" -gt 0 ] || [ "$minor" -ge "$NVIM_MIN_MINOR" ]
}

install_packages() {
  info "Installing core packages..."

  case "$OS" in
    macos)
      pkg_install "${MACOS_PACKAGES[@]}"
      ;;
    debian)
      sudo apt-get update -qq
      pkg_install "${DEBIAN_PACKAGES[@]}"
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
      pkg_install "${FEDORA_PACKAGES[@]}"
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
        sudo dnf install -y "${FEDORA_DOCKER_PACKAGES[@]}"
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

# ─── Ollama ───────────────────────────────────────────────────────────────────
# One heavy model at a time (OLLAMA_KEEP_ALIVE=0). Profile: 48gb | 24gb | auto
# Override via OLLAMA_PROFILE in ~/.config/workbench/config

detect_ollama_profile() {
  if [ -n "${OLLAMA_PROFILE:-}" ]; then
    echo "$OLLAMA_PROFILE"
    return
  fi
  if [ "$OS" = "macos" ]; then
    local gb
    gb=$(( $(sysctl -n hw.memsize) / 1024 / 1024 / 1024 ))
    if [ "$gb" -le 26 ]; then echo "24gb"; else echo "48gb"; fi
  else
    echo "48gb"
  fi
}

configure_ollama_profile() {
  local profile
  profile=$(detect_ollama_profile)
  case "$profile" in
    24gb)
      OLLAMA_MODELS=("${OLLAMA_MODELS_24GB[@]}")
      OLLAMA_CONTEXT_LENGTH=$OLLAMA_CTX_24GB
      ;;
    48gb)
      OLLAMA_MODELS=("${OLLAMA_MODELS_48GB[@]}")
      OLLAMA_CONTEXT_LENGTH=$OLLAMA_CTX_48GB
      ;;
    *)
      die "unknown OLLAMA_PROFILE: $profile (use 24gb or 48gb)"
      ;;
  esac
  info "Ollama profile: $profile (${OLLAMA_CONTEXT_LENGTH} ctx, ${#OLLAMA_MODELS[@]} models)"
}

write_ollama_env() {
  local env_file=$1 entry
  mkdir -p "$(dirname "$env_file")"
  {
    echo "# Ollama — profile via OLLAMA_PROFILE in ~/.config/workbench/config"
    echo "export OLLAMA_CONTEXT_LENGTH=${OLLAMA_CONTEXT_LENGTH}"
    for entry in "${OLLAMA_ENV_FIXED[@]}"; do
      echo "export $entry"
    done
  } > "$env_file"
  info "Wrote $env_file"
}

apply_ollama_launchctl_env() {
  local entry key val
  launchctl setenv OLLAMA_CONTEXT_LENGTH "$OLLAMA_CONTEXT_LENGTH"
  for entry in "${OLLAMA_ENV_FIXED[@]}"; do
    key="${entry%%=*}"
    val="${entry#*=}"
    launchctl setenv "$key" "$val"
  done
  info "Restart Ollama app to apply daemon env"
}

install_ollama() {
  local env_file="${XDG_CONFIG_HOME:-$HOME/.config}/workbench/ollama.env"
  local workbench_config="${WORKBENCH_CONFIG:-$HOME/.config/workbench/config}"
  if [ -f "$workbench_config" ]; then
    source "$workbench_config"
  fi

  configure_ollama_profile

  if [ "$OS" = "macos" ]; then
    if ! brew list --cask ollama &>/dev/null; then
      doing "ollama"
      brew install --cask ollama
    else
      skip "ollama"
    fi
  elif ! installed ollama; then
    doing "ollama"
    curl -fsSL https://ollama.com/install.sh | sh
  else
    skip "ollama"
  fi

  write_ollama_env "$env_file"

  if [ "$OS" = "macos" ]; then
    apply_ollama_launchctl_env
  fi

  if ! ollama list &>/dev/null; then
    info "Ollama daemon not running — start the app, then re-run make setup to sync models"
    return
  fi

  local model name
  for model in "${OLLAMA_MODELS[@]}"; do
    doing "ollama pull $model"
    ollama pull "$model"
  done
  while IFS= read -r line; do
    name="${line%% *}"
    [ -z "$name" ] || [ "$name" = "NAME" ] && continue
    if ! printf '%s\n' "${OLLAMA_MODELS[@]}" | grep -qxF "$name"; then
      doing "ollama rm $name"
      ollama rm "$name"
    fi
  done < <(ollama list | tail -n +2)
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
install_ollama

echo ""
info "Done. Toolchain versions:"
for entry in "${VERSION_REPORT[@]}"; do
  label="${entry%%|*}"
  cmd="${entry#*|}"
  printf '  %-6s %s\n' "$label:" "$(eval "$cmd" || echo 'not found')"
done

#!/usr/bin/env bash
set -euo pipefail

YES="${YES:-0}"

say() { printf "%b\n" "$*"; }
die() { say "ERROR: $*"; exit 1; }

confirm() {
  if [[ "$YES" == "1" ]]; then
    return 0
  fi
  read -r -p "$1 [y/N] " ans
  [[ "${ans,,}" == "y" || "${ans,,}" == "yes" ]]
}

have() { command -v "$1" >/dev/null 2>&1; }

os_name() { uname -s | tr '[:upper:]' '[:lower:]'; }
is_macos() { [[ "$(os_name)" == "darwin" ]]; }
is_linux() { [[ "$(os_name)" == "linux" ]]; }

require_sudo_if_needed() {
  if is_linux; then
    if ! sudo -n true >/dev/null 2>&1; then
      say "Sudo access is required for apt installs."
      if [[ "$YES" == "1" ]]; then
        sudo true || die "Sudo required but not available."
      else
        say "You may be prompted for your password."
        sudo true || die "Sudo required but not available."
      fi
    fi
  fi
}

print_plan() {
  say ""
  say "== Fresh Machine Bootstrap Plan =="
  if is_macos; then
    say "- OS: macOS"
    say "- Install/ensure: Homebrew"
    say "- Install/ensure: git, python, node, pnpm, direnv, jq"
  elif is_linux; then
    say "- OS: Linux (Ubuntu assumed)"
    say "- Install/ensure: git, python3, venv, pip, curl, jq, direnv"
    say "- Node: install/upgrade to >= 18 (apt or nvm)"
    say "- pnpm: via corepack (preferred) or npm fallback"
  else
    die "Unsupported OS."
  fi
  say "- Then run: make bootstrap"
  say ""
}

install_homebrew() {
  if have brew; then
    say "Homebrew already installed."
    return 0
  fi
  say "Homebrew not found."
  if ! confirm "Install Homebrew now?"; then
    die "Homebrew is required on macOS for bootstrap-fresh."
  fi
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  if [[ -x /opt/homebrew/bin/brew ]]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
  elif [[ -x /usr/local/bin/brew ]]; then
    eval "$(/usr/local/bin/brew shellenv)"
  fi
  have brew || die "Homebrew install completed but 'brew' not found in PATH."
}

macos_install_packages() {
  install_homebrew
  say "Updating Homebrew…"
  brew update

  local pkgs=(git python node jq direnv)

  say "Will install/upgrade: ${pkgs[*]}"
  if confirm "Proceed with brew install/upgrade?"; then
    brew install "${pkgs[@]}" || true
    brew upgrade "${pkgs[@]}" || true
  else
    die "Aborted."
  fi

  if have pnpm; then
    say "pnpm already installed."
  else
    if have corepack; then
      say "Enabling corepack + pnpm…"
      corepack enable || true
      corepack prepare pnpm@latest --activate || true
    fi
    if ! have pnpm; then
      say "Installing pnpm via brew…"
      brew install pnpm || true
    fi
  fi

  say ""
  say "NOTE: To enable direnv in your shell:"
  say "  - zsh:  echo 'eval \"\$(direnv hook zsh)\"' >> ~/.zshrc"
  say "  - bash: echo 'eval \"\$(direnv hook bash)\"' >> ~/.bashrc"
}

node_major() {
  if ! have node; then
    echo "0"; return 0
  fi
  node -p "process.versions.node.split('.')[0]" 2>/dev/null || echo "0"
}

install_nvm_and_node() {
  local nvm_dir="${NVM_DIR:-$HOME/.nvm}"
  if [[ -d "$nvm_dir" && -s "$nvm_dir/nvm.sh" ]]; then
    say "nvm already installed at $nvm_dir"
  else
    say "Installing nvm…"
    curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
  fi

  export NVM_DIR="$nvm_dir"
  # shellcheck disable=SC1090
  [[ -s "$NVM_DIR/nvm.sh" ]] && . "$NVM_DIR/nvm.sh"

  have nvm || die "nvm installation failed."
  say "Installing Node LTS via nvm…"
  nvm install --lts
  nvm use --lts
  corepack enable || true
}

install_node_and_pnpm_ubuntu() {
  local major
  major="$(node_major)"

  if [[ "$major" -ge 18 ]]; then
    say "Node.js already present (major=$major)."
  else
    say "Node.js missing or too old (major=$major)."
    if confirm "Try apt install nodejs/npm first?"; then
      sudo apt-get install -y nodejs npm || true
    fi
    major="$(node_major)"
    if [[ "$major" -lt 18 ]]; then
      say "apt nodejs still missing/too old. Recommended: nvm."
      if confirm "Install Node via nvm?"; then
        install_nvm_and_node
      else
        die "Node.js >= 18 required."
      fi
    fi
  fi

  if have pnpm; then
    say "pnpm already installed."
  else
    if have corepack; then
      say "Enabling corepack + pnpm…"
      corepack enable || true
      corepack prepare pnpm@latest --activate || true
    fi
    if ! have pnpm; then
      if confirm "Install pnpm via npm -g pnpm?"; then
        npm install -g pnpm
      else
        die "pnpm required."
      fi
    fi
  fi
}

ubuntu_install_packages() {
  require_sudo_if_needed
  say "Updating apt…"
  sudo apt-get update -y

  local pkgs=(git curl ca-certificates jq direnv python3 python3-venv python3-pip python3-dev)

  say "Will install: ${pkgs[*]}"
  if confirm "Proceed with apt install?"; then
    sudo apt-get install -y "${pkgs[@]}"
  else
    die "Aborted."
  fi

  install_node_and_pnpm_ubuntu

  say ""
  say "NOTE: To enable direnv in your shell:"
  say "  echo 'eval \"\$(direnv hook bash)\"' >> ~/.bashrc"
}

run_bootstrap() {
  say ""
  say "== Running project bootstrap =="
  [[ -f Makefile ]] || die "Makefile not found. Run from repo root."
  make bootstrap
}

main() {
  print_plan
  if ! confirm "Proceed with fresh-machine bootstrap?"; then
    die "Aborted."
  fi

  if is_macos; then
    macos_install_packages
  elif is_linux; then
    ubuntu_install_packages
  else
    die "Unsupported OS."
  fi

  run_bootstrap

  say ""
  say "== Fresh bootstrap complete =="
  say "Copy/paste into Cursor as your first message:"
  say "-------------------------------------------"
  say "Read and obey: .cursor/START_HERE.md"
  say "My task: <describe what you want to build>"
  say "-------------------------------------------"
}

main "$@"

SHELL := /bin/bash
PWD := $(shell pwd)
PROJECT := workbench

UNAME := $(shell uname -s)

ifeq ($(UNAME),Darwin)
  VSCODE_USER := $(HOME)/Library/Application Support/Code/User
  CURSOR_USER := $(HOME)/Library/Application Support/Cursor/User
else
  VSCODE_USER := $(HOME)/.config/Code/User
  CURSOR_USER := $(HOME)/.config/Cursor/User
endif

NVIM_HOME := $(HOME)/.config/nvim
PROFILE_D := $(if $(filter $(UNAME),Darwin),$(HOME)/.zprofile.d,$(HOME)/.bashrc.d)
BACKUP_DIR := $(HOME)/.$(PROJECT)-backup

.PHONY: install install-vscode install-cursor install-nvim install-shell
.PHONY: uninstall uninstall-vscode uninstall-cursor uninstall-nvim uninstall-shell
.PHONY: backup extensions scaffold template setup snippets

# ─── Install ───────────────────────────────────────────────────────────────────

install: install-vscode install-cursor install-nvim install-shell
	@echo "Done. All configs symlinked."

install-vscode: backup
	ln -sfn "$(PWD)/vscode/settings.json" "$(VSCODE_USER)/settings.json"
	ln -sfn "$(PWD)/vscode/keybindings.json" "$(VSCODE_USER)/keybindings.json"
	ln -sfn "$(PWD)/vscode/tasks.json" "$(VSCODE_USER)/tasks.json"
	rm -rf "$(VSCODE_USER)/snippets"
	ln -sfn "$(PWD)/vscode/snippets" "$(VSCODE_USER)/snippets"
	@echo "VSCode config linked."

install-cursor: backup
	ln -sfn "$(PWD)/vscode/settings.json" "$(CURSOR_USER)/settings.json"
	ln -sfn "$(PWD)/vscode/keybindings.json" "$(CURSOR_USER)/keybindings.json"
	ln -sfn "$(PWD)/vscode/tasks.json" "$(CURSOR_USER)/tasks.json"
	rm -rf "$(CURSOR_USER)/snippets"
	ln -sfn "$(PWD)/vscode/snippets" "$(CURSOR_USER)/snippets"
	@echo "Cursor config linked."

install-nvim: backup
	@if [ -d "$(NVIM_HOME)" ] && [ ! -L "$(NVIM_HOME)" ]; then \
		echo "Error: $(NVIM_HOME) exists and is not a symlink. Run 'make backup' first, then remove it."; \
		exit 1; \
	fi
	ln -sfn "$(PWD)/nvim" "$(NVIM_HOME)"
	@echo "Neovim config linked."

install-shell: backup
	@mkdir -p "$(PROFILE_D)" "$(HOME)/.local/bin"
	@for f in $(PWD)/shell/profile.d/*.sh; do \
		name=$$(basename "$$f"); \
		ln -sfn "$$f" "$(PROFILE_D)/$$name"; \
	done
	@ln -sfn "$(PWD)/templates/scaffold" "$(HOME)/.local/bin/scaffold"
	@mkdir -p "$(HOME)/.config/workbench"
	@if [ ! -f "$(HOME)/.config/workbench/config" ]; then \
		cp "$(PWD)/templates/config.example" "$(HOME)/.config/workbench/config"; \
		echo "Created ~/.config/workbench/config — edit with your values"; \
	fi
	@echo "Shell scripts linked into $(PROFILE_D)"
	@echo "scaffold command linked into ~/.local/bin/"
	@if [ "$(UNAME)" = "Darwin" ]; then \
		if ! grep -qF '.zprofile.d' "$(HOME)/.zprofile" 2>/dev/null; then \
			echo '' >> "$(HOME)/.zprofile"; \
			echo '# $(PROJECT) shell scripts' >> "$(HOME)/.zprofile"; \
			echo 'for f in ~/.zprofile.d/*.sh; do [ -r "$$f" ] && source "$$f"; done' >> "$(HOME)/.zprofile"; \
			echo "Added .zprofile.d loader to ~/.zprofile"; \
		fi; \
	else \
		if ! grep -qF '.bashrc.d' "$(HOME)/.bashrc" 2>/dev/null; then \
			echo '' >> "$(HOME)/.bashrc"; \
			echo '# $(PROJECT) shell scripts' >> "$(HOME)/.bashrc"; \
			echo 'for f in ~/.bashrc.d/*.sh; do [ -r "$$f" ] && source "$$f"; done' >> "$(HOME)/.bashrc"; \
			echo "Added .bashrc.d loader to ~/.bashrc"; \
		fi; \
	fi

# ─── Uninstall ─────────────────────────────────────────────────────────────────

uninstall: uninstall-vscode uninstall-cursor uninstall-nvim uninstall-shell
	@echo "Done. Symlinks removed. Restore from $(BACKUP_DIR) if needed."

uninstall-vscode:
	@for f in settings.json keybindings.json tasks.json snippets; do \
		rm -f "$(VSCODE_USER)/$$f"; \
	done

uninstall-cursor:
	@for f in settings.json keybindings.json tasks.json snippets; do \
		rm -f "$(CURSOR_USER)/$$f"; \
	done

uninstall-nvim:
	@if [ -L "$(NVIM_HOME)" ]; then rm "$(NVIM_HOME)"; fi

uninstall-shell:
	@for f in $(PWD)/shell/profile.d/*.sh; do \
		name=$$(basename "$$f"); \
		rm -f "$(PROFILE_D)/$$name"; \
	done
	@echo "Shell symlinks removed from $(PROFILE_D)"

# ─── Backup ───────────────────────────────────────────────────────────────────

backup:
	@mkdir -p "$(BACKUP_DIR)/vscode" "$(BACKUP_DIR)/cursor" "$(BACKUP_DIR)/nvim" "$(BACKUP_DIR)/shell"
	@for f in settings.json keybindings.json; do \
		[ -f "$(VSCODE_USER)/$$f" ] && [ ! -L "$(VSCODE_USER)/$$f" ] && \
			cp "$(VSCODE_USER)/$$f" "$(BACKUP_DIR)/vscode/$$f" 2>/dev/null || true; \
	done
	@[ -d "$(VSCODE_USER)/snippets" ] && [ ! -L "$(VSCODE_USER)/snippets" ] && \
		cp -r "$(VSCODE_USER)/snippets" "$(BACKUP_DIR)/vscode/" 2>/dev/null || true
	@for f in settings.json keybindings.json; do \
		[ -f "$(CURSOR_USER)/$$f" ] && [ ! -L "$(CURSOR_USER)/$$f" ] && \
			cp "$(CURSOR_USER)/$$f" "$(BACKUP_DIR)/cursor/$$f" 2>/dev/null || true; \
	done
	@[ -d "$(CURSOR_USER)/snippets" ] && [ ! -L "$(CURSOR_USER)/snippets" ] && \
		cp -r "$(CURSOR_USER)/snippets" "$(BACKUP_DIR)/cursor/" 2>/dev/null || true
	@[ -d "$(NVIM_HOME)" ] && [ ! -L "$(NVIM_HOME)" ] && \
		cp -r "$(NVIM_HOME)" "$(BACKUP_DIR)/nvim/" 2>/dev/null || true
	@if [ -d "$(PROFILE_D)" ]; then \
		for f in "$(PROFILE_D)"/*.sh; do \
			[ -f "$$f" ] && [ ! -L "$$f" ] && cp "$$f" "$(BACKUP_DIR)/shell/" 2>/dev/null || true; \
		done; \
	fi
	@echo "Backup saved to $(BACKUP_DIR)"

# ─── Extensions ────────────────────────────────────────────────────────────────

extensions:
	@echo "Installing VSCode extensions..."
	@xargs -L1 code --install-extension < vscode/extensions.txt

# ─── Snippets ─────────────────────────────────────────────────────────────────

snippets:
	@./vscode/snippets/build.sh

# ─── Templates ─────────────────────────────────────────────────────────────────

template:
	@./vscode/templates/apply.sh

# ─── Scaffold ─────────────────────────────────────────────────────────────────

scaffold:
	@./templates/scaffold

# ─── Toolchain Setup ──────────────────────────────────────────────────────────

setup:
	@./setup.sh

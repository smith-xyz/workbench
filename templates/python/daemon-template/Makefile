PREFIX ?= /usr/local
BINDIR = $(PREFIX)/bin
SYSTEMD_DIR ?= /etc/systemd/system

.PHONY: run test lint check install-linux uninstall-linux install-macos uninstall-macos

run:
	python -m src.main

test:
	pytest

lint:
	ruff check .
	ruff format --check .
	mypy src/

check: lint test

install-linux:
	install -d "$(DESTDIR)$(BINDIR)" "$(DESTDIR)$(SYSTEMD_DIR)"
	install -m755 -D <(echo '#!/bin/sh\nexec python -m src.main "$$@"') "$(DESTDIR)$(BINDIR)/daemon-template"
	install -m644 deploy/linux/__SERVICE__.service "$(DESTDIR)$(SYSTEMD_DIR)/__SERVICE__.service"

uninstall-linux:
	rm -f "$(DESTDIR)$(BINDIR)/daemon-template"
	rm -f "$(DESTDIR)$(SYSTEMD_DIR)/__SERVICE__.service"

install-macos:
	cp deploy/macos/com.__ORG__.__SERVICE__.plist ~/Library/LaunchAgents/
	launchctl load ~/Library/LaunchAgents/com.__ORG__.__SERVICE__.plist

uninstall-macos:
	launchctl unload ~/Library/LaunchAgents/com.__ORG__.__SERVICE__.plist 2>/dev/null || true
	rm -f ~/Library/LaunchAgents/com.__ORG__.__SERVICE__.plist

PREFIX ?= /usr/local
BINDIR = $(PREFIX)/bin
SYSTEMD_UNIT = __SERVICE__
SYSTEMD_DIR ?= /etc/systemd/system

PROJECT_NAME = daemon-template
BINARY_NAME = daemon-template
RELEASE_DIR = target/release

.PHONY: all
all: build

.PHONY: help
help:
	@echo "Targets: build, build-release, run, fmt, clippy, check, install-linux, uninstall-linux, install-macos, uninstall-macos, docker-build"

.PHONY: build
build:
	cargo build

.PHONY: build-release
build-release:
	cargo build --release

.PHONY: run
run:
	cargo run

.PHONY: fmt
fmt:
	cargo fmt

.PHONY: clippy
clippy:
	cargo clippy --all-targets --all-features -- -D warnings

.PHONY: check
check:
	cargo fmt --check
	cargo clippy --all-targets --all-features -- -D warnings
	cargo test

.PHONY: test
test:
	cargo test

.PHONY: install-linux
install-linux: build-release
	install -d "$(DESTDIR)$(BINDIR)" "$(DESTDIR)$(SYSTEMD_DIR)"
	install -m755 "$(RELEASE_DIR)/$(BINARY_NAME)" "$(DESTDIR)$(BINDIR)/$(BINARY_NAME)"
	install -m644 deploy/linux/__SERVICE__.service "$(DESTDIR)$(SYSTEMD_DIR)/$(SYSTEMD_UNIT).service"

.PHONY: uninstall-linux
uninstall-linux:
	rm -f "$(DESTDIR)$(BINDIR)/$(BINARY_NAME)"
	rm -f "$(DESTDIR)$(SYSTEMD_DIR)/$(SYSTEMD_UNIT).service"

.PHONY: install-macos
install-macos: build-release
	install -d "$(DESTDIR)$(BINDIR)"
	install -m755 "$(RELEASE_DIR)/$(BINARY_NAME)" "$(DESTDIR)$(BINDIR)/$(BINARY_NAME)"
	cp deploy/macos/com.__ORG__.__SERVICE__.plist ~/Library/LaunchAgents/
	launchctl load ~/Library/LaunchAgents/com.__ORG__.__SERVICE__.plist

.PHONY: uninstall-macos
uninstall-macos:
	launchctl unload ~/Library/LaunchAgents/com.__ORG__.__SERVICE__.plist 2>/dev/null || true
	rm -f ~/Library/LaunchAgents/com.__ORG__.__SERVICE__.plist
	rm -f "$(DESTDIR)$(BINDIR)/$(BINARY_NAME)"

.PHONY: docker-build
docker-build:
	docker build -t $(PROJECT_NAME) .

.PHONY: clean
clean:
	cargo clean

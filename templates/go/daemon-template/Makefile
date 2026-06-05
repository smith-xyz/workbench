PREFIX ?= /usr/local
BINDIR = $(PREFIX)/bin
SYSTEMD_DIR ?= /etc/systemd/system
BINARY_NAME = __SERVICE__

.PHONY: build run test lint check install-linux uninstall-linux install-macos uninstall-macos

build:
	go build -o bin/$(BINARY_NAME) .

run:
	go run .

test:
	go test ./...

lint:
	golangci-lint run ./...

check: lint test

install-linux: build
	install -d "$(DESTDIR)$(BINDIR)" "$(DESTDIR)$(SYSTEMD_DIR)"
	install -m755 bin/$(BINARY_NAME) "$(DESTDIR)$(BINDIR)/$(BINARY_NAME)"
	install -m644 deploy/linux/__SERVICE__.service "$(DESTDIR)$(SYSTEMD_DIR)/$(BINARY_NAME).service"

uninstall-linux:
	rm -f "$(DESTDIR)$(BINDIR)/$(BINARY_NAME)"
	rm -f "$(DESTDIR)$(SYSTEMD_DIR)/$(BINARY_NAME).service"

install-macos: build
	install -d "$(DESTDIR)$(BINDIR)"
	install -m755 bin/$(BINARY_NAME) "$(DESTDIR)$(BINDIR)/$(BINARY_NAME)"
	cp deploy/macos/com.__ORG__.__SERVICE__.plist ~/Library/LaunchAgents/com.__ORG__.$(BINARY_NAME).plist
	launchctl load ~/Library/LaunchAgents/com.__ORG__.$(BINARY_NAME).plist

uninstall-macos:
	launchctl unload ~/Library/LaunchAgents/com.__ORG__.$(BINARY_NAME).plist 2>/dev/null || true
	rm -f ~/Library/LaunchAgents/com.__ORG__.$(BINARY_NAME).plist
	rm -f "$(DESTDIR)$(BINDIR)/$(BINARY_NAME)"

docker-build:
	docker build -t $(BINARY_NAME) .

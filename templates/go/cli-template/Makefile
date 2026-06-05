VERSION ?= $(shell git describe --tags --always --dirty 2>/dev/null || echo dev)
COMMIT  ?= $(shell git rev-parse --short HEAD 2>/dev/null || echo none)
DATE    ?= $(shell date -u +%Y-%m-%dT%H:%M:%SZ)
LDFLAGS := -X github.com/__ORG__/__SERVICE__/internal/version.Version=$(VERSION) \
           -X github.com/__ORG__/__SERVICE__/internal/version.Commit=$(COMMIT) \
           -X github.com/__ORG__/__SERVICE__/internal/version.Date=$(DATE)

.PHONY: build run test lint install

build:
	go build -ldflags "$(LDFLAGS)" -o bin/__SERVICE__ .

run:
	go run . run

test:
	go test ./...

lint:
	golangci-lint run ./...

install:
	go install -ldflags "$(LDFLAGS)" .

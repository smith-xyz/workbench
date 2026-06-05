.PHONY: run build test lint migrate migrate-create

run:
	go run ./cmd/api

build:
	go build -o bin/api ./cmd/api
	go build -o bin/migrate ./cmd/migrate

test:
	go test ./...

lint:
	golangci-lint run ./...

migrate:
	go run ./cmd/migrate up

migrate-down:
	go run ./cmd/migrate down

migrate-status:
	go run ./cmd/migrate status

migrate-create:
	@test -n "$(NAME)" || (echo "usage: make migrate-create NAME=add_users" && exit 1)
	go run ./cmd/migrate create $(NAME)

docker-build:
	docker build -t __SERVICE__ .

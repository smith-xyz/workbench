package main

import (
	"log/slog"
	"os"

	"github.com/__ORG__/__SERVICE__/internal/api"
	"github.com/__ORG__/__SERVICE__/internal/server"
)

func main() {
	cfg, err := api.ServerConfig()
	if err != nil {
		slog.Error("config", "err", err)
		os.Exit(1)
	}
	server.Run(server.New(cfg))
}

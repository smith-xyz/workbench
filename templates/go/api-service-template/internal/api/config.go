package api

import (
	"fmt"
	"io"
	"log/slog"

	"github.com/__ORG__/__SERVICE__/internal/apiutil"
	"github.com/__ORG__/__SERVICE__/internal/env"
	"github.com/__ORG__/__SERVICE__/internal/health"
	"github.com/__ORG__/__SERVICE__/internal/items"
	"github.com/__ORG__/__SERVICE__/internal/server"
	storedb "github.com/__ORG__/__SERVICE__/internal/store/db"
)

const DefaultListenAddr = ":8080"

type Config struct {
	ListenAddr  string
	DatabaseURL string
	DBPool      storedb.PoolConfig
}

func ConfigFromEnv() Config {
	return Config{
		ListenAddr:  env.Get("LISTEN_ADDR", DefaultListenAddr),
		DatabaseURL: env.Get("DATABASE_URL", ""),
		DBPool: storedb.PoolConfig{
			MaxOpenConns: env.GetInt("DB_MAX_OPEN_CONNS", storedb.DefaultMaxOpenConns),
			MaxIdleConns: env.GetInt("DB_MAX_IDLE_CONNS", storedb.DefaultMaxIdleConns),
		},
	}
}

func ServerConfig() (*server.Config, error) {
	cfg := ConfigFromEnv()
	d, closers, err := buildDeps(cfg)
	if err != nil {
		return nil, err
	}
	return &server.Config{
		Name:    "__SERVICE__",
		Addr:    cfg.ListenAddr,
		Handler: Routes(&d),
		Closers: closers,
	}, nil
}

func buildDeps(cfg Config) (APIDeps, []io.Closer, error) {
	if cfg.DatabaseURL == "" {
		return APIDeps{}, nil, fmt.Errorf("DATABASE_URL is required")
	}

	resp := &apiutil.Helper{Debug: env.GetBool("DEBUG", false)}

	db, err := storedb.OpenPostgres(cfg.DatabaseURL, cfg.DBPool)
	if err != nil {
		return APIDeps{}, nil, fmt.Errorf("postgres: %w", err)
	}

	var checks []health.Checker
	var closers []io.Closer
	checks = append(checks, db)
	closers = append(closers, db)

	slog.Info("postgres connected")

	itemRepo := items.NewRepository(db.Conn())
	itemSvc := items.NewService(itemRepo)

	return APIDeps{
		Items:  items.NewHandler(itemSvc, resp),
		Resp:   resp,
		Checks: checks,
	}, closers, nil
}

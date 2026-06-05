package main

import (
	"fmt"
	"log/slog"
	"os"

	"github.com/__ORG__/__SERVICE__/internal/env"
	storedb "github.com/__ORG__/__SERVICE__/internal/store/db"

	_ "github.com/__ORG__/__SERVICE__/internal/store/db/migrations"
)

func main() {
	if err := run(); err != nil {
		slog.Error(err.Error())
		os.Exit(1)
	}
}

func run() error {
	cmd := "up"
	if len(os.Args) > 1 {
		cmd = os.Args[1]
	}

	if cmd == "create" {
		if len(os.Args) < 3 {
			return fmt.Errorf("usage: migrate create <name>")
		}
		return storedb.CreateMigration(os.Args[2])
	}

	dbURL := os.Getenv("DATABASE_URL")
	if dbURL == "" {
		return fmt.Errorf("DATABASE_URL is required")
	}

	db, err := storedb.OpenPostgres(dbURL, storedb.PoolConfig{
		MaxOpenConns: env.GetInt("DB_MAX_OPEN_CONNS", storedb.DefaultMaxOpenConns),
		MaxIdleConns: env.GetInt("DB_MAX_IDLE_CONNS", storedb.DefaultMaxIdleConns),
	})
	if err != nil {
		return fmt.Errorf("database connection failed: %w", err)
	}
	defer func() { _ = db.Close() }()

	switch cmd {
	case "up":
		slog.Info("running migrations")
		if err := db.Migrate(); err != nil {
			return fmt.Errorf("migration failed: %w", err)
		}
		slog.Info("migrations complete")
	case "down":
		slog.Info("rolling back last migration")
		if err := db.Rollback(); err != nil {
			return fmt.Errorf("rollback failed: %w", err)
		}
		slog.Info("rollback complete")
	case "status":
		statuses, err := db.MigrationStatus()
		if err != nil {
			return fmt.Errorf("status check failed: %w", err)
		}
		fmt.Printf("%-45s %-10s %s\n", "VERSION", "STATUS", "APPLIED AT")
		fmt.Printf("%-45s %-10s %s\n", "-------", "------", "----------")
		for _, s := range statuses {
			status := "pending"
			appliedAt := ""
			if s.Applied {
				status = "applied"
				appliedAt = s.AppliedAt.Format("2006-01-02 15:04:05")
			}
			fmt.Printf("%-45s %-10s %s\n", s.Version, status, appliedAt)
		}
	default:
		return fmt.Errorf("unknown command %q, use: up, down, status, create", cmd)
	}
	return nil
}

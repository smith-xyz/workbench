package main

import (
	"context"
	"log/slog"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/__ORG__/__SERVICE__/internal/config"
	"github.com/__ORG__/__SERVICE__/internal/health"
)

func main() {
	cfg := config.Load()
	initLogger(cfg.LogJSON)

	slog.Info("starting", "tick_interval", cfg.TickInterval.String())

	ctx, cancel := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer cancel()

	hw := health.NewWriter(cfg.HealthFile)
	ticker := time.NewTicker(cfg.TickInterval)
	defer ticker.Stop()

	for {
		select {
		case <-ctx.Done():
			slog.Info("shutting down")
			return
		case <-ticker.C:
			if err := performWork(ctx); err != nil {
				slog.Error("tick failed", "err", err)
				hw.WriteError(err.Error())
			} else {
				hw.WriteOK()
			}
		}
	}
}

func performWork(ctx context.Context) error {
	slog.Debug("tick")
	return nil
}

func initLogger(jsonOutput bool) {
	var handler slog.Handler
	if jsonOutput {
		handler = slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{Level: slog.LevelDebug})
	} else {
		handler = slog.NewTextHandler(os.Stdout, &slog.HandlerOptions{Level: slog.LevelDebug})
	}
	slog.SetDefault(slog.New(handler))
}

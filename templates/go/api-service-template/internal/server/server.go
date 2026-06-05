package server

import (
	"context"
	"io"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"
)

type Config struct {
	Name              string
	Addr              string
	Handler           http.Handler
	ReadHeaderTimeout time.Duration
	LogLevel          slog.Level
	Closers           []io.Closer
}

type Server struct {
	config     *Config
	httpServer *http.Server
}

const defaultReadHeaderTimeout = 10 * time.Second

func New(cfg *Config) *Server {
	opts := &slog.HandlerOptions{Level: cfg.LogLevel}
	handler := slog.NewJSONHandler(os.Stdout, opts)
	logger := slog.New(handler).With("service", cfg.Name)
	slog.SetDefault(logger)
	return &Server{config: cfg}
}

func Run(srv *Server) {
	if err := untilSignal(srv); err != nil {
		slog.Error("server error", "err", err)
		os.Exit(1)
	}
}

func untilSignal(srv *Server) error {
	ctx, cancel := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer cancel()

	errCh := make(chan error, 1)
	go func() { errCh <- srv.ListenAndServe() }()

	select {
	case <-ctx.Done():
	case err := <-errCh:
		if err != nil && err != http.ErrServerClosed {
			return err
		}
		return nil
	}

	shutdownCtx, shutdownCancel := context.WithTimeout(context.WithoutCancel(ctx), 10*time.Second)
	defer shutdownCancel()
	if err := srv.Shutdown(shutdownCtx); err != nil {
		slog.Error("shutdown failed", "err", err)
	}
	if err := <-errCh; err != nil && err != http.ErrServerClosed {
		return err
	}
	return nil
}

func (s *Server) ListenAndServe() error {
	addr := s.config.Addr
	if addr == "" {
		addr = ":8080"
	}
	timeout := s.config.ReadHeaderTimeout
	if timeout == 0 {
		timeout = defaultReadHeaderTimeout
	}
	s.httpServer = &http.Server{
		Addr:              addr,
		Handler:           s.config.Handler,
		ReadHeaderTimeout: timeout,
	}
	slog.Info("server starting", "addr", addr)
	return s.httpServer.ListenAndServe()
}

func (s *Server) Shutdown(ctx context.Context) error {
	if s.httpServer == nil {
		return nil
	}
	slog.Info("server shutting down")
	err := s.httpServer.Shutdown(ctx)
	for _, c := range s.config.Closers {
		if cerr := c.Close(); cerr != nil {
			slog.Warn("closer failed", "err", cerr)
		}
	}
	return err
}

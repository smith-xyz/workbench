package config

import (
	"os"
	"strconv"
	"time"
)

type Config struct {
	TickInterval time.Duration
	HealthFile   string
	LogJSON      bool
}

func Load() Config {
	return Config{
		TickInterval: durationSecs("DAEMON_TICK_INTERVAL_SECS", 30),
		HealthFile:   envOr("DAEMON_HEALTH_FILE", "/tmp/__SERVICE__-health.json"),
		LogJSON:      envBool("DAEMON_LOG_JSON", false),
	}
}

func envOr(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}

func envBool(key string, fallback bool) bool {
	v := os.Getenv(key)
	if v == "" {
		return fallback
	}
	b, err := strconv.ParseBool(v)
	if err != nil {
		return fallback
	}
	return b
}

func durationSecs(key string, fallback int) time.Duration {
	v := os.Getenv(key)
	if v == "" {
		return time.Duration(fallback) * time.Second
	}
	n, err := strconv.Atoi(v)
	if err != nil || n < 1 {
		return time.Duration(fallback) * time.Second
	}
	return time.Duration(n) * time.Second
}

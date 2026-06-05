package db

import (
	"context"
	"database/sql"
	"fmt"
	"log"
	"os"
	"strings"

	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

const (
	DefaultMaxOpenConns = 10
	DefaultMaxIdleConns = 5
)

type PoolConfig struct {
	MaxOpenConns int `yaml:"maxOpenConns"`
	MaxIdleConns int `yaml:"maxIdleConns"`
}

type DB struct {
	conn  *gorm.DB
	sqlDB *sql.DB
}

func (db *DB) Conn() *gorm.DB                  { return db.conn }
func (db *DB) Health(ctx context.Context) error { return db.sqlDB.PingContext(ctx) }
func (db *DB) Name() string                    { return "postgres" }
func (db *DB) Close() error                    { return db.sqlDB.Close() }

type builder struct {
	open         func(string) gorm.Dialector
	dsn          string
	maxOpenConns int
	maxIdleConns int
	logLevel     logger.LogLevel
}

func newBuilder(open func(string) gorm.Dialector, dsn string) *builder {
	return &builder{
		open:         open,
		dsn:          dsn,
		logLevel:     logLevelFromEnv(),
		maxOpenConns: DefaultMaxOpenConns,
		maxIdleConns: DefaultMaxIdleConns,
	}
}

func logLevelFromEnv() logger.LogLevel {
	switch strings.ToLower(os.Getenv("DB_LOG_LEVEL")) {
	case "silent":
		return logger.Silent
	case "error":
		return logger.Error
	case "info":
		return logger.Info
	default:
		return logger.Warn
	}
}

func (b *builder) WithPoolConfig(p PoolConfig) *builder {
	if p.MaxOpenConns > 0 {
		b.maxOpenConns = p.MaxOpenConns
	}
	if p.MaxIdleConns > 0 {
		b.maxIdleConns = p.MaxIdleConns
	}
	return b
}

func (b *builder) Build() (*DB, error) {
	gormLogger := logger.New(log.New(os.Stderr, "\n", log.LstdFlags), logger.Config{
		LogLevel: b.logLevel,
	})

	conn, err := gorm.Open(b.open(b.dsn), &gorm.Config{Logger: gormLogger})
	if err != nil {
		return nil, fmt.Errorf("connect to database: %w", err)
	}

	sqlDB, err := conn.DB()
	if err != nil {
		return nil, fmt.Errorf("underlying sql.DB: %w", err)
	}
	sqlDB.SetMaxOpenConns(b.maxOpenConns)
	sqlDB.SetMaxIdleConns(b.maxIdleConns)

	return &DB{conn: conn, sqlDB: sqlDB}, nil
}
